# BenefitBridge — Intelligent Government Welfare Discovery Platform

**BenefitBridge** is a full-stack civic-tech web application built to eliminate information asymmetry and empower citizens—especially farmers, students, senior citizens, persons with disabilities, and low-income households—to discover, evaluate, and claim official government welfare schemes, grants, and subsidies.

It combines a **Deterministic Explainable Rule Engine** with an **AI Recommendation Service (Lyzr Orchestrator + Qdrant Vector Search)**, an **OCR Document Verification & Cross-Checking Engine**, and a **Voice Assistant** powered by the Web Speech API.

---

## Architecture Overview

```
agenticai/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── endpoints/
│   │   │       │   ├── profile.py          # User profile CRUD & demo presets
│   │   │       │   ├── eligibility.py      # Rule engine & explainable breakdowns
│   │   │       │   └── discovery.py        # Scheme catalog, Qdrant search, Lyzr AI, OCR
│   │   │       └── __init__.py
│   │   ├── core/
│   │   │   ├── config.py                   # Pydantic Settings & environment variables
│   │   │   └── security.py                 # File sanitization & security checks
│   │   ├── services/
│   │   │   ├── rule_engine.py              # Deterministic, explainable eligibility checker
│   │   │   ├── lyzr_orchestrator.py        # Lyzr AI agent with intelligent fallback
│   │   │   ├── qdrant_client.py            # Qdrant vector client with in-memory fallback
│   │   │   └── ocr_engine.py               # Document OCR extraction & profile cross-check
│   │   ├── models/
│   │   │   ├── profile.py                  # SQLAlchemy UserProfile model
│   │   │   ├── scheme.py                   # SQLAlchemy Scheme model (16+ pre-seeded)
│   │   │   └── document.py                 # SQLAlchemy DocumentRecord model
│   │   ├── schemas/
│   │   │   ├── profile.py                  # Pydantic profile request/response schemas
│   │   │   ├── scheme.py                   # Pydantic scheme schemas & filter parameters
│   │   │   ├── eligibility.py              # Pydantic eligibility breakdown schemas
│   │   │   ├── document.py                 # Pydantic document OCR verification schemas
│   │   │   └── recommendation.py           # Pydantic AI recommendation schemas
│   │   ├── database.py                     # SQLAlchemy PostgreSQL engine with SQLite fallback
│   │   ├── seed_data.py                    # 16 pre-populated Indian national/state schemes
│   │   └── main.py                         # FastAPI app with CORS & lifespan DB init
│   ├── requirements.txt                    # Backend dependencies
│   ├── test_backend.py                     # Automated backend verification test suite
│   ├── run.py                              # Backend startup runner
│   └── .env.example                        # Backend environment template
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard/
│   │   │   │   └── Dashboard.jsx           # Profile summary, unlocked benefits, rule checklists
│   │   │   ├── ProfileForm/
│   │   │   │   └── ProfileForm.jsx         # Demographic assessment & 1-click presets
│   │   │   ├── VerificationTool/
│   │   │   │   └── VerificationTool.jsx    # File upload, OCR extraction, discrepancy alerts
│   │   │   ├── Discovery/
│   │   │   │   ├── SchemeCard.jsx          # Scheme card with benefit pills & speech audio
│   │   │   │   ├── SchemeModal.jsx         # Full scheme modal with official portal links
│   │   │   │   └── SchemesCatalog.jsx      # Filterable & searchable catalog
│   │   │   └── Common/
│   │   │       ├── Navbar.jsx              # Navigation, demo persona dropdown, voice trigger
│   │   │       ├── Hero.jsx                # Landing page hero & key stats
│   │   │       ├── Footer.jsx              # Attribution & portal links
│   │   │       └── VoiceAssistantModal.jsx # Voice interaction dock with sound visualizer
│   │   ├── hooks/
│   │   │   ├── useDiscovery.js             # Scheme discovery, search & category filters
│   │   │   └── useVoice.js                 # Web Speech API speech-to-text & read-aloud TTS
│   │   ├── services/
│   │   │   └── api.js                      # Axios REST client configured for backend
│   │   ├── App.jsx                         # Main app orchestrating views and hooks
│   │   ├── main.jsx                        # React root entry
│   │   └── index.css                       # Tailwind CSS v4 styling & animations
│   ├── package.json
│   ├── vite.config.js                      # Vite configuration with backend proxy
│   └── .env.example
│
└── README.md
```

---

## Key Features

