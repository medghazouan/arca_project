<div align="center">

<img src="https://img.shields.io/badge/ARCA-Agile%20Regulatory%20Compliance%20Agent-0066CC?style=for-the-badge" alt="ARCA"/>

<br/>

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Node.js 18+](https://img.shields.io/badge/Node.js-18+-339933?style=flat-square&logo=node.js&logoColor=white)](https://nodejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.6-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React 19](https://img.shields.io/badge/React-19.2-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-F7B731?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-2ECC71?style=flat-square)]()

<br/>

**Analyze new regulations against internal policies in minutes, not weeks.**

ARCA is an AI-powered multi-agent system that automates compliance gap analysis — identifying conflicts, assessing risk levels, and generating actionable recommendations at scale.

[Quick Start](#-quick-start) · [Documentation](#-documentation) · [API Reference](#-api-reference) · [Report a Bug](https://github.com/medghazouan/arca_project/issues)

</div>

---

## Overview

Regulatory compliance reviews are slow, expensive, and error-prone when done manually. ARCA eliminates this bottleneck by orchestrating three specialized AI agents that work in sequence to deliver structured compliance analysis in **under 10 seconds**.

| Without ARCA | With ARCA |
|---|---|
| Manual legal review: 2–3 weeks | Automated analysis: 3–8 seconds |
| Inconsistent coverage | Comprehensive semantic search across all policies |
| Ad-hoc prioritization | Structured severity classification (HIGH / MEDIUM / LOW) |
| No audit trail | Persistent JSON reports with full traceability |

---

## How It Works

```
Input (Text or PDF)
        │
        ▼
┌───────────────────┐
│  Policy Researcher │  Semantic search over FAISS vector store → Top 5 relevant policies
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ Compliance Auditor │  LLM-powered conflict detection → Severity classification
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Report Generator  │  Structured JSON output → Recommendations + risk summary
└───────────────────┘
```

**Agent 1 — Policy Researcher:** Converts the incoming regulation into embeddings and retrieves the most semantically relevant internal policies from a FAISS vector store.

**Agent 2 — Compliance Auditor:** Passes the regulation and retrieved policies to a Gemini LLM to identify direct conflicts, gaps, and ambiguities — each tagged with a severity level.

**Agent 3 — Report Generator:** Formats findings into a structured JSON report including an executive summary, section-level policy mappings, and prioritized remediation steps.

---

## Features

- **Multi-agent orchestration** via LangChain — modular, extensible pipeline
- **Semantic policy retrieval** using FAISS + Sentence-Transformers
- **LLM-powered analysis** via Google Gemini 2.5 Flash
- **Risk classification** at three severity levels: HIGH, MEDIUM, LOW
- **File upload support** — accepts PDF and plain text regulation documents
- **REST API** with auto-generated interactive docs (`/docs`)
- **React frontend** with real-time feedback, Tailwind CSS, and Three.js visualizations
- **Docker support** for one-command deployment

---

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- Google Gemini API key — [get one free here](https://aistudio.google.com/apikey)

### 1. Clone the repository

```bash
git clone https://github.com/medghazouan/arca_project.git
cd arca_project
```

### 2. Set up the backend

```bash
cd arca

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
echo "GOOGLE_API_KEY=your_api_key_here" > .env

# Initialize the vector store
python ingest.py

# Start the API server
python api.py
```

Backend running at **http://localhost:8000** · API docs at **http://localhost:8000/docs**

### 3. Set up the frontend

```bash
# In a new terminal
cd arca_interface
npm install
npm run dev
```

Frontend running at **http://localhost:5173**

### 4. Run your first analysis

```bash
curl -X POST http://localhost:8000/analyze_regulation \
  -H "Content-Type: application/json" \
  -d '{
    "new_regulation_text": "All employees must use multi-factor authentication for system access.",
    "regulation_title": "MFA Mandate 2026"
  }'
```

---

## API Reference

### Analyze a regulation (text)

```bash
POST /analyze_regulation
Content-Type: application/json

{
  "new_regulation_text": "Employee data must be encrypted at rest and in transit.",
  "regulation_title": "Data Protection Regulation 2026",
  "date_of_law": "2026-04-01"
}
```

### Analyze a regulation (file upload)

```bash
POST /analyze_regulation_file

-F "file=@regulation.pdf"
-F "regulation_title=Security Policy Update"
-F "date_of_law=2026-03-01"
```

### Health check

```bash
GET /health

# Response
{
  "status": "healthy",
  "agents_ready": true,
  "timestamp": "2026-02-28T12:15:30.123Z"
}
```

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for the full reference.

---

## Configuration

**Backend** — `arca/.env`

```env
GOOGLE_API_KEY=your_api_key_here   # Required

API_HOST=0.0.0.0                   # Optional
API_PORT=8000                      # Optional
LOG_LEVEL=INFO                     # Optional
```

**Frontend** — `arca_interface/.env.local`

```env
VITE_API_URL=http://localhost:8000
VITE_DEBUG=false
```

---

## Docker Deployment

```bash
# Build and start all services
docker-compose up -d

# Stream logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Tear down
docker-compose down
```

For cloud deployment (Azure, AWS, GCP, Heroku), see [DEPLOYMENT.md](DEPLOYMENT.md).

---

## Performance

| Operation | Typical Duration |
|---|---|
| Health check | 10–50 ms |
| System startup | 2–5 s (one-time) |
| Policy search | 200–800 ms |
| Text analysis (1,000 words) | 3–6 s |
| Report generation | 500–2,000 ms |
| **Full end-to-end** | **3–8 seconds** |

---

## Project Structure

```
arca_project/
├── arca/                          # Backend (Python / FastAPI)
│   ├── api.py                     # API server entry point
│   ├── arca_pipeline.py           # Agent orchestration
│   ├── document_processor.py      # PDF / TXT extraction
│   ├── ingest.py                  # Vector store initialization
│   ├── requirements.txt
│   ├── agents/
│   │   ├── policy_researcher.py   # Agent 1: semantic retrieval
│   │   ├── compliance_auditor.py  # Agent 2: conflict detection
│   │   └── report_generator.py    # Agent 3: report formatting
│   ├── data/policies/             # Internal policy documents
│   ├── vectorstore/               # FAISS index
│   └── reports/                   # Generated analysis reports
│
├── arca_interface/                # Frontend (React / Vite)
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   ├── pages/
│   │   └── lib/
│   ├── package.json
│   └── vite.config.js
│
└── docs/
    ├── ARCHITECTURE.md
    ├── API_DOCUMENTATION.md
    ├── AGENTS_GUIDE.md
    ├── BACKEND_SETUP.md
    ├── FRONTEND_SETUP.md
    ├── DEPLOYMENT.md
    ├── TROUBLESHOOTING.md
    └── CONTRIBUTING.md
```

---

## Documentation

| Document | Description |
|---|---|
| [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) | High-level system overview |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System design and data flow |
| [BACKEND_SETUP.md](BACKEND_SETUP.md) | Backend installation and configuration |
| [FRONTEND_SETUP.md](FRONTEND_SETUP.md) | Frontend installation and configuration |
| [API_DOCUMENTATION.md](API_DOCUMENTATION.md) | Full REST API reference |
| [AGENTS_GUIDE.md](AGENTS_GUIDE.md) | Deep dive into the agent pipeline |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Production and cloud deployment |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Common issues and solutions |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guidelines |

---

## Tech Stack

| Layer | Technology |
|---|---|
| API Framework | FastAPI + Uvicorn |
| LLM | Google Gemini 2.5 Flash |
| Vector Store | FAISS |
| Embeddings | Sentence-Transformers |
| Orchestration | LangChain |
| Frontend | React 19 + Vite |
| Styling | Tailwind CSS 4 |
| 3D Visuals | Three.js |
| Containerization | Docker + Docker Compose |

---

## Roadmap

- [x] Three-agent pipeline
- [x] REST API with file upload
- [x] React frontend
- [x] Docker support
- [ ] Async analysis with webhooks
- [ ] Batch regulation processing
- [ ] User authentication and RBAC
- [ ] PDF / Word report export
- [ ] Historical comparison view
- [ ] Multi-language support

---

## Contributing

Contributions are welcome. Please follow standard GitHub flow:

1. Fork the repository
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "feat: describe your change"`
4. Push and open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## License

Distributed under the [MIT License](LICENSE).

---

<div align="center">

Built by [Medghaz Ouan](https://github.com/medghazouan) · [Open an Issue](https://github.com/medghazouan/arca_project/issues) · [Start a Discussion](https://github.com/medghazouan/arca_project/discussions)

</div>