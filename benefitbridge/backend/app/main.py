from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .models import Profile, AskRequest
from .qdrant_store import SchemeStore
from .eligibility import rank
from .lyzr import ask_lyzr

app = FastAPI(title="BenefitBridge API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=[settings.frontend_origin, "http://localhost:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
store = SchemeStore()

@app.get("/api/health")
def health():
    return {"ok": True, "qdrant": True, "lyzr_configured": bool(settings.lyzr_api_key and settings.lyzr_agent_id), "schemes": len(store.schemes)}

@app.get("/api/schemes")
def schemes():
    return store.schemes

@app.post("/api/match")
def match(profile: Profile):
    query = " ".join([profile.occupation, profile.state, " ".join(profile.life_events), "government benefits", str(profile.age)])
    candidates = store.search(query, limit=8)
    results = rank(profile, candidates)
    return {"profile": profile, "results": results[:8]}

@app.post("/api/search")
def search(body: AskRequest):
    candidates = store.search(body.question, limit=8)
    if body.profile:
        candidates = rank(body.profile, candidates)
    return {"results": candidates[:8]}

@app.post("/api/ask")
def ask(body: AskRequest):
    candidates = store.search(body.question, limit=5)
    context = "\n".join([f"- {x['name']}: {x['benefit']} | Documents: {', '.join(x['documents'])} | Official: {x['official_url']}" for x in candidates])
    answer = ask_lyzr(body.question, context)
    if answer and not answer.startswith("Lyzr could not be reached"):
        return {"answer": answer, "source": "Lyzr AI + Qdrant", "results": candidates}
    if not candidates:
        return {"answer": "I could not find a matching scheme in the current verified dataset. Please try a more specific question.", "source": "Qdrant", "results": []}
    top = candidates[0]
    return {"answer": f"The closest match is {top['name']}. {top['benefit']}\n\nDocuments: {', '.join(top['documents'])}.\n\nAlways verify current eligibility and application instructions on the official portal: {top['official_url']}", "source": "Qdrant local fallback", "results": candidates}
