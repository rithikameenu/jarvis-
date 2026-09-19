# FinSecure Sentinel™ — Real-Time Banking Fraud Detection & Compliance Engine

[![Tests](https://img.shields.io/badge/Tests-13%2F13%20Passing-emerald)]()
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-blue)]()
[![React](https://img.shields.io/badge/Frontend-React%2018%20%2B%20Vite-indigo)]()
[![ML](https://img.shields.io/badge/ML%20Engine-XGBoost%20%2B%20IsolationForest-amber)]()
[![RAG](https://img.shields.io/badge/RAG-FAISS%20%2B%20BM25-cyan)]()

A high-performance core banking fraud risk management platform that combines real-time machine learning inference, forensic relationship graph analysis, and an AI Compliance Advisor grounded in Reserve Bank of India (RBI) directives and statutory laws.

---

## 1. Core Modules

| Module | Description |
| :--- | :--- |
| **Overview & Accounts** | Account profiles with risk ratings, saved devices, spend habits, and rapid freeze/review actions. |
| **Live Transactions** | Real-time payment stream with latency tracking, risk level filtering, and instant search. |
| **Case Investigation** | Deep investigation dossier with an interactive **Network Graph** (linking Account → Device → Receiver) and 6 safety checks. |
| **Compliance AI** | Grounded regulatory AI assistant powered by **FAISS & BM25 RAG** across RBI Master Directions, PMLA rules, and bank safety standards. |
| **2-Step Authentication** | Secure 2-step sign-in (Password $\rightarrow$ 6-digit Code) with **Fingerprint** and **Face Lock** biometric unlock options. |
| **Jargon-Free Reports** | Exportable, official **PDF Investigation Reports** and **Executive Summaries** written in clear language that anyone can understand. |

---

## 2. Bank Official Credentials

The system operates with a unified Bank Official / Fraud Analyst role (pre-filled on the login screen):

- **Official Email**: `analyst@finsecure.com`
- **Password**: `AnalystPass123!`
- **Step 2 Verification Code**: `123456`
- **Biometric Unlock**: Tap **Fingerprint** or **Face Lock** for instant 1-touch sign-in.

---

## 3. End-to-End System Architecture

```text
┌────────────────────────────────────────────────────────────────────┐
│                   1. Customer Makes Transaction                    │
│                (Fund transfer, payment, UPI, etc.)                 │
└─────────────────────────────────┬──────────────────────────────────┘
                                  │
                                  ▼
┌────────────────────────────────────────────────────────────────────┐
│                         2. Transaction API                         │
│         (Receives transaction details from bank / gateway)         │
└─────────────────────────────────┬──────────────────────────────────┘
                                  │
                                  ▼
┌────────────────────────────────────────────────────────────────────┐    ┌──────────────────────────────────────────────┐
│                       3. Feature Extraction                        │    │ 6 Required Safety Signals:                   │
│              (Builds features from multiple signals)               │───►│ 1. Transaction Behaviour (Amount, type)      │
└─────────────────────────────────┬──────────────────────────────────┘    │ 2. Customer History (Past spending average)  │
                                  │                                       │ 3. Device Fingerprint (Hardware ID)          │
                   ┌──────────────┴──────────────┐                        │ 4. Location Patterns (Distance & city)       │
                   ▼                             ▼                        │ 5. Transfer Speed (Velocity windows)         │
┌──────────────────────────────────────┐  ┌──────────────────────────┐    │ 6. Receiver Connections (Syndicate clusters) │
│       4. Model 1: Smart Fraud        │  │  5. Model 2: Behavior    │    └──────────────────────────────────────────────┘
│         (Supervised XGBoost)         │  │   (Isolation Forest)     │
└──────────────────┬───────────────────┘  └─────────────┬────────────┘
                   └──────────────┬─────────────────────┘
                                  │
                                  ▼
┌────────────────────────────────────────────────────────────────────┐
│                        6. Fraud Risk Engine                        │
│            (Combines model results + contextual signals)           │
└─────────────────────────────────┬──────────────────────────────────┘
                                  │
                                  ▼
┌────────────────────────────────────────────────────────────────────┐
│                        7. SHAP Explanation                         │
│          (Clear breakdown of what caused the risk score)           │
└─────────────────────────────────┬──────────────────────────────────┘
                                  │
                                  ▼
┌────────────────────────────────────────────────────────────────────┐
│                         8. Risk Assessment                         │
│            (Determines risk level and recommended action)          │
└─────────────┬──────────────────────┬──────────────────────┬────────┘
              │                      │                      │
              ▼                      ▼                      ▼
┌──────────────────┐   ┌───────────────────┐   ┌───────────────────┐
│ Low Risk (0-30)  │   │Medium Risk (31-70)│   │High Risk (71-100) │
├──────────────────┤   ├───────────────────┤   ├───────────────────┤
│Allow Transaction │   │  Flag for Review  │   │  Stop Transaction │
│• Tx continues    │   │• Temporary hold   │   │• Block transfer   │
│• Log result      │   │• Verify customer  │   │• Open case report │
└──────────────────┘   └─────────┬─────────┘   └─────────┬─────────┘
                                 └──────────┬────────────┘
                                            │
                                            ▼
                             ┌──────────────────────────────┐
                             │ 9. Fraud Investigation (RAG) │
                             │ • FAISS: RBI | Rules | Cases │
                             │ • Report: Reason / Evidence  │
                             └──────────────┬───────────────┘
                                            │
                                            ▼
                             ┌──────────────────────────────┐
                             │ 10. Case Report & Sign-off   │
                             │ • Jargon-free investigation  │
                             │ • Official PDF report export │
                             └──────────────────────────────┘
```

### The 10-Step Pipeline Explained:
1. **Transaction Ingestion**: Payment telemetry is received in real-time.
2. **Transaction API**: High-speed validation and schema checking via FastAPI.
3. **Feature Extraction**: Computes the **6 Safety Signals** (Amount, History, Device, Location, Speed, Receiver).
4. **Model 1 (XGBoost)**: Supervised fraud probability inference.
5. **Model 2 (Isolation Forest)**: Unsupervised behavioral anomaly detection.
6. **Fraud Risk Engine**: Synthesizes a composite **Risk Score (0–100)**.
7. **SHAP Explanation**: Computes key drivers (e.g. amount 5× higher, new device, impossible distance).
8. **Risk Assessment**: Categorizes the payment into **Low Risk** (Allow), **Medium Risk** (Hold & Review), or **High Risk** (Block & Case Report).
9. **Fraud Investigation (RAG)**: Dense vector search queries statutory documents across **RBI Directives**, **Bank Safety Rules**, and **Past Precedents**.
10. **Case Report & Sign-off**: Generates an everyday-language **Payment Safety & Investigation Report** with exportable PDF formatting.

---

## 4. Regulatory Knowledge Base

The Compliance AI assistant answers regulatory and operational inquiries grounded in statutory documents indexed into semantic chunks:

- **RBI Directives**: Fraud Risk Management Directions 2024, Master Direction on KYC (2016/2025), Digital Payment Security Controls, Credit & Debit Card Directions 2022.
- **PMLA Compliance**: Prevention of Money-Laundering Act 2002, Authentication of Records Outside India Rules 2005, FIU-IND Reporting Standards.
- **Internal Safety Rules**: DemoBank Transaction Rules (BM-001 to BM-010), Account Takeover (ATO) Protocols, and Historical Cases (CASE-001 to CASE-006).

---

## 5. Quick Start & Setup

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### 1. Backend (FastAPI + ML Engine)
```powershell
# In project root:
$env:PYTHONPATH='backend;.'
.\venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```
- **Backend API**: `http://127.0.0.1:8000`
- **Swagger Interactive Docs**: `http://127.0.0.1:8000/docs`

### 2. Frontend (React 18 + Vite)
```powershell
cd frontend
npm install
npm run dev -- --host 127.0.0.1
```
- **Web Application**: `http://127.0.0.1:5173`

---

## 6. Verification & Automated Tests

```powershell
# 1. Run unit & integration test suite (13/13 passing)
$env:PYTHONPATH='backend;.'
.\venv\Scripts\python.exe -m pytest tests/test_core_system.py -v

# 2. Run end-to-end live flow verification
.\venv\Scripts\python.exe tests/verify_live_flow.py

# 3. Production build test for frontend
cd frontend
npm run build
```

---

## 7. Project Structure

```text
fraud-detection-system/
├── backend/
│   ├── app/
│   │   ├── audit/               # Immutable audit logging service
│   │   ├── fraud_engine/        # Dual ML engine & SHAP explainer
│   │   ├── models/              # SQLAlchemy database models
│   │   ├── network_analysis/    # NetworkX entity graph builder
│   │   ├── rag/                 # FAISS vector retriever & AI assistant
│   │   ├── routers/             # FastAPI REST endpoints
│   │   ├── security/            # JWT auth, 2FA, RBAC, and rate limiting
│   │   └── main.py              # Application entrypoint
│   └── data/                    # Seed data & SQLite fallback database
├── frontend/
│   ├── src/
│   │   ├── components/          # Reusable UI components & navigation
│   │   ├── context/             # AuthContext & ThemeContext
│   │   ├── pages/               # Dashboard, LiveStream, Investigation, AI
│   │   └── services/            # Axios client & jsPDF report generator
│   ├── package.json
│   └── vite.config.js
├── ml/
│   ├── feature_engineering/     # 6 Safety signals extractor
│   └── models/                  # Trained model artifacts & scalers
├── rag_documents/               # Indexed RBI, PMLA, & Bank Rule markdown files
├── tests/                       # Pytest test suite & verification scripts
└── README.md                    # System documentation
```

---

## 8. License
FinSecure Sentinel Enterprise Banking FRMS is proprietary software licensed for internal banking operations and regulatory compliance auditing.
