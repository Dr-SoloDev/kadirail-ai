"""
KadiRail AI - Multi-Agent Legal Navigation System
Streamlit Main Application — Redesigned UI
"""

import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from agents.orchestrator import OrchestratorAgent
from services.llm_service import LLMConfig, LLMService, get_llm_service

st.set_page_config(
    page_title="KadiRail AI",
    page_icon="🚂",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Background ── */
.stApp { background: #0f1117; color: #e2e8f0; }
.main .block-container { padding: 2rem 2.5rem 4rem; max-width: 1200px; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #1a1d27 !important;
    border-right: 1px solid #2d3148;
}
section[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
section[data-testid="stSidebar"] .stRadio label { color: #94a3b8 !important; }
section[data-testid="stSidebar"] [aria-checked="true"] + div > p {
    color: #818cf8 !important;
    font-weight: 600;
}

/* ── Cards ── */
.kd-card {
    background: #1e2130;
    border: 1px solid #2d3148;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: border-color .2s;
}
.kd-card:hover { border-color: #6366f1; }

.kd-card-accent {
    background: linear-gradient(135deg, #1e2130 0%, #1a1d2e 100%);
    border: 1px solid #4f46e5;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

/* ── Hero ── */
.kd-hero {
    background: linear-gradient(135deg, #1e1b4b 0%, #1e2130 50%, #0f172a 100%);
    border: 1px solid #3730a3;
    border-radius: 16px;
    padding: 3rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.kd-hero::before {
    content: '';
    position: absolute; top: -60px; right: -60px;
    width: 240px; height: 240px;
    background: radial-gradient(circle, rgba(99,102,241,.25) 0%, transparent 70%);
    pointer-events: none;
}
.kd-hero-title {
    font-size: 2.8rem; font-weight: 700;
    background: linear-gradient(135deg, #818cf8, #c084fc);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    line-height: 1.15; margin: 0 0 .5rem;
}
.kd-hero-sub {
    font-size: 1.15rem; color: #94a3b8; margin: 0 0 1.5rem;
}
.kd-badge {
    display: inline-block;
    background: rgba(99,102,241,.18);
    border: 1px solid rgba(99,102,241,.4);
    color: #a5b4fc;
    border-radius: 999px;
    padding: .25rem .85rem;
    font-size: .78rem;
    font-weight: 600;
    letter-spacing: .03em;
    margin-right: .4rem;
    margin-bottom: .4rem;
}

/* ── Stat tiles ── */
.kd-stat {
    background: #1e2130;
    border: 1px solid #2d3148;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    text-align: center;
}
.kd-stat-value {
    font-size: 2rem; font-weight: 700; color: #818cf8; line-height: 1;
}
.kd-stat-label {
    font-size: .82rem; color: #64748b; margin-top: .35rem; font-weight: 500;
}
.kd-stat-delta {
    font-size: .75rem; color: #4ade80; margin-top: .2rem;
}

/* ── Agent chips ── */
.kd-agent-row {
    display: flex; flex-wrap: wrap; gap: .5rem; margin-top: .75rem;
}
.kd-agent-chip {
    display: inline-flex; align-items: center; gap: .4rem;
    background: #262940; border: 1px solid #3730a3;
    border-radius: 8px; padding: .4rem .8rem;
    font-size: .82rem; color: #a5b4fc; font-weight: 500;
    transition: background .2s;
}
.kd-agent-chip:hover { background: #2e3360; }
.kd-agent-chip.done  { border-color: #059669; color: #34d399; background: #052e16; }
.kd-agent-chip.active { border-color: #7c3aed; color: #c084fc; background: #2e1065; animation: pulse 1.4s infinite; }

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: .65; }
}

/* ── Risk badges ── */
.risk-high   { color: #f87171; font-weight: 700; }
.risk-medium { color: #fbbf24; font-weight: 700; }
.risk-low    { color: #34d399; font-weight: 700; }

/* ── Section title ── */
.kd-section-title {
    font-size: 1.1rem; font-weight: 600;
    color: #e2e8f0; letter-spacing: .01em;
    margin: 1.5rem 0 .75rem;
    display: flex; align-items: center; gap: .45rem;
}

/* ── Result metric row ── */
.kd-metric-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: .75rem;
    margin-bottom: 1.5rem;
}
.kd-metric-box {
    background: #1e2130;
    border: 1px solid #2d3148;
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
}
.kd-metric-label { font-size: .78rem; color: #64748b; font-weight: 500; }
.kd-metric-value { font-size: 1.4rem; font-weight: 700; color: #c7d2fe; margin-top: .25rem; }

/* ── Step rail ── */
.kd-step {
    display: flex; gap: 1rem;
    align-items: flex-start;
    padding: .9rem 1rem;
    border-radius: 10px;
    background: #1e2130;
    border: 1px solid #2d3148;
    margin-bottom: .6rem;
    transition: border-color .2s;
}
.kd-step:hover { border-color: #4f46e5; }
.kd-step-num {
    min-width: 2rem; height: 2rem;
    background: #312e81; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: .82rem; font-weight: 700; color: #a5b4fc;
    flex-shrink: 0;
}
.kd-step-num.risk-high   { background: #450a0a; color: #fca5a5; }
.kd-step-num.risk-medium { background: #451a03; color: #fcd34d; }
.kd-step-num.risk-low    { background: #052e16; color: #6ee7b7; }
.kd-step-body { flex: 1; }
.kd-step-title { font-weight: 600; color: #e2e8f0; font-size: .92rem; }
.kd-step-desc  { color: #94a3b8; font-size: .82rem; margin-top: .2rem; }
.kd-step-meta  { display: flex; gap: .75rem; margin-top: .4rem; }
.kd-step-meta span {
    font-size: .75rem; color: #64748b;
    background: #262940; border-radius: 5px;
    padding: .15rem .5rem;
}

/* ── Law pill ── */
.kd-law-pill {
    display: inline-block;
    background: #1e3a5f; border: 1px solid #1d4ed8;
    color: #93c5fd; border-radius: 6px;
    padding: .2rem .6rem; font-size: .78rem;
    margin: .15rem .2rem;
}

/* ── Tip box ── */
.kd-tip {
    background: #0c1a2e; border-left: 3px solid #3b82f6;
    border-radius: 0 8px 8px 0;
    padding: .6rem 1rem;
    color: #93c5fd; font-size: .83rem;
    margin-top: .5rem;
}

/* ── Case law card ── */
.kd-case-card {
    background: #1e2130; border: 1px solid #2d3148;
    border-radius: 10px; padding: 1.1rem 1.25rem; margin-bottom: .75rem;
}
.kd-case-num  { font-size: .78rem; color: #818cf8; font-weight: 600; }
.kd-case-issue { font-weight: 600; color: #e2e8f0; margin: .25rem 0; }
.kd-case-summary { color: #94a3b8; font-size: .84rem; line-height: 1.55; }
.kd-relevance-bar {
    height: 4px; background: #1e3a5f;
    border-radius: 2px; margin-top: .75rem; overflow: hidden;
}
.kd-relevance-fill {
    height: 100%; background: linear-gradient(90deg, #6366f1, #a78bfa);
    border-radius: 2px;
}

/* ── Bias finding ── */
.kd-bias-finding {
    background: #1e2130; border-radius: 10px;
    padding: 1rem 1.25rem; margin-bottom: .75rem;
    border-left: 3px solid #f59e0b;
}
.kd-bias-finding.high   { border-left-color: #ef4444; }
.kd-bias-finding.medium { border-left-color: #f59e0b; }
.kd-bias-finding.low    { border-left-color: #10b981; }

/* ── Timeline ── */
.kd-timeline { position: relative; padding-left: 1.5rem; }
.kd-timeline::before {
    content: '';
    position: absolute; left: .5rem; top: 0; bottom: 0;
    width: 2px; background: #2d3148;
}
.kd-tl-item {
    position: relative; margin-bottom: 1.25rem;
}
.kd-tl-dot {
    position: absolute; left: -1.5rem;
    width: 1rem; height: 1rem;
    background: #6366f1; border-radius: 50%;
    border: 2px solid #1e2130;
    top: .2rem;
}
.kd-tl-step { font-size: .78rem; color: #818cf8; font-weight: 600; }
.kd-tl-desc { color: #94a3b8; font-size: .85rem; margin-top: .15rem; }
.kd-tl-days {
    display: inline-block;
    background: #262940; color: #a5b4fc;
    border-radius: 5px; padding: .1rem .45rem;
    font-size: .74rem; margin-top: .2rem;
}

/* ── Compensation table ── */
.kd-comp-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: .55rem 0; border-bottom: 1px solid #2d3148;
}
.kd-comp-row:last-child { border-bottom: none; }
.kd-comp-label { color: #94a3b8; font-size: .87rem; }
.kd-comp-amount { color: #c7d2fe; font-weight: 600; font-size: .92rem; }
.kd-comp-total  { color: #34d399; font-weight: 700; font-size: 1.1rem; }

/* ── Sidebar nav ── */
.kd-nav-header {
    font-size: .7rem; font-weight: 700; letter-spacing: .1em;
    color: #475569 !important;
    text-transform: uppercase;
    padding: .4rem .5rem;
    margin-top: .5rem;
}

/* ── Streamlit overrides ── */
.stTextArea textarea, .stTextInput input, .stSelectbox select {
    background: #1e2130 !important;
    border: 1px solid #2d3148 !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 2px rgba(99,102,241,.25) !important;
}
.stButton > button {
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: #fff !important; border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: opacity .2s !important;
}
.stButton > button:hover { opacity: .88 !important; }
.stButton > button[kind="secondary"] {
    background: #1e2130 !important;
    border: 1px solid #2d3148 !important;
    color: #94a3b8 !important;
}
div[data-testid="stTabs"] [role="tab"] {
    color: #64748b !important;
    border-radius: 8px 8px 0 0 !important;
    font-weight: 500 !important;
}
div[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: #a5b4fc !important;
    border-bottom: 2px solid #6366f1 !important;
}
.stExpander { border: 1px solid #2d3148 !important; border-radius: 10px !important; background: #1e2130 !important; }
.stExpander header { color: #e2e8f0 !important; }
.stSuccess { background: #052e16 !important; border: 1px solid #166534 !important; color: #86efac !important; border-radius: 8px !important; }
.stWarning { background: #451a03 !important; border: 1px solid #92400e !important; color: #fde68a !important; border-radius: 8px !important; }
.stError   { background: #450a0a !important; border: 1px solid #991b1b !important; color: #fca5a5 !important; border-radius: 8px !important; }
.stInfo    { background: #0c1a2e !important; border: 1px solid #1d4ed8 !important; color: #93c5fd !important; border-radius: 8px !important; }
div[data-testid="metric-container"] {
    background: #1e2130; border: 1px solid #2d3148;
    border-radius: 10px; padding: .75rem 1rem !important;
}
div[data-testid="metric-container"] label { color: #64748b !important; }
div[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #c7d2fe !important; font-weight: 700 !important; }
</style>
""", unsafe_allow_html=True)


# ─── Helpers ───────────────────────────────────────────────────────────────────

def _fmt_thb(amount) -> str:
    try:
        return f"฿{int(amount):,}"
    except Exception:
        return str(amount)


def _risk_class(risk: str) -> str:
    return {"high": "risk-high", "medium": "risk-medium", "low": "risk-low"}.get(risk, "")


def _risk_icon(risk: str) -> str:
    return {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(risk, "⚪")


# ─── Session init ──────────────────────────────────────────────────────────────

def init_session():
    if "orchestrator" not in st.session_state:
        st.session_state.orchestrator = OrchestratorAgent()
    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = None
    if "llm_status" not in st.session_state:
        st.session_state.llm_status = None


# ─── Sidebar ──────────────────────────────────────────────────────────────────

def sidebar() -> str:
    with st.sidebar:
        st.markdown("""
        <div style="padding:.5rem 0 1rem">
            <div style="font-size:1.5rem;font-weight:700;color:#a5b4fc;letter-spacing:-.5px">🚂 KadiRail AI</div>
            <div style="font-size:.78rem;color:#475569;margin-top:.2rem">Multi-Agent Legal Navigator</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="kd-nav-header">Main</div>', unsafe_allow_html=True)
        menu = st.radio(
            "nav",
            [
                "🏠  Overview",
                "🔍  Full Analysis",
                "🗺️  Case Map",
                "🔮  What-If Simulator",
                "⚖️  Bias Audit",
                "🔒  PII Masking",
                "📚  Case Law",
                "📝  Summarize",
                "📊  Dashboard",
            ],
            label_visibility="collapsed",
        )

        st.markdown("---")
        st.markdown('<div class="kd-nav-header">LLM Endpoint</div>', unsafe_allow_html=True)

        with st.expander("Configure", expanded=False):
            base_url = st.text_input("vLLM URL", value=os.getenv("LLM_BASE_URL", "http://localhost:8000/v1"), label_visibility="collapsed")
            model = st.text_input("Model", value=os.getenv("LLM_MODEL", "Qwen/Qwen2-7B-Instruct"), label_visibility="collapsed")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Save", use_container_width=True):
                    cfg = LLMConfig(base_url=base_url, model=model)
                    st.session_state.orchestrator = OrchestratorAgent(llm=LLMService(cfg))
                    st.session_state.llm_status = None
                    st.rerun()
            with c2:
                if st.button("Ping", use_container_width=True):
                    h = st.session_state.orchestrator.llm.health_check()
                    st.session_state.llm_status = h

        if st.session_state.llm_status:
            h = st.session_state.llm_status
            if h["status"] == "healthy":
                st.success(f"✅ Connected — {', '.join(h.get('models', []))[:40]}")
            else:
                st.error(f"❌ {h.get('error','Offline')[:60]}")

        st.markdown("---")
        st.markdown('<div class="kd-nav-header">Agents</div>', unsafe_allow_html=True)
        orch = st.session_state.orchestrator
        icons = ["🔍", "🗺️", "⚖️", "📚"]
        for icon, agent in zip(icons, orch.agents):
            tasks = len(agent.history)
            dot = "🟢" if tasks else "⚫"
            st.markdown(
                f'<div style="font-size:.8rem;padding:.25rem .1rem;color:#64748b">'
                f'{dot} {icon} <span style="color:#94a3b8">{agent.name}</span>'
                f'<span style="float:right;color:#475569">{tasks}</span></div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.markdown(
            '<div style="font-size:.72rem;color:#334155;line-height:1.6">'
            '🏆 AMD Dev Hackathon 2026<br>Track 1 · AI Agents<br>'
            '<span style="color:#4f46e5">NovaPulse Team</span></div>',
            unsafe_allow_html=True,
        )

    return menu


# ─── Pages ────────────────────────────────────────────────────────────────────

def page_overview():
    st.markdown("""
    <div class="kd-hero">
        <div class="kd-hero-title">🚂 KadiRail AI</div>
        <div class="kd-hero-sub">
            Transform complex Thai legal cases into clear, actionable navigation maps<br>
            powered by 5 specialized AI agents on AMD Instinct MI300X
        </div>
        <div>
            <span class="kd-badge">AMD MI300X</span>
            <span class="kd-badge">ROCm + vLLM</span>
            <span class="kd-badge">Qwen2-7B</span>
            <span class="kd-badge">Thai Labour Law</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Stat row
    c1, c2, c3, c4 = st.columns(4)
    stats = [
        ("120 min → 5 min", "Case Understanding", "96% faster"),
        ("5", "Specialized Agents", "Parallel pipeline"),
        ("192 GB", "AMD HBM3 VRAM", "MI300X GPU"),
        ("3", "Case Types", "Labour law focus"),
    ]
    for col, (val, label, delta) in zip([c1, c2, c3, c4], stats):
        with col:
            st.markdown(f"""
            <div class="kd-stat">
                <div class="kd-stat-value">{val}</div>
                <div class="kd-stat-label">{label}</div>
                <div class="kd-stat-delta">{delta}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("")

    left, right = st.columns([3, 2])

    with left:
        st.markdown('<div class="kd-section-title">🤖 Agent Pipeline</div>', unsafe_allow_html=True)
        agents = [
            ("🔍", "LegalAnalysisAgent", "Document analysis · Case classification · Risk assessment"),
            ("🗺️", "CaseStrategyAgent", "What-If simulation · Timeline & cost estimation"),
            ("⚖️", "BiasAuditAgent", "Bias detection · PII masking · Fairness scoring"),
            ("📚", "CaseLawAgent", "Precedent search · Document summarization · Report"),
            ("🎯", "OrchestratorAgent", "Coordinates all agents · Manages pipeline execution"),
        ]
        for icon, name, desc in agents:
            st.markdown(f"""
            <div class="kd-card" style="padding:1rem 1.25rem;margin-bottom:.5rem">
                <div style="display:flex;align-items:flex-start;gap:.75rem">
                    <span style="font-size:1.4rem;line-height:1">{icon}</span>
                    <div>
                        <div style="font-weight:600;color:#e2e8f0;font-size:.9rem">{name}</div>
                        <div style="color:#64748b;font-size:.8rem;margin-top:.15rem">{desc}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with right:
        st.markdown('<div class="kd-section-title">⚡ Workflow</div>', unsafe_allow_html=True)
        steps = [
            ("Upload / paste document", "Thai or English"),
            ("LegalAnalysisAgent runs", "Classify · Extract · Risk"),
            ("3 agents run in parallel", "Strategy · CaseLaw · Bias"),
            ("Orchestrator combines", "Unified case map"),
            ("Interactive dashboard", "Maps · Sim · Reports"),
        ]
        st.markdown('<div class="kd-timeline">', unsafe_allow_html=True)
        for title, sub in steps:
            st.markdown(f"""
            <div class="kd-tl-item">
                <div class="kd-tl-dot"></div>
                <div class="kd-tl-step">{title}</div>
                <div class="kd-tl-desc">{sub}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="kd-section-title">⚖️ Case Types</div>', unsafe_allow_html=True)
        for th, en in [("โกงค่าจ้าง", "Unpaid wages"), ("เลิกจ้างไม่เป็นธรรม", "Unfair termination"), ("ไม่จ่ายโบนัส", "Bonus dispute")]:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;padding:.5rem .75rem;
                        background:#1e2130;border:1px solid #2d3148;border-radius:8px;margin-bottom:.4rem">
                <span style="color:#e2e8f0;font-weight:500">{th}</span>
                <span style="color:#64748b;font-size:.83rem">{en}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="text-align:center;padding:1rem 0">
        <div style="font-size:.82rem;color:#475569">
            Powered by <strong style="color:#818cf8">vLLM</strong> ·
            <strong style="color:#818cf8">AMD ROCm</strong> ·
            <strong style="color:#818cf8">PyThaiNLP</strong> ·
            <strong style="color:#818cf8">Streamlit</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)


def page_full_analysis():
    st.markdown('<div class="kd-section-title" style="font-size:1.4rem;margin-top:0">🔍 Full Case Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#64748b;margin-bottom:1.25rem">Paste a legal document — all 5 agents will analyze it in sequence.</div>', unsafe_allow_html=True)

    col_btn, col_demo = st.columns([2, 1])
    with col_demo:
        if st.button("📄 Load Demo Case", use_container_width=True):
            from data.demo_responses import DEMO_CASE_TEXT
            st.session_state["_demo_text"] = DEMO_CASE_TEXT
            st.rerun()

    default_text = st.session_state.get("_demo_text", "")
    text = st.text_area(
        "Legal document",
        value=default_text,
        height=220,
        placeholder="วางเอกสารคดีที่นี่ — รองรับภาษาไทยและอังกฤษ\nPaste your legal document here (Thai or English)...",
        label_visibility="collapsed",
    )

    with col_btn:
        run = st.button("🚀 Run Full Analysis", type="primary", use_container_width=True, disabled=not bool(text))

    if run and text:
        orch = st.session_state.orchestrator

        # Pipeline progress display
        st.markdown('<div class="kd-section-title">🤖 Agent Pipeline</div>', unsafe_allow_html=True)
        cols = st.columns(4)
        chips = {}
        agent_defs = [("🔍", "LegalAnalysis"), ("🗺️", "CaseStrategy"), ("📚", "CaseLaw"), ("⚖️", "BiasAudit")]
        for i, (icon, name) in enumerate(agent_defs):
            with cols[i]:
                chips[name] = st.empty()
                chips[name].markdown(
                    f'<div class="kd-agent-chip">⏳ {icon} {name}</div>',
                    unsafe_allow_html=True,
                )

        chips["LegalAnalysis"].markdown(
            '<div class="kd-agent-chip active">🔄 🔍 LegalAnalysis</div>',
            unsafe_allow_html=True,
        )

        with st.spinner(""):
            result = orch.analyze_case(text)

        for icon, name in agent_defs:
            chips[name].markdown(
                f'<div class="kd-agent-chip done">✅ {icon} {name}</div>',
                unsafe_allow_html=True,
            )

        st.session_state.analysis_result = result
        _render_analysis_result(result)

    elif st.session_state.analysis_result:
        _render_analysis_result(st.session_state.analysis_result)


def _render_analysis_result(result: dict):
    analysis = result.get("results", {}).get("analysis", {}).get("data", {})
    strategy = result.get("results", {}).get("strategy", {}).get("data", {})
    bias     = result.get("results", {}).get("bias", {}).get("data", {})
    case_law = result.get("results", {}).get("case_law", {}).get("data", {})

    st.markdown('<div class="kd-section-title">📊 Summary</div>', unsafe_allow_html=True)

    # Metric row
    risk = analysis.get("risk_level", "unknown")
    st.markdown(f"""
    <div class="kd-metric-row">
        <div class="kd-metric-box">
            <div class="kd-metric-label">Case Type</div>
            <div class="kd-metric-value" style="font-size:1rem">{analysis.get("case_type_thai", analysis.get("case_type","—"))}</div>
        </div>
        <div class="kd-metric-box">
            <div class="kd-metric-label">Risk Level</div>
            <div class="kd-metric-value {_risk_class(risk)}">{_risk_icon(risk)} {risk.upper()}</div>
        </div>
        <div class="kd-metric-box">
            <div class="kd-metric-label">Win Probability</div>
            <div class="kd-metric-value">{strategy.get("win_rate","—")}%</div>
        </div>
        <div class="kd-metric-box">
            <div class="kd-metric-label">Est. Duration</div>
            <div class="kd-metric-value" style="font-size:1rem">{strategy.get("estimated_duration_days","—")} days</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Compensation estimate
    comp = analysis.get("compensation_estimate", {})
    if comp:
        st.markdown('<div class="kd-section-title">💰 Compensation Estimate</div>', unsafe_allow_html=True)
        st.markdown('<div class="kd-card">', unsafe_allow_html=True)
        items = [
            ("Severance Pay", "severance_pay"),
            ("Notice Pay", "notice_pay"),
            ("Unpaid Wages", "unpaid_wages"),
            ("Unpaid Overtime", "unpaid_overtime"),
            ("Unfair Dismissal", "unfair_dismissal"),
        ]
        rows = "".join(
            f'<div class="kd-comp-row"><span class="kd-comp-label">{lbl}</span>'
            f'<span class="kd-comp-amount">{_fmt_thb(comp.get(key, 0))}</span></div>'
            for lbl, key in items if comp.get(key, 0)
        )
        total = comp.get("total_estimate", 0)
        st.markdown(
            f'{rows}<div class="kd-comp-row" style="margin-top:.25rem;padding-top:.75rem;border-top:1px solid #4f46e5">'
            f'<span style="color:#e2e8f0;font-weight:700">Total Estimate</span>'
            f'<span class="kd-comp-total">{_fmt_thb(total)}</span></div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Tabs
    tabs = st.tabs(["📋 Analysis", "🗺️ Strategy", "📚 Case Law", "⚖️ Bias", "📊 Pipeline"])

    with tabs[0]:
        st.markdown(f'<div style="color:#94a3b8;line-height:1.7;margin-bottom:1rem">{analysis.get("summary","")}</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if analysis.get("key_facts"):
                st.markdown('<div class="kd-section-title">Key Facts</div>', unsafe_allow_html=True)
                for f in analysis["key_facts"]:
                    st.markdown(f'<div style="color:#94a3b8;font-size:.86rem;padding:.3rem 0;border-bottom:1px solid #1e2130">• {f}</div>', unsafe_allow_html=True)
        with c2:
            if analysis.get("applicable_laws"):
                st.markdown('<div class="kd-section-title">Applicable Laws</div>', unsafe_allow_html=True)
                for law in analysis["applicable_laws"]:
                    st.markdown(f'<span class="kd-law-pill">{law}</span>', unsafe_allow_html=True)

    with tabs[1]:
        c1, c2 = st.columns([3, 2])
        with c1:
            if strategy.get("timeline"):
                st.markdown('<div class="kd-section-title">Timeline</div>', unsafe_allow_html=True)
                st.markdown('<div class="kd-timeline">', unsafe_allow_html=True)
                for step in strategy["timeline"]:
                    st.markdown(f"""
                    <div class="kd-tl-item">
                        <div class="kd-tl-dot"></div>
                        <div class="kd-tl-step">{step.get("step","")}</div>
                        <div class="kd-tl-desc">{step.get("description","")}</div>
                        <span class="kd-tl-days">⏱ {step.get("duration_days","?")} days</span>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
        with c2:
            if strategy.get("recommendations"):
                st.markdown('<div class="kd-section-title">Recommendations</div>', unsafe_allow_html=True)
                for rec in strategy["recommendations"]:
                    st.markdown(f'<div class="kd-tip">💡 {rec}</div>', unsafe_allow_html=True)
            if strategy.get("best_case"):
                st.markdown('<div class="kd-section-title">Outcomes</div>', unsafe_allow_html=True)
                st.success(f"**Best:** {strategy['best_case']}")
            if strategy.get("worst_case"):
                st.error(f"**Worst:** {strategy['worst_case']}")

    with tabs[2]:
        cases = case_law.get("cases", [])
        if cases:
            for case in cases:
                rel = int(case.get("relevance_score", 0.5) * 100)
                sections = "".join(f'<span class="kd-law-pill">{s}</span>' for s in case.get("applicable_sections", []))
                st.markdown(f"""
                <div class="kd-case-card">
                    <div class="kd-case-num">{case.get("case_number","N/A")} · {case.get("court","N/A")} · {case.get("year","")}</div>
                    <div class="kd-case-issue">{case.get("issue","")}</div>
                    <div class="kd-case-summary">{case.get("summary","")}</div>
                    <div style="margin-top:.5rem;font-size:.8rem;color:#818cf8">⚖️ {case.get("key_principle","")}</div>
                    <div style="margin-top:.5rem">{sections}</div>
                    <div class="kd-relevance-bar"><div class="kd-relevance-fill" style="width:{rel}%"></div></div>
                    <div style="font-size:.72rem;color:#475569;margin-top:.25rem">Relevance: {rel}%</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No case law results.")

    with tabs[3]:
        score = bias.get("bias_score", 0)
        col_s, col_c = st.columns([1, 2])
        with col_s:
            color = "#ef4444" if score > 50 else "#f59e0b" if score > 20 else "#10b981"
            st.markdown(f"""
            <div class="kd-stat" style="border-color:{color}33">
                <div class="kd-stat-value" style="color:{color}">{score:.1f}%</div>
                <div class="kd-stat-label">Bias Score</div>
                <div class="kd-stat-delta" style="color:{color}">{"⚠️ Bias Detected" if score > 30 else "✅ Fair"}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_c:
            cats = bias.get("bias_categories", {})
            if cats:
                for cat, val in cats.items():
                    pct = int(val)
                    st.markdown(f"""
                    <div style="margin-bottom:.5rem">
                        <div style="display:flex;justify-content:space-between;font-size:.8rem;color:#94a3b8;margin-bottom:.2rem">
                            <span>{cat}</span><span>{val:.1f}%</span>
                        </div>
                        <div style="height:6px;background:#2d3148;border-radius:3px;overflow:hidden">
                            <div style="height:100%;width:{pct}%;background:linear-gradient(90deg,#6366f1,#a78bfa);border-radius:3px"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        if bias.get("findings"):
            st.markdown('<div class="kd-section-title">Findings</div>', unsafe_allow_html=True)
            for finding in bias["findings"]:
                sev = finding.get("severity", "low")
                st.markdown(f"""
                <div class="kd-bias-finding {sev}">
                    <div style="font-weight:600;color:#e2e8f0">{_risk_icon(sev)} {finding.get("category","")} <span style="font-size:.75rem;color:#64748b">({sev})</span></div>
                    <div style="color:#94a3b8;font-size:.84rem;margin-top:.3rem">"{finding.get("text","")}"</div>
                    <div style="color:#64748b;font-size:.82rem;margin-top:.25rem">{finding.get("explanation","")}</div>
                    {f'<div class="kd-tip">💡 {finding["suggestion"]}</div>' if finding.get("suggestion") else ""}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ No significant bias detected")

    with tabs[4]:
        elapsed = result.get("execution_time", 0)
        agents_n = result.get("agent_count", 0)
        mode = result.get("mode", "demo")
        st.markdown(f"""
        <div class="kd-metric-row" style="grid-template-columns:repeat(3,1fr)">
            <div class="kd-metric-box"><div class="kd-metric-label">Execution Time</div><div class="kd-metric-value">{elapsed:.2f}s</div></div>
            <div class="kd-metric-box"><div class="kd-metric-label">Agents Used</div><div class="kd-metric-value">{agents_n}</div></div>
            <div class="kd-metric-box"><div class="kd-metric-label">Mode</div><div class="kd-metric-value" style="font-size:1rem;color:{'#34d399' if mode=='live' else '#fbbf24'}">{mode.upper()}</div></div>
        </div>
        """, unsafe_allow_html=True)
        if result.get("execution_log"):
            st.markdown('<div class="kd-section-title">Execution Log</div>', unsafe_allow_html=True)
            for entry in result["execution_log"]:
                st.markdown(f'<div style="font-size:.78rem;color:#475569;padding:.2rem 0;font-family:monospace">▸ {entry["event"]}</div>', unsafe_allow_html=True)


def page_case_map():
    st.markdown('<div class="kd-section-title" style="font-size:1.4rem;margin-top:0">🗺️ Case Map</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#64748b;margin-bottom:1.25rem">Visualize the legal journey as a step-by-step railway map.</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        case_type = st.selectbox("Case Type", ["wage_theft", "unfair_termination", "bonus_dispute"],
                                  format_func=lambda x: {"wage_theft":"โกงค่าจ้าง","unfair_termination":"เลิกจ้างไม่เป็นธรรม","bonus_dispute":"ไม่จ่ายโบนัส"}[x])
    with c2:
        strategy = st.selectbox("Strategy", ["litigation", "mediation", "settlement"],
                                 format_func=lambda x: {"litigation":"ฟ้องศาล","mediation":"ไกล่เกลี่ย","settlement":"ยอมความ"}[x])
    with c3:
        st.markdown("")
        st.markdown("")
        generate = st.button("Generate", type="primary", use_container_width=True)

    if generate:
        orch = st.session_state.orchestrator
        with st.spinner("Generating case map..."):
            result = orch.case_strategy.run({"action": "map", "case_type": case_type, "strategy": strategy})
        data = result.data
        st.session_state["_case_map"] = data

    data = st.session_state.get("_case_map")
    if not data:
        st.info("Select a case type and strategy, then click Generate.")
        return

    steps = data.get("steps", [])
    if not steps:
        st.warning("Could not generate case map — check LLM connection.")
        return

    # Summary bar
    total_days = data.get("total_duration_days", sum(s.get("duration_days", 0) for s in steps))
    total_cost = sum(s.get("cost_thb", 0) for s in steps)
    st.markdown(f"""
    <div class="kd-card-accent" style="display:flex;gap:2rem;align-items:center">
        <div><div class="kd-metric-label">Total Steps</div><div class="kd-metric-value">{len(steps)}</div></div>
        <div><div class="kd-metric-label">Total Duration</div><div class="kd-metric-value">{total_days} days</div></div>
        <div><div class="kd-metric-label">Estimated Cost</div><div class="kd-metric-value">{_fmt_thb(total_cost)}</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="kd-section-title">📍 Steps</div>', unsafe_allow_html=True)
    for step in steps:
        risk = step.get("risk_level", "low")
        docs = "".join(f'<span class="kd-law-pill">{d}</span>' for d in step.get("required_documents", []))
        tip = f'<div class="kd-tip">💡 {step["tips"]}</div>' if step.get("tips") else ""
        st.markdown(f"""
        <div class="kd-step">
            <div class="kd-step-num {risk}">{step.get("step_number","?")}</div>
            <div class="kd-step-body">
                <div class="kd-step-title">🚉 {step.get("title","")}</div>
                <div class="kd-step-desc">{step.get("description","")}</div>
                <div class="kd-step-meta">
                    <span>⏱ {step.get("duration_days","?")} days</span>
                    <span>💰 {_fmt_thb(step.get("cost_thb",0))}</span>
                    <span class="{_risk_class(risk)}">{_risk_icon(risk)} {risk}</span>
                </div>
                <div style="margin-top:.5rem">{docs}</div>
                {tip}
            </div>
        </div>
        """, unsafe_allow_html=True)

    if data.get("mermaid_diagram"):
        with st.expander("📊 Mermaid Diagram"):
            st.code(data["mermaid_diagram"], language="mermaid")


def page_simulator():
    st.markdown('<div class="kd-section-title" style="font-size:1.4rem;margin-top:0">🔮 What-If Simulator</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#64748b;margin-bottom:1.25rem">Simulate different legal strategies and see how outcomes change.</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        case_type = st.selectbox("Case Type", ["wage_theft", "unfair_termination", "bonus_dispute"], key="sim_ct")
    with c2:
        scenario = st.selectbox("Scenario", ["proceed_normally", "settle_early", "go_to_mediation", "full_litigation", "appeal_judgment"],
                                 format_func=lambda x: x.replace("_", " ").title())

    summary = st.text_area("Case Summary", placeholder="Brief description of the case...", height=90)
    key_facts_raw = st.text_area("Key Facts (one per line)", placeholder="Fact 1\nFact 2", height=80)

    if summary and st.button("🔮 Run Simulation", type="primary"):
        orch = st.session_state.orchestrator
        key_facts = [f.strip() for f in key_facts_raw.split("\n") if f.strip()]
        with st.spinner("Simulating..."):
            result = orch.simulate_scenario(case_type, summary, scenario, key_facts)
        data = result.get("data", {})

        # Outcome cards
        st.markdown('<div class="kd-section-title">📊 Outcome</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="kd-metric-row">
            <div class="kd-metric-box">
                <div class="kd-metric-label">Win Probability</div>
                <div class="kd-metric-value">{data.get("win_rate","—")}%</div>
            </div>
            <div class="kd-metric-box">
                <div class="kd-metric-label">Est. Duration</div>
                <div class="kd-metric-value">{data.get("estimated_duration_days","—")} days</div>
            </div>
            <div class="kd-metric-box">
                <div class="kd-metric-label">Est. Cost</div>
                <div class="kd-metric-value" style="font-size:1rem">{_fmt_thb(data.get("estimated_cost_thb",0))}</div>
            </div>
            <div class="kd-metric-box">
                <div class="kd-metric-label">Strategy</div>
                <div class="kd-metric-value" style="font-size:.95rem;color:#a78bfa">{scenario.replace("_"," ").title()}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        lc, rc = st.columns(2)
        with lc:
            if data.get("risks"):
                st.markdown('<div class="kd-section-title">⚠️ Risks</div>', unsafe_allow_html=True)
                for r in data["risks"]:
                    st.markdown(f'<div style="color:#fca5a5;font-size:.85rem;padding:.3rem 0;border-bottom:1px solid #1e2130">⚠ {r}</div>', unsafe_allow_html=True)
        with rc:
            if data.get("recommendations"):
                st.markdown('<div class="kd-section-title">💡 Recommendations</div>', unsafe_allow_html=True)
                for r in data["recommendations"]:
                    st.markdown(f'<div class="kd-tip">{r}</div>', unsafe_allow_html=True)

        if data.get("best_case"):
            st.success(f"🟢 **Best Case:** {data['best_case']}")
        if data.get("worst_case"):
            st.error(f"🔴 **Worst Case:** {data['worst_case']}")


def page_bias_audit():
    st.markdown('<div class="kd-section-title" style="font-size:1.4rem;margin-top:0">⚖️ Bias Audit</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#64748b;margin-bottom:1.25rem">Detect gender, age, nationality and socioeconomic bias in legal texts.</div>', unsafe_allow_html=True)

    text = st.text_area("Text to audit", height=200, placeholder="วางข้อความที่ต้องการตรวจสอบอคติ...")

    if text and st.button("🔍 Run Bias Audit", type="primary"):
        orch = st.session_state.orchestrator
        with st.spinner("Auditing..."):
            result = orch.audit_bias(text)
        data = result.get("data", {})

        score = data.get("bias_score", 0)
        color = "#ef4444" if score > 50 else "#f59e0b" if score > 20 else "#10b981"
        cats = data.get("bias_categories", {})

        lc, rc = st.columns([1, 2])
        with lc:
            st.markdown(f"""
            <div class="kd-stat" style="border-color:{color}44">
                <div class="kd-stat-value" style="color:{color};font-size:2.5rem">{score:.1f}%</div>
                <div class="kd-stat-label">Overall Bias Score</div>
                <div class="kd-stat-delta" style="color:{color}">{"⚠️ Bias Detected" if score > 30 else "✅ Looks Fair"}</div>
            </div>
            """, unsafe_allow_html=True)
        with rc:
            if cats:
                st.markdown('<div class="kd-section-title">Category Breakdown</div>', unsafe_allow_html=True)
                for cat, val in cats.items():
                    bar_color = "#ef4444" if val > 40 else "#f59e0b" if val > 15 else "#10b981"
                    st.markdown(f"""
                    <div style="margin-bottom:.65rem">
                        <div style="display:flex;justify-content:space-between;font-size:.83rem;color:#94a3b8;margin-bottom:.3rem">
                            <span style="font-weight:500">{cat.title()}</span><span>{val:.1f}%</span>
                        </div>
                        <div style="height:8px;background:#2d3148;border-radius:4px;overflow:hidden">
                            <div style="height:100%;width:{int(val)}%;background:{bar_color};border-radius:4px;transition:width .5s"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        if data.get("findings"):
            st.markdown('<div class="kd-section-title">Findings</div>', unsafe_allow_html=True)
            for f in data["findings"]:
                sev = f.get("severity", "low")
                st.markdown(f"""
                <div class="kd-bias-finding {sev}">
                    <div style="display:flex;justify-content:space-between;align-items:center">
                        <span style="font-weight:600;color:#e2e8f0">{_risk_icon(sev)} {f.get("category","").title()}</span>
                        <span style="font-size:.73rem;background:#1e2130;color:#64748b;padding:.15rem .5rem;border-radius:5px">{sev}</span>
                    </div>
                    <div style="color:#94a3b8;font-size:.84rem;margin:.35rem 0">"{f.get("text","")}"</div>
                    <div style="color:#64748b;font-size:.82rem">{f.get("explanation","")}</div>
                    {f'<div class="kd-tip" style="margin-top:.5rem">💡 {f["suggestion"]}</div>' if f.get("suggestion") else ""}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ No significant bias detected in this text.")

        if data.get("corrected_text"):
            st.markdown('<div class="kd-section-title">✨ Debiased Version</div>', unsafe_allow_html=True)
            st.text_area("", data["corrected_text"], height=180, label_visibility="collapsed")


def page_pii_masking():
    st.markdown('<div class="kd-section-title" style="font-size:1.4rem;margin-top:0">🔒 PII Masking</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#64748b;margin-bottom:1.25rem">Automatically mask personal information before sharing legal documents.</div>', unsafe_allow_html=True)

    text = st.text_area("Document to mask", height=200, placeholder="วางเอกสารที่ต้องการปิดบังข้อมูลส่วนตัว...")

    st.markdown('<div class="kd-section-title">What to mask</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    mask_name = c1.checkbox("Names", value=True)
    mask_id   = c2.checkbox("National ID", value=True)
    mask_addr = c3.checkbox("Address", value=True)
    mask_phone = c4.checkbox("Phone", value=True)

    if text and st.button("🔒 Mask PII", type="primary"):
        orch = st.session_state.orchestrator
        cfg = {"name": mask_name, "national_id": mask_id, "address": mask_addr, "phone": mask_phone}
        with st.spinner("Masking..."):
            result = orch.mask_pii(text, cfg)
        data = result.get("data", {})
        summary = data.get("summary", {})

        st.markdown(f"""
        <div class="kd-metric-row" style="grid-template-columns:repeat(3,1fr)">
            <div class="kd-metric-box"><div class="kd-metric-label">Total PII Found</div><div class="kd-metric-value">{summary.get("total_detected",0)}</div></div>
            <div class="kd-metric-box"><div class="kd-metric-label">Names</div><div class="kd-metric-value">{summary.get("names",0)}</div></div>
            <div class="kd-metric-box"><div class="kd-metric-label">National IDs</div><div class="kd-metric-value">{summary.get("national_ids",0)}</div></div>
        </div>
        """, unsafe_allow_html=True)

        masked = data.get("masked_text", "")
        st.markdown('<div class="kd-section-title">✨ Masked Result</div>', unsafe_allow_html=True)
        st.text_area("", masked, height=220, label_visibility="collapsed")
        st.download_button("📥 Download", masked, file_name="masked_document.txt", mime="text/plain")

        if data.get("entities_found"):
            st.markdown('<div class="kd-section-title">Entities Detected</div>', unsafe_allow_html=True)
            rows = ""
            for ent in data["entities_found"]:
                rows += f"""
                <div class="kd-comp-row">
                    <span style="color:#64748b;font-size:.82rem">{ent.get("type","").title()}</span>
                    <span style="color:#94a3b8;font-size:.84rem">{ent.get("original","")}</span>
                    <span class="kd-law-pill">{ent.get("masked","")}</span>
                </div>
                """
            st.markdown(f'<div class="kd-card">{rows}</div>', unsafe_allow_html=True)


def page_case_law():
    st.markdown('<div class="kd-section-title" style="font-size:1.4rem;margin-top:0">📚 Case Law Search</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#64748b;margin-bottom:1.25rem">Search Thai court precedents using semantic AI search.</div>', unsafe_allow_html=True)

    query = st.text_input("🔍 Search", placeholder="e.g., ค่าจ้าง นายจ้าง ไม่จ่าย หรือ unfair termination severance...")

    c1, c2 = st.columns(2)
    with c1:
        court = st.selectbox("Court", ["", "ศาลแรงงาน", "ศาลฎีกา", "ศาลปกครอง", "ศาลแพ่ง"])
    with c2:
        case_type = st.selectbox("Case Type", ["", "wage_theft", "unfair_termination", "bonus_dispute"])

    if query and st.button("🔍 Search", type="primary"):
        orch = st.session_state.orchestrator
        with st.spinner("Searching..."):
            result = orch.search_case_law(query, case_type=case_type, court=court)
        data = result.get("data", {})
        cases = data.get("cases", [])

        st.markdown(f'<div class="kd-section-title">📋 {len(cases)} Result(s)</div>', unsafe_allow_html=True)
        if cases:
            for case in cases:
                rel = int(case.get("relevance_score", 0.5) * 100)
                sections = "".join(f'<span class="kd-law-pill">{s}</span>' for s in case.get("applicable_sections", []))
                st.markdown(f"""
                <div class="kd-case-card">
                    <div style="display:flex;justify-content:space-between;align-items:center">
                        <span class="kd-case-num">{case.get("case_number","N/A")}</span>
                        <span style="font-size:.75rem;color:#475569">{case.get("court","N/A")} · {case.get("year","")}</span>
                    </div>
                    <div class="kd-case-issue">{case.get("issue","")}</div>
                    <div class="kd-case-summary">{case.get("summary","")}</div>
                    <div style="margin-top:.5rem;font-size:.8rem;color:#818cf8">⚖️ {case.get("key_principle","")}</div>
                    <div style="margin-top:.5rem">{sections}</div>
                    <div class="kd-relevance-bar"><div class="kd-relevance-fill" style="width:{rel}%"></div></div>
                    <div style="font-size:.72rem;color:#475569;margin-top:.25rem">Relevance: {rel}%</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No results. Try a different search query.")


def page_summarize():
    st.markdown('<div class="kd-section-title" style="font-size:1.4rem;margin-top:0">📝 Document Summary</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#64748b;margin-bottom:1.25rem">AI-powered summarization of Thai legal documents.</div>', unsafe_allow_html=True)

    text = st.text_area("Document to summarize", height=200, placeholder="วางเอกสารที่ต้องการสรุป...")
    length = st.select_slider("Length", options=["short", "medium", "long"], value="medium")

    if text and st.button("📝 Summarize", type="primary"):
        orch = st.session_state.orchestrator
        with st.spinner("Summarizing..."):
            result = orch.summarize_document(text, length=length)
        data = result.get("data", {})

        st.markdown('<div class="kd-card-accent">', unsafe_allow_html=True)
        st.markdown(f'<div style="color:#c7d2fe;line-height:1.75;font-size:.95rem">{data.get("summary","")}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        if data.get("key_points"):
            st.markdown('<div class="kd-section-title">🎯 Key Points</div>', unsafe_allow_html=True)
            for point in data["key_points"]:
                st.markdown(f'<div class="kd-tip">• {point}</div>', unsafe_allow_html=True)

        if data.get("entities"):
            st.markdown('<div class="kd-section-title">🏷️ Entities</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            items = list(data["entities"].items())
            for i, (etype, ents) in enumerate(items):
                col = c1 if i % 2 == 0 else c2
                with col:
                    if ents:
                        st.markdown(f'<div style="font-size:.78rem;color:#818cf8;font-weight:600;margin-bottom:.3rem">{etype.upper()}</div>', unsafe_allow_html=True)
                        for e in ents:
                            st.markdown(f'<span class="kd-law-pill">{e}</span>', unsafe_allow_html=True)


def page_dashboard():
    st.markdown('<div class="kd-section-title" style="font-size:1.4rem;margin-top:0">📊 Agent Dashboard</div>', unsafe_allow_html=True)

    orch = st.session_state.orchestrator

    # LLM status
    if st.button("🔄 Refresh Status"):
        health = orch.llm.health_check()
        st.session_state.llm_status = health

    health = st.session_state.llm_status or orch.llm.health_check()
    if health["status"] == "healthy":
        models = ", ".join(health.get("models", []))
        st.success(f"✅ LLM Connected — {models}")
    else:
        st.error(f"❌ LLM Offline — {health.get('error','Unknown')}")
        st.markdown(f'<div class="kd-tip">Endpoint: {orch.llm.config.base_url}</div>', unsafe_allow_html=True)

    # Agent cards
    st.markdown('<div class="kd-section-title">🤖 Agent Status</div>', unsafe_allow_html=True)
    icons = ["🔍", "🗺️", "⚖️", "📚"]
    cols = st.columns(4)
    for col, icon, agent in zip(cols, icons, orch.agents):
        tasks = len(agent.history)
        with col:
            st.markdown(f"""
            <div class="kd-card" style="text-align:center">
                <div style="font-size:2rem">{icon}</div>
                <div style="font-weight:600;color:#e2e8f0;font-size:.88rem;margin:.35rem 0">{agent.name}</div>
                <div style="font-size:2rem;font-weight:700;color:#818cf8">{tasks}</div>
                <div style="font-size:.74rem;color:#64748b">tasks completed</div>
            </div>
            """, unsafe_allow_html=True)

    # Execution log
    if orch._execution_log:
        st.markdown('<div class="kd-section-title">📋 Execution Log</div>', unsafe_allow_html=True)
        st.markdown('<div class="kd-card" style="max-height:300px;overflow-y:auto">', unsafe_allow_html=True)
        for entry in reversed(orch._execution_log[-25:]):
            st.markdown(
                f'<div style="font-size:.78rem;color:#475569;padding:.2rem 0;font-family:monospace;border-bottom:1px solid #2d3148">'
                f'▸ <span style="color:#818cf8">{entry["event"]}</span>'
                + (f' <span style="color:#475569">— {entry.get("data","")}</span>' if entry.get("data") else "")
                + "</div>",
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("No executions yet. Run a case analysis first.")

    # Architecture
    st.markdown('<div class="kd-section-title">🏗️ Architecture</div>', unsafe_allow_html=True)
    st.code("""
OrchestratorAgent
├── LegalAnalysisAgent  → classify · extract · risk
├── CaseStrategyAgent   → simulate · map · timeline
├── BiasAuditAgent      → bias · PII masking
└── CaseLawAgent        → search · summarize · report
         │
    LLM Service (OpenAI-compatible)
         │
    vLLM + ROCm on AMD MI300X (192GB HBM3)
""", language="text")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    init_session()
    menu = sidebar()

    page_map = {
        "🏠  Overview":        page_overview,
        "🔍  Full Analysis":   page_full_analysis,
        "🗺️  Case Map":        page_case_map,
        "🔮  What-If Simulator": page_simulator,
        "⚖️  Bias Audit":      page_bias_audit,
        "🔒  PII Masking":     page_pii_masking,
        "📚  Case Law":        page_case_law,
        "📝  Summarize":       page_summarize,
        "📊  Dashboard":       page_dashboard,
    }

    fn = page_map.get(menu, page_overview)
    fn()


if __name__ == "__main__":
    main()
