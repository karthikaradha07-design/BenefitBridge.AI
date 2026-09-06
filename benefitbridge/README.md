# GovScheme AI

GovScheme AI is a responsible, demo-ready full-stack navigator for Indian government schemes. It helps citizens discover relevant programmes, understand likely matches, and reach the official application portal.

> **Important:** Results are recommendations, not official eligibility decisions. Always verify current rules, documents, deadlines, and application instructions on the official government portal.

## What it includes

- Responsive React + Vite interface with home, catalogue, eligibility checker, AI assistant, dashboard, about, and scheme detail views
- Multi-step profile form with explainable percentage-style matching
- Searchable scheme catalogue with category filtering and official source links
- FastAPI endpoints for schemes, search, eligibility, chat, profiles, categories, states, and health
- Local sample data and deterministic retrieval so the project runs in demo mode without API keys
- Qdrant local embedded mode or Qdrant Cloud support
- Lyzr integration boundary for configured conversational responses
- Enkrypt-ready response safety boundary that removes overconfident eligibility language
- PostgreSQL Docker service, with SQLite as the local fallback configuration
- CORS, Pydantic validation, environment configuration, and GitHub-safe secret handling

## Architecture

```text
React / Vite
    -> FastAPI
    -> profile validation and eligibility scoring
    -> Qdrant retrieval (local embedded or cloud)
    -> Lyzr conversational reasoning (optional)
    -> safety screening / verification disclaimer
    -> explainable recommendations and official portal links
```

## Project structure

```text
govscheme-ai/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── eligibility.py
│   │   ├── qdrant_store.py
│   │   ├── lyzr.py
│   │   ├── safety.py
│   │   └── config.py
│   └── requirements.txt
├── data/schemes.json
├── frontend/src/main.jsx
├── frontend/src/styles.css
├── .env.example
├── docker-compose.yml
└── README.md
```

## Run locally

### Backend

Python 3.10+ is recommended.

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item ..\.env.example .env
uvicorn app.main:app --reload --port 8000
```

The API documentation is available at `http://localhost:8000/docs`.

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

Open the Vite URL, normally `http://localhost:5173`.

## Environment variables

Copy `.env.example` to `backend/.env`. Demo mode is enabled by default and does not require credentials.

| Variable | Purpose |
| --- | --- |
| `DEMO_MODE=true` | Uses local sample retrieval and safe deterministic fallbacks |
| `LYZR_API_KEY` / `LYZR_AGENT_ID` | Optional Lyzr agent credentials |
| `ENKRYPT_API_KEY` / `ENKRYPT_API_URL` | Optional safety provider credentials |
| `QDRANT_URL` / `QDRANT_API_KEY` | Optional Qdrant Cloud connection |
| `QDRANT_COLLECTION` | Qdrant collection name |
| `DATABASE_URL` | PostgreSQL in deployment or SQLite fallback locally |
| `FRONTEND_ORIGIN` | Allowed browser origin for CORS |

API keys are read only by the backend and are never sent to the browser.

## Qdrant and database options

With no `QDRANT_URL`, the backend uses Qdrant's local embedded storage under `qdrant_storage/` and seeds it from `data/schemes.json`. For optional infrastructure:

```powershell
docker compose up -d postgres qdrant
```

Then set the Qdrant URL and PostgreSQL `DATABASE_URL` in `backend/.env`. The current demo keeps the authoritative sample dataset in JSON so it remains easy to inspect and replace.

## API surface

- `GET /api/health`
- `GET /api/schemes`
- `GET /api/schemes/{id}`
- `GET /api/categories`
- `GET /api/states`
- `POST /api/eligibility/check`
- `POST /api/match` (backward-compatible alias)
- `POST /api/schemes/search`
- `POST /api/chat` and `POST /api/ask`
- `POST /api/profile`

## Data and responsible use

The included schemes are sample/demo records intended to demonstrate the product flow. They should be reviewed against current official sources before any public launch. The UI labels demo mode and every recommendation includes a verification reminder.

## GitHub

```powershell
git init
git add .
git commit -m "Build GovScheme AI navigator"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/govscheme-ai.git
git push -u origin main
```

Do not commit `backend/.env`, API keys, `node_modules`, build output, or local Qdrant data.

## Future scope

- Replace sample records with an editorially verified ingestion pipeline
- Add authenticated profiles and persistent saved schemes
- Add regional languages and accessibility testing with citizens
- Add provider-backed Enkrypt policy enforcement and PostgreSQL persistence
- Add automated source freshness checks and API contract tests