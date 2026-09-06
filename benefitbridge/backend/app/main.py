from pathlib import Path
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .models import Profile, AskRequest, SearchRequest, EligibilityRequest, ProfileRequest
from .qdrant_store import SchemeStore
from .eligibility import enrich_results
from .lyzr import ask_lyzr
from .safety import screen_response

logging.basicConfig(level=logging.INFO)
app = FastAPI(title="GovScheme AI API", version="2.0.0", description="Demo-mode government scheme discovery API")
app.add_middleware(CORSMiddleware, allow_origins=[settings.frontend_origin, "http://localhost:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
store = SchemeStore()

@app.get("/api/health")
def health():
    return {"ok": True, "demo_mode": settings.demo_mode, "qdrant": True, "lyzr_configured": bool(settings.lyzr_api_key and settings.lyzr_agent_id), "enkrypt_configured": bool(settings.enkrypt_api_key), "schemes": len(store.schemes)}

@app.get("/api/schemes")
def schemes():
    return store.schemes

@app.get("/api/schemes/{scheme_id}")
def scheme_detail(scheme_id: str):
    scheme = next((item for item in store.schemes if item["id"] == scheme_id), None)
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    return scheme

@app.get("/api/categories")
def categories():
    return sorted({item["category"] for item in store.schemes})

@app.get("/api/states")
def states():
    return sorted({item["state"] for item in store.schemes})

@app.post("/api/match")
def match(profile: Profile):
    query = " ".join([profile.occupation, profile.state, " ".join(profile.life_events), "government benefits", str(profile.age)])
    candidates = store.search(query, limit=8)
    results = enrich_results(profile, candidates)
    return {"profile": profile, "results": results[:8], "disclaimer": "These are recommendations, not an official eligibility decision. Verify details on the official portal."}

@app.post("/api/eligibility/check")
def eligibility_check(profile: EligibilityRequest):
    return match(profile)

@app.post("/api/schemes/search")
def search_schemes(body: SearchRequest):
    candidates = store.search(body.query or "government scheme", limit=len(store.schemes))
    filtered = [item for item in candidates if (not body.category or item["category"].lower() == body.category.lower()) and (not body.state or item["state"].lower() in (body.state.lower(), "all india")) and (body.age is None or item["min_age"] <= body.age <= item["max_age"]) and (body.income is None or item.get("income_max") is None or body.income <= item["income_max"])]
    return {"results": filtered}

@app.post("/api/profile")
def save_profile(profile: ProfileRequest):
    return {"saved": True, "profile": profile, "message": "Profile saved for this demo session."}

@app.post("/api/search")
def search(body: AskRequest):
    candidates = store.search(body.question, limit=8)
    if body.profile:
        candidates = enrich_results(body.profile, candidates)
    return {"results": candidates[:8]}

@app.post("/api/ask")
@app.post("/api/chat")
def ask(body: AskRequest):
    candidates = store.search(body.question, limit=5)
    context = "\n".join([f"- {x['name']}: {x['benefit']} | Documents: {', '.join(x['documents'])} | Official: {x['official_url']}" for x in candidates])
    answer = screen_response(ask_lyzr(body.question, context))
    if answer and not answer.startswith("Lyzr could not be reached"):
        return {"answer": answer, "source": "Lyzr AI + Qdrant", "results": candidates, "demo_mode": settings.demo_mode}
    if not candidates:
        return {"answer": "I could not find a matching scheme in the current verified dataset. Please try a more specific question.", "source": "Qdrant", "results": [], "demo_mode": settings.demo_mode}
    top = candidates[0]
    return {"answer": f"The closest match is {top['name']}. {top['benefit']}\n\nDocuments: {', '.join(top['documents'])}.\n\nAlways verify current eligibility and application instructions on the official portal: {top['official_url']}", "source": "Qdrant local fallback", "results": candidates, "demo_mode": settings.demo_mode}
