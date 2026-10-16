<div align="center">

<img src="./static/image/MiroFish_logo_compressed.jpeg" alt="CampusPulse AI Banner" width="85%"/>

### CampusPulse AI — Multimodal Campus Notice-to-Action & Swarm Decision Intelligence

*Turn confusing campus posters, circulars, and notices into verified actionable checklists with Google Gemma 4 — backed by a multi-agent swarm intelligence sandbox.*

[![MLH Hacktoberfest Hack Day](https://img.shields.io/badge/MLH-Hacktoberfest_Hack_Day_Gwalior_2026-F65314?style=for-the-badge&logo=majorleaguehacking&logoColor=white)](https://www.mlh.com/)
[![Best Use of Gemma 4](https://img.shields.io/badge/Track-Best_Use_of_Gemma_4-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/gemma)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Vue 3](https://img.shields.io/badge/Vue-3.5-4FC08D?style=flat-square&logo=vue.js&logoColor=white)](https://vuejs.org/)
[![Vite](https://img.shields.io/badge/Vite-5.0-646CFF?style=flat-square&logo=vite&logoColor=white)](https://vitejs.dev/)
[![Docker Ready](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)
[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg?style=flat-square)](https://www.gnu.org/licenses/agpl-3.0.html)

[English](./README.md) | [中文说明](./README-ZH.md) | [Gemma 4 Assessment & Architecture](./Docs/GEMMA4_ASSESSMENT.md)

</div>

---

## ⚡ Overview

**CampusPulse AI** is a decision intelligence platform designed to eliminate information overload and ambiguity across university campuses. Built for the **MLH Hacktoberfest Hack Day Gwalior x ITM University** hackathon under the **Best Use of Gemma 4** challenge, CampusPulse AI bridges the gap between dense visual announcements and student action through two powerful, complementary systems:

1. **Notice-to-Action Intelligence (Primary Feature — Best Use of Gemma 4)**:  
   Students constantly encounter complex event posters, club notices, hackathon flyers, examination schedules, and scholarship circulars with fragmented dates, eligibility conditions, and obscure registration instructions. Using the official Google GenAI SDK and hosted Gemma 4 models (`gemma-4-26b-a4b-it` and `gemma-4-31b-it`), CampusPulse AI reads image notices directly, accurately extracts structured fields, explicitly highlights missing or ambiguous details, and produces an instant, prioritized student action plan with calendar integration.

2. **Campus Reaction Sandbox (Multi-Agent Swarm Intelligence)**:  
   University administrators and student leaders can test the collective impact of campus policy changes, fee revisions, or event schedules before rolling them out. Powered by OASIS multi-agent simulation and GraphRAG knowledge graph memory, the sandbox models hundreds of diverse student personas interacting and evolving over simulated days to surface feedback and friction points early.

---

## 🎯 Key Capabilities

| Capability | Powered By | What It Does |
|---|---|---|
| **Multimodal Notice Extraction** | Google Gemma 4 (`gemma-4-26b-a4b-it`) | Parses PNG/JPG screenshots of event posters, exam schedules, and circulars directly into structured JSON. |
| **Zero-Hallucination Uncertainty Flagging** | Prompt Engineering & Schema Validation | Distinguishes verified facts from unstated or ambiguous information (e.g., missing venues, conflicting deadlines). |
| **Instant Action Checklist** | Frontend Action Engine | Generates chronologically ordered, priority-tagged steps with one-click Google Calendar export links. |
| **Multimodal Comparison UI** | Vue 3 Reactive Components | Side-by-side inspection of the original notice screenshot alongside extracted parameters and evidence snippets. |
| **Campus Swarm Simulation** | OASIS + GraphRAG (Zep Cloud) | Simulates student body sentiment, discussions, and emergent reactions across digital campus channels. |
| **Decision Intelligence Reports** | ReportAgent with Deep Attribution | Automatically synthesizes simulation metrics into executive summaries, friction analysis, and policy recommendations. |

---

## 📸 System Screenshots

<div align="center">
<table>
<tr>
<td><img src="./static/image/Screenshot/screenshot-1.png" alt="CampusPulse AI Home" width="100%"/></td>
<td><img src="./static/image/Screenshot/screenshot-2.png" alt="Graph Relationship Visualization" width="100%"/></td>
</tr>
<tr>
<td><img src="./static/image/Screenshot/screenshot-3.png" alt="Environment Setup & Persona Generation" width="100%"/></td>
<td><img src="./static/image/Screenshot/screenshot-4.png" alt="Dual-Platform Simulation" width="100%"/></td>
</tr>
<tr>
<td><img src="./static/image/Screenshot/screenshot-5.png" alt="Comprehensive Prediction Report" width="100%"/></td>
<td><img src="./static/image/Screenshot/screenshot-6.png" alt="Deep Agent Interaction" width="100%"/></td>
</tr>
</table>
</div>

---

## 🎬 Demo Showcase

### 1. Campus Notice-to-Action Intelligence (Gemma 4 Multimodal Demo)

<div align="center">
<img src="./static/image/wuhan-university-simulation-cover.png" alt="CampusPulse AI Notice-to-Action Demo" width="80%"/>

*Instant visual notice extraction and action checklist generation powered by Google Gemma 4 via Gemini API.*
</div>

### 2. Multi-Agent Campus Swarm Simulation & Policy Sandbox

<div align="center">
<img src="./static/image/red-chamber-simulation-cover.jpg" alt="Campus Swarm Simulation Demo" width="80%"/>

*High-fidelity multi-agent simulation predicting student community sentiment, event turnout, and policy response.*
</div>

---

## 🧠 Gemma 4 Multimodal Architecture

CampusPulse AI leverages Google's **Gemma 4** open-weight model family through the official **Google GenAI SDK** (`google-genai`):

```
       [ Campus Notice Image (PNG / JPG) ]
                       │
                       ▼
         [ Flask Backend Validation ]
         (MIME check, 10MB limit, base64 payload)
                       │
                       ▼
       [ Google GenAI Client / Gemini API ]
             Model: gemma-4-26b-a4b-it
                       │
                       ▼
     [ Strict Structured Schema Parsing ]
     ├── Title & Category (event, policy, exam, scholarship)
     ├── Critical Timestamps (event date, registration deadline)
     ├── Logistics (venue, eligibility, team size, prerequisites)
     ├── Links & Contacts (registration URL, helpline, email)
     ├── Missing / Ambiguous Fields (explicitly flagged)
     └── Priority Action Items (action, deadline, evidence)
                       │
                       ▼
        [ Vue 3 Notice-to-Action UI ]
    (Side-by-side view, calendar links, fallback modes)
```

### Notice Extraction Schema

```json
{
  "notice_title": "string or null",
  "notice_type": "event | policy | exam | scholarship | other",
  "event_date": "string or null",
  "registration_deadline": "string or null",
  "time": "string or null",
  "venue": "string or null",
  "eligibility": ["string"],
  "team_size": "string or null",
  "required_documents": ["string"],
  "registration_url": "string or null",
  "contact_details": ["string"],
  "action_items": [
    {
      "action": "string",
      "priority": "high | medium | low",
      "deadline": "string or null",
      "evidence": "source excerpt or null"
    }
  ],
  "missing_or_ambiguous": ["string"],
  "plain_language_summary": "string",
  "verification_note": "AI-extracted details should be checked against the original notice"
}
```

---

## 🚀 Quick Start Guide

### Prerequisites

| Tool | Recommended Version | Purpose | Command to Check |
|---|---|---|---|
| **Node.js** | 18+ (tested on Node 20/22) | Frontend build & dev server | `node -v` |
| **Python** | 3.11+ | Backend runtime & LLM services | `python --version` |
| **uv** | Latest | Ultra-fast Python package manager | `uv --version` |
| **Docker** (optional) | 24+ with Compose v2.24+ | Containerized local deployment | `docker compose version` |

---

### Step 1: Clone Repository & Configure Environment

```bash
git clone https://github.com/SKYGOD07/Test_Forge.git
cd Test_Forge

# Copy environment template
cp .env.example .env
```

Edit `.env` and provide your API keys:

```env
# =================================================================
# Google Gemma 4 (Gemini API) - REQUIRED for Notice-to-Action
# =================================================================
GEMINI_API_KEY=your_gemini_api_key_here
GEMMA_MODEL_NAME=gemma-4-26b-a4b-it

# =================================================================
# Optional: Multi-Agent Simulation & Zep Cloud Memory
# =================================================================
LLM_API_KEY=your_openai_compatible_api_key
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL_NAME=qwen-plus
ZEP_API_KEY=your_zep_api_key
```

> **Note on Gemma 4**: Obtain a free API key from [Google AI Studio](https://aistudio.google.com/). The default recommended model is `gemma-4-26b-a4b-it`, with automatic fallback to `gemma-4-31b-it`.

---

### Step 2: Install Dependencies

Using `npm` and `uv` for seamless installation:

```bash
# One-click install (root, frontend, and backend)
npm run setup:all
```

Or install individually:

```bash
# Install frontend dependencies
npm run setup

# Install backend dependencies in virtual environment
npm run setup:backend
```

---

### Step 3: Run the Application

```bash
# Launch both frontend and backend concurrently
npm run dev
```

- **Frontend Application**: [http://localhost:3000](http://localhost:3000)
- **Backend API Server**: [http://localhost:5001](http://localhost:5001)
- **Health Check**: [http://localhost:5001/health](http://localhost:5001/health)

To run services individually:

```bash
npm run frontend   # Starts Vite dev server (Port 3000)
npm run backend    # Starts Flask server (Port 5001)
```

---

### Step 4: Docker Deployment (Alternative)

Run the entire application in an isolated Docker container:

```bash
# Build and start container
docker compose up -d --build

# Inspect logs
docker compose logs -f campuspulse

# Stop container
docker compose down
```

The application will be available at [http://localhost:3000](http://localhost:3000).

---

## 🧪 Testing Gemma 4 Connectivity

Validate your Gemini API key and Gemma 4 model support directly with our diagnostic script:

```bash
cd backend
python test_gemma.py
```

Expected output:
```
Key present: True
--- Testing model: gemma-4-26b-a4b-it ---
SUCCESS with gemma-4-26b-a4b-it:
CampusPulse AI is a decision intelligence platform that turns campus announcements into structured student actions...
```

---

## 📂 Project Structure

```
├── .github/                      # CI/CD workflows and star history
├── backend/                      # Python backend
│   ├── app/
│   │   ├── api/                  # REST endpoints (graph, simulation, report)
│   │   ├── models/               # Data models and schemas
│   │   ├── services/             # Notice extraction, OASIS generator, graph memory
│   │   └── utils/                # GenAI client, retry logic, ontology helpers
│   ├── pyproject.toml            # Backend dependencies (google-genai, flask, camel-oasis)
│   ├── run.py                    # Flask application entry point
│   └── test_gemma.py             # Gemma 4 verification script
├── Docs/
│   └── GEMMA4_ASSESSMENT.md      # Detailed architecture assessment & Hack Day roadmap
├── frontend/                     # Vue 3 + Vite frontend
│   ├── public/
│   │   ├── icon.png              # High-res CampusPulse AI app icon
│   │   └── logo.svg              # CampusPulse brand vector logo
│   ├── src/
│   │   ├── assets/logo/          # Logo banners and hero emblems
│   │   ├── components/
│   │   │   ├── NoticeToAction.vue # Primary Gemma 4 multimodal notice analyzer
│   │   │   ├── GraphPanel.vue     # Knowledge graph interactive visualization
│   │   │   └── Step1-Step5.vue    # Multi-agent simulation step components
│   │   └── views/
│   │       ├── Home.vue           # Unified interface (Notice-to-Action & Sandbox tabs)
│   │       └── Process.vue        # Simulation workflow management
├── locales/                      # Internationalization strings (en.json)
├── static/image/                 # Screenshots, covers, and promotional assets
├── docker-compose.yml            # Docker container orchestration
├── Dockerfile                    # Multi-stage container specification
└── README.md                     # Project documentation
```

---

## 📜 Acknowledgments & Attribution

- **Hackathon**: Developed for the **MLH Hacktoberfest Hack Day Gwalior x ITM University 2026** under the **Best Use of Gemma 4** prize track.
- **Google Gemma 4**: Powered by Google's open-weight Gemma 4 foundation model via the Google GenAI SDK.
- **Simulation Engine**: Powered by **[OASIS (Open Agent Social Interaction Simulations)](https://github.com/camel-ai/oasis)** by CAMEL-AI.
- **Upstream Foundation**: Derived from the open-source **[MiroFish](https://github.com/666ghj/MiroFish)** multi-agent simulation project by 666ghj. We extend sincere appreciation to the upstream contributors.

---

## ⚖️ License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**. See the [LICENSE](./LICENSE) file for complete details.