### 1. Deterministic, Explainable Rule Engine (`rule_engine.py`)
- Unlike black-box ML models, government welfare distribution requires **100% statutory transparency**.
- Every single scheme evaluation tests:
  - Age limits (min/max age)
  - Gender targeting (e.g. women-only maternal grants)
  - Income ceilings (BPL, EWS cap, creamy layer)
  - Occupational reservations (Farmers, Cultivators, Street Vendors, Students, Artisans)
  - Landholding thresholds (e.g. small/marginal farmer $< 2.5$ acres)
  - Disability benchmark status ($\ge 40\%$ certified PwD)
  - Senior citizen status ($60+$ years)
  - Geographic jurisdiction (Pan-India Central vs State-specific)
  - Social reservations (General, OBC, SC, ST, EWS)
  - Ration card tiers (BPL, Antyodaya / AAY, APL)
- Outputs:
  - `ELIGIBLE`: 100% criteria met, ready to apply.
  - `PARTIALLY_ELIGIBLE`: $\ge 70\%$ match with precise actionable advice on what's missing (e.g. *"Requires income certificate under ₹2.5L"*).
  - `NOT_ELIGIBLE`: Lists primary failure reasons.

### 2. AI Recommendation Service (`lyzr_orchestrator.py` + `qdrant_client.py`)
- **Lyzr Orchestrator**:
  - Connects to live Lyzr Agent API when `LYZR_API_KEY` is present.
  - When keys are absent, runs an intelligent semantic reasoning orchestrator that analyzes multi-factor vulnerability and demographic synergies.
  - **Explainability Guardrail**: Clearly distinguishes AI recommendations from deterministic verified rules with distinct badges (🤖 `AI Suggestion` vs 🏛️ `Verified Government Eligibility`).
- **Qdrant Vector Service**:
  - Semantic vector search for schemes across descriptions, benefits, and categories.
  - Seamlessly falls back to an in-memory TF-IDF cosine similarity index if no remote Qdrant cluster is specified.

### 3. Verification & OCR Analysis Tool (`ocr_engine.py` + `VerificationTool.jsx`)
- Upload certificates (PDF, PNG, JPG, WEBP, or TXT).
- OCR engine extracts key entities: Certified Annual Income, Beneficiary Name, State, Certificate ID, Disability Percentage.
- Cross-references document values against stated Citizen Profile values to detect discrepancies before official portal submission.
- **Safety Disclaimer**: Prominently warns users: *"Document Analysis & Cross-Check Only: This is an automated preliminary citizen readiness check and does not constitute official government authentication or statutory verification."*
- Includes 1-click **Sample Demo Documents** (Income Certificate, Aadhaar, UDID Disability Card) for instant testing.

### 4. Accessibility & Voice Support (`useVoice.js`)
- Uses the browser's native **Web Speech API** for hands-free interaction.
- Voice command parsing:
  - *"Search agriculture schemes"* $\rightarrow$ Filters to agricultural welfare.
  - *"Find scholarships"* $\rightarrow$ Filters to student education programs.
  - *"Check my eligibility"* $\rightarrow$ Opens the Eligibility Dashboard.
  - *"Verify documents"* $\rightarrow$ Opens the Verification Tool.
- **Text-to-Speech (TTS)**: Reads scheme benefits and application steps out loud for low-literacy or visually impaired citizens.

### 5. 1-Click Demographic Demo Personas
For rapid hackathon judging and live demonstrations:
- 🌾 **Marginal Farmer (UP)**: Income ₹1,20,000, 2.2 acres, eligible for PM-KISAN, PMFBY, PMAY-G (~₹2,33,000 in benefits unlocked).
- 🎓 **College Student (SC)**: Age 19, Maharashtra, eligible for Post-Matric Scholarship, NMMSS.
- 👵 **Senior Citizen (AAY)**: Age 68, Rajasthan, BPL/AAY card, eligible for Old Age Pension (IGNOAPS), PM-JAY.
- ♿ **Differently-Abled Artisan**: 50% locomotor disability, Bangalore, eligible for ADIP free assistive aids, IGNDPS, PM SVANidhi.

---

## Installation & Setup

### Prerequisites
- **Python**: 3.10+ (Python 3.11 recommended)
- **Node.js**: v18+ (v20+ or v24+ recommended)

---

### Step 1: Backend Setup (FastAPI)

1. Open a terminal in the project directory:
   ```bash
   cd agenticai/backend
   ```

2. (Optional) Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # On Windows PowerShell:
   .\venv\Scripts\Activate.ps1
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure Environment Variables:
   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   *Note: BenefitBridge defaults to SQLite (`sqlite:///./benefitbridge.db`) out-of-the-box. If you have PostgreSQL running, set `DATABASE_URL=postgresql://user:password@localhost:5432/benefitbridge_db`.*

