# BenefitBridge — AI Government Benefit Navigator

A complete working prototype for discovering Indian government schemes using a profile, eligibility rules, Qdrant retrieval and Lyzr AI.

## Architecture
React → FastAPI → eligibility + Qdrant retrieval → Lyzr AI → verified scheme results → application guidance

## Features
- Responsive green/orange/white UI
- Profile wizard for age, state, occupation, income, gender and life events
- Eligibility scoring and explainable reasons
- Qdrant vector search for scheme discovery
- Lyzr Agent API integration
- English/Tamil UI toggle
- AI assistant for scheme questions
- Document checklist and application links
- Sample verified scheme dataset
- Works locally even before API credentials are added: deterministic matching and a safe local assistant fallback remain available

## 1. Start backend

Python 3.10+ recommended.

```bash
cd backend
python -m venv .venv
# Windows PowerShell:
.venv\\Scripts\\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env   # Windows CMD
# cp .env.example .env   # macOS/Linux
uvicorn app.main:app --reload --port 8000
```

## 2. Start frontend

Node.js 18+ recommended.

```bash
cd frontend
npm install
npm run dev
```

Open the URL printed by Vite (normally http://localhost:5173).

## 3. Qdrant

The app supports Qdrant Cloud or a local Qdrant server. If `QDRANT_URL` is empty, it uses Qdrant's local embedded mode and stores data in `../qdrant_storage`.

For Qdrant Cloud, set:

```env
QDRANT_URL=https://YOUR-CLUSTER.cloud.qdrant.io
QDRANT_API_KEY=your_qdrant_key
```

## 4. Lyzr

Create an agent in Lyzr Studio and set its ID and API key:

```env
LYZR_API_KEY=your_lyzr_api_key
LYZR_AGENT_ID=your_lyzr_agent_id
LYZR_API_URL=https://agent.api.lyzr.app/v2/chat/
```

The code uses the documented Lyzr chat endpoint with `x-api-key`, `user_id`, `agent_id`, `session_id`, and `message`.

## 5. Optional data refresh

The backend automatically seeds the Qdrant collection from `../data/schemes.json` on startup. You can add more schemes using the same JSON structure and restart the backend.

## Important
API keys are never stored in the frontend. Put them only in `backend/.env`. Do not commit `.env` to Git.
