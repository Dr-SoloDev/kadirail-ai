# 🚂 KadiRail AI — Multi-Agent Legal Navigation System

> Transform complex Thai legal cases into clear, actionable navigation maps — powered by AI agents on AMD GPUs.

**AMD Developer Hackathon 2026 — Track 1: AI Agents & Agentic Workflows**

**Team: NovaPulse**

---

## 🎯 Problem

Navigating the Thai legal system is overwhelming for ordinary citizens. Understanding a labor dispute case takes **~120 minutes** of reading dense legal documents, researching precedents, and figuring out the process. Most people give up or make uninformed decisions.

## 💡 Solution

KadiRail AI uses **5 specialized AI agents** running on **AMD Instinct MI300X** GPUs to analyze Thai legal cases end-to-end in **under 5 minutes** — a **96% reduction** in case understanding time.

The system transforms legal procedures into an interactive "train station" map, making the legal journey as intuitive as navigating a railway system.

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│           OrchestratorAgent              │
│         (Workflow Coordinator)           │
└────────┬──────┬──────┬──────┬───────────┘
         │      │      │      │
┌────────▼──┐ ┌─▼────┐ ┌▼─────┐ ┌▼────────┐
│  Legal    │ │ Case │ │ Case │ │  Bias   │
│ Analysis  │ │Strat.│ │ Law  │ │  Audit  │
│  Agent    │ │Agent │ │Agent │ │  Agent  │
└─────┬─────┘ └──┬───┘ └──┬───┘ └────┬────┘
      │          │        │           │
┌─────▼──────────▼────────▼───────────▼────┐
│              LLM Service                  │
│        (OpenAI-compatible API)            │
└──────────────────┬───────────────────────┘
                   │
┌──────────────────▼───────────────────────┐
│     vLLM + ROCm on AMD MI300X            │
│     (AMD Developer Cloud)                │
└──────────────────────────────────────────┘
```

### Agents

| Agent | Responsibility |
|-------|---------------|
| 🔍 **LegalAnalysisAgent** | Document analysis, case classification, entity extraction, risk assessment |
| 🗺️ **CaseStrategyAgent** | What-If simulation, timeline/cost estimation, case map generation |
| ⚖️ **BiasAuditAgent** | Bias detection (gender, age, nationality), PII masking, fairness scoring |
| 📚 **CaseLawAgent** | Case law search, document summarization, legal report generation |
| 🎯 **OrchestratorAgent** | Coordinates all agents in optimal workflow, manages pipeline execution |

### Workflow

1. **Document Input** → User uploads/pastes a legal document
2. **LegalAnalysisAgent** → Classifies case type, extracts entities, assesses risk
3. **Parallel Processing** → CaseStrategy + CaseLaw + BiasAudit run on extracted data
4. **OrchestratorAgent** → Combines results into a unified case navigation map
5. **Output** → Interactive dashboard with maps, simulations, and recommendations

## ⚡ Tech Stack

| Component | Technology |
|-----------|-----------|
| **GPU** | AMD Instinct MI300X (192GB VRAM) |
| **Runtime** | ROCm 6.x |
| **LLM Serving** | vLLM (OpenAI-compatible API) |
| **LLM Model** | Qwen2-7B-Instruct (open-source) |
| **Backend** | Python 3.11+ |
| **Frontend** | Streamlit |
| **NLP** | PyThaiNLP (Thai language processing) |
| **Cloud** | AMD Developer Cloud |

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- AMD Developer Cloud instance with MI300X GPU (or any vLLM endpoint)

### 1. Clone & Install

```bash
git clone https://github.com/Dr-SoloDev/kadirail-ai.git
cd kadirail-ai
pip install -r requirements.txt
```

### 2. Start vLLM on AMD Developer Cloud

```bash
# SSH into your AMD Developer Cloud instance
vllm serve Qwen/Qwen2-7B-Instruct --host 0.0.0.0 --port 8000
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env and set LLM_BASE_URL=http://<YOUR_VM_IP>:8000/v1
```

### 4. Run the App

```bash
streamlit run streamlit_app.py
```

## 📋 Features

- **Full Case Analysis** — One-click analysis using all 5 agents
- **Case Map** — Visual railway-style legal process map
- **What-If Simulator** — Simulate different legal strategies
- **Bias Audit** — Detect bias in legal documents (gender, age, nationality)
- **PII Masking** — Protect personal information before sharing
- **Case Law Search** — Find relevant Thai court precedents
- **Document Summary** — AI-powered legal document summarization
- **Agent Dashboard** — Monitor agent status and execution logs

## 📊 Supported Case Types

| Type | Thai | Description |
|------|------|-------------|
| `wage_theft` | โกงค่าจ้าง | Unpaid or underpaid wages |
| `unfair_termination` | เลิกจ้างไม่เป็นธรรม | Wrongful dismissal |
| `bonus_dispute` | ไม่จ่ายโบนัส | Withheld bonus payments |

## 🏆 AMD GPU Usage

KadiRail AI leverages AMD hardware throughout:

- **vLLM** serves the open-source LLM on **AMD Instinct MI300X** via **ROCm**
- **192GB HBM3** enables large model inference (supports up to 72B parameter models)
- **OpenAI-compatible API** means zero vendor lock-in — any open-source model works
- All inference happens on AMD GPU — no external API calls to OpenAI/Anthropic

## 📁 Project Structure

```
kadirail-ai/
├── agents/                  # Multi-agent system
│   ├── base_agent.py       # Abstract base agent class
│   ├── legal_analysis_agent.py
│   ├── case_strategy_agent.py
│   ├── bias_audit_agent.py
│   ├── case_law_agent.py
│   └── orchestrator.py     # Agent coordinator
├── services/
│   └── llm_service.py      # vLLM/OpenAI-compatible client
├── app/
│   └── main.py             # Streamlit application
├── core/                    # Legacy modules (preserved)
├── utils/                   # Utility functions
├── streamlit_app.py         # Entry point
├── requirements.txt
└── .env.example
```

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- **AMD** — Developer Cloud credits and MI300X GPU access
- **lablab.ai** — Hackathon platform and community
- **vLLM** — High-performance LLM serving with ROCm support
- **Qwen Team** — Qwen2-7B-Instruct open-source model