5. Run the Automated Backend Verification Suite:
   ```bash
   python test_backend.py
   ```
   *Expected output: All 6 test suites pass with 200 OK!*

6. Start the Backend Server:
   ```bash
   python run.py
   ```
   *API will start at `http://localhost:8000` with interactive Swagger docs at `http://localhost:8000/docs`.*

---

### Step 2: Frontend Setup (React + Vite + Tailwind)

1. Open a new terminal in the project directory:
   ```bash
   cd agenticai/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the Frontend Development Server:
   ```bash
   npm run dev
   ```
   *The application will launch at `http://localhost:5173`.*

---

## Configuration & Credentials Guide

The application is architected to work **immediately without external paid credentials**, while supporting live external services when API keys are added to `backend/.env`:

| Service | Environment Variable | Where to Obtain | Default Fallback Behavior |
| :--- | :--- | :--- | :--- |
| **PostgreSQL** | `DATABASE_URL` | Local Postgres or Supabase / Neon | Automatically falls back to local SQLite (`sqlite:///./benefitbridge.db`) |
| **Lyzr Agent Studio** | `LYZR_API_KEY` | [studio.lyzr.ai](https://studio.lyzr.ai) | Runs local multi-factor semantic reasoning orchestrator with AI rationale |
| **Qdrant Vector DB** | `QDRANT_URL`, `QDRANT_API_KEY` | [cloud.qdrant.io](https://cloud.qdrant.io) | Runs fast in-memory cosine TF-IDF vector search |
| **OCR Provider** | `OCR_PROVIDER` | Local Tesseract / Cloud Vision | Uses built-in certificate layout parser & regex cross-check |

---

## Hackathon 3-Minute Demo Walkthrough

1. **Home Page**:
   - Open `http://localhost:5173`.
   - Show the BenefitBridge mission and key statistics (₹2.5L+ Max Benefit, 100% Explainable Rules).

2. **1-Click Demographic Persona**:
   - In the top navigation bar, click the **"Demo Personas"** dropdown.
   - Select **"🌾 Marginal Farmer (UP)"**.
   - Notice how the app instantly loads Ramesh Kumar's profile and navigates to the **Eligibility Dashboard**.

3. **Explainable Rule Breakdown**:
   - In the Dashboard, show the **"Potential Benefits Unlocked"** counter (₹2,33,000 / year).
   - Click on **"PM-KISAN"** or **"PM Awas Yojana"** to expand the rule accordion.
   - Show the green **"Passed Government Criteria"** breakdown: confirms age, income under ceiling, farmer status, and landholding.
   - Click the **"AI Recommendations"** tab: show the distinct 🤖 `AI Suggestion` badge and natural language AI rationale explaining *why* the orchestrator recommended specific programs.

4. **Document Verification & OCR Cross-Check**:
   - Click **"Verify Documents"** in the navigation bar.
   - Note the statutory safety disclaimer badge.
   - Click the 1-click demo button **"📄 Sample Income Certificate"**.
   - Watch the OCR extraction report display side-by-side comparison:
     - Profile Income: ₹1,20,000
     - Document Income: ₹1,20,000
     - Status: `Verified Match` (90% Readiness Score).

5. **Voice Assistant**:
   - Click the **"Voice Assistant"** button in the navbar.
   - Speak or click *"Search agriculture schemes"* or *"Find college scholarships"*.
   - Watch the schemes catalog filter automatically in real-time.
   - Click the **Volume Speaker icon** on any scheme card to hear the details read aloud!

---

## API Endpoints Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Service health status |
| `GET` | `/api/v1/discovery/schemes` | List, filter, and vector-search schemes |
| `GET` | `/api/v1/discovery/schemes/{id}` | Complete scheme specification & application steps |
| `GET` | `/api/v1/discovery/categories` | Categories list with scheme counts |
| `POST` | `/api/v1/discovery/recommendations/{profile_id}` | Lyzr AI recommendations with explainable rationale |
| `POST` | `/api/v1/discovery/verify-document` | Multipart document upload for OCR & profile cross-check |
| `POST` | `/api/v1/profile/` | Create citizen demographic profile |
| `GET` | `/api/v1/profile/{id}` | Retrieve profile details |
| `POST` | `/api/v1/profile/demo-preset/{preset_name}` | Load demo persona (`marginal_farmer`, `college_student`, etc.) |
| `GET` | `/api/v1/eligibility/check/{profile_id}` | Comprehensive deterministic rule engine evaluation |
| `POST` | `/api/v1/eligibility/check-adhoc` | Ad-hoc eligibility evaluation without persistence |

---

## License

MIT License. Designed for civic empowerment and public welfare accessibility.
