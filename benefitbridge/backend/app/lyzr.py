import uuid
import requests
from .config import settings

SYSTEM_CONTEXT = """You are BenefitBridge, a careful government-benefit navigation assistant for India.\nUse only the scheme context supplied in the message. Do not invent eligibility, benefit amounts, deadlines, or documents. Clearly say when a rule must be verified on the official portal. Prefer concise, practical answers. You may answer in Tamil when asked."""

def ask_lyzr(question: str, scheme_context: str, user_id: str = "demo-user"):
    if not settings.lyzr_api_key or not settings.lyzr_agent_id:
        return None
    message = f"{SYSTEM_CONTEXT}\n\nVERIFIED SCHEME CONTEXT:\n{scheme_context}\n\nUSER QUESTION:\n{question}"
    payload = {
        "user_id": user_id,
        "agent_id": settings.lyzr_agent_id,
        "session_id": str(uuid.uuid4()),
        "message": message,
    }
    try:
        r = requests.post(settings.lyzr_api_url, headers={"Content-Type": "application/json", "x-api-key": settings.lyzr_api_key}, json=payload, timeout=30)
        r.raise_for_status()
        data = r.json()
        return data.get("response") or data.get("message") or str(data)
    except Exception as exc:
        return f"Lyzr could not be reached right now. Showing the verified scheme data instead. ({type(exc).__name__})"
