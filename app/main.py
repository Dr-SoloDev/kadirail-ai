"""
KadiRail AI - Multi-Agent Legal Navigation System
Streamlit Main Application

Powered by AMD Instinct MI300X + ROCm + vLLM
AMD Developer Hackathon 2026 — Track 1: AI Agents & Agentic Workflows
"""

import os
import streamlit as st

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from agents.orchestrator import OrchestratorAgent
from services.llm_service import LLMConfig, LLMService, get_llm_service

# Page config
st.set_page_config(
    page_title="KadiRail AI - Multi-Agent Legal Navigator",
    page_icon="🚂",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Theme
st.markdown("""
<style>
    .main { background-color: #f8fafc; }
    .stApp { background-color: #ffffff; }
    .agent-card {
        padding: 1rem; border-radius: 0.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; margin-bottom: 0.5rem;
    }
    .agent-active { border-left: 4px solid #10B981; background-color: #ecfdf5; padding: 0.5rem; border-radius: 0.25rem; margin: 0.25rem 0; }
    .agent-waiting { border-left: 4px solid #f59e0b; background-color: #fffbeb; padding: 0.5rem; border-radius: 0.25rem; margin: 0.25rem 0; }
    .agent-done { border-left: 4px solid #6366f1; background-color: #eef2ff; padding: 0.5rem; border-radius: 0.25rem; margin: 0.25rem 0; }
    .risk-high { color: #dc2626; font-weight: bold; }
    .risk-medium { color: #f59e0b; font-weight: bold; }
    .risk-low { color: #10b981; font-weight: bold; }
    .metric-card { background: #f1f5f9; padding: 1rem; border-radius: 0.5rem; text-align: center; }
    .step-card { padding: 1rem; border-radius: 0.5rem; background-color: #f1f5f9; margin-bottom: 0.5rem; }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state."""
    if "orchestrator" not in st.session_state:
        st.session_state.orchestrator = OrchestratorAgent()
    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = None
    if "llm_connected" not in st.session_state:
        st.session_state.llm_connected = False


def check_llm_connection():
    """Check and display LLM connection status."""
    llm = get_llm_service()
    health = llm.health_check()
    connected = health["status"] == "healthy"
    st.session_state.llm_connected = connected
    return health


def sidebar():
    """Sidebar with navigation, LLM status, and agent info."""
    st.sidebar.title("🚂 KadiRail AI")
    st.sidebar.markdown("**Multi-Agent Legal Navigator**")
    st.sidebar.markdown("*AMD Instinct MI300X + ROCm + vLLM*")
    st.sidebar.markdown("---")

    # LLM Connection Status
    with st.sidebar.expander("⚡ LLM Status", expanded=False):
        if st.button("Check Connection", use_container_width=True):
            health = check_llm_connection()
            if health["status"] == "healthy":
                st.success(f"✅ Connected")
                for m in health.get("models", []):
                    st.code(m)
            else:
                st.error(f"❌ {health.get('error', 'Disconnected')}")

        # Quick config
        base_url = st.text_input("vLLM URL", value=os.getenv("LLM_BASE_URL", "http://localhost:8000/v1"))
        model = st.text_input("Model", value=os.getenv("LLM_MODEL", "Qwen/Qwen2-7B-Instruct"))
        if st.button("Update Config", use_container_width=True):
            config = LLMConfig(base_url=base_url, model=model)
            new_llm = LLMService(config)
            st.session_state.orchestrator = OrchestratorAgent(llm=new_llm)
            st.success("✅ Config updated!")
            st.rerun()

    st.sidebar.markdown("---")

    # Navigation
    menu = st.sidebar.radio(
        "Navigate",
        [
            "🏠 Home",
            "🔍 Full Case Analysis",
            "🗺️ Case Map",
            "🔮 What-If Simulator",
            "⚖️ Bias Audit",
            "🔒 PII Masking",
            "📚 Case Law Search",
            "📝 Document Summary",
            "📊 Agent Dashboard",
        ],
    )

    st.sidebar.markdown("---")

    # Agent status
    st.sidebar.markdown("### 🤖 Agents")
    orch = st.session_state.orchestrator
    for agent in orch.agents:
        tasks = len(agent.history)
        icon = "🟢" if tasks > 0 else "⚪"
        st.sidebar.markdown(f"{icon} **{agent.name}** ({tasks} tasks)")

    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    **🏆 AMD Developer Hackathon 2026**
    Track 1: AI Agents & Agentic Workflows
    
    **NovaPulse Team**
    """)

    return menu


def home_page():
    """Landing page."""
    st.title("🚂 KadiRail AI")
    st.markdown("### Multi-Agent Legal Navigation System for Thailand")
    st.markdown("*Transform complex legal cases into clear, actionable maps — powered by AI agents on AMD GPUs*")
    st.markdown("---")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        ## How It Works
        
        KadiRail AI uses **5 specialized AI agents** running on **AMD Instinct MI300X** GPUs
        to analyze Thai legal cases end-to-end:
        
        | Agent | Role |
        |-------|------|
        | 🔍 **LegalAnalysisAgent** | Document analysis, case classification, entity extraction |
        | 🗺️ **CaseStrategyAgent** | What-If simulation, timeline & cost estimation |
        | ⚖️ **BiasAuditAgent** | Bias detection, PII masking, fairness scoring |
        | 📚 **CaseLawAgent** | Case law search, summarization, report generation |
        | 🎯 **OrchestratorAgent** | Coordinates all agents in optimal workflow |
        
        ### Supported Case Types (Thai Labor Law)
        - **โกงค่าจ้าง** — Wage theft / unpaid wages
        - **เลิกจ้างไม่เป็นธรรม** — Unfair termination
        - **ไม่จ่ายโบนัส** — Bonus disputes
        """)

    with col2:
        st.markdown("### 🚀 Quick Start")
        st.info("Upload or paste a legal document to get started. The AI agents will analyze it automatically.")

        st.markdown("### 📊 Impact")
        st.metric("Case Understanding Time", "120 min → 5 min", delta="-96%", delta_color="normal")

        st.markdown("### ⚡ Tech Stack")
        st.markdown("""
        - **GPU:** AMD Instinct MI300X (192GB)
        - **Runtime:** ROCm + vLLM
        - **LLM:** Open-source (Qwen/Llama)
        - **Framework:** Python + Streamlit
        - **Agents:** Custom multi-agent system
        """)


def full_analysis_page():
    """Full case analysis — runs all agents."""
    st.title("🔍 Full Case Analysis")
    st.markdown("Upload or paste a legal document. All 5 agents will analyze it together.")

    text = st.text_area(
        "Paste legal document text (Thai or English)",
        height=250,
        placeholder="วางเอกสารคดีที่นี่... / Paste your legal document here...",
    )

    if text and st.button("🚀 Run Full Analysis", type="primary", use_container_width=True):
        orch = st.session_state.orchestrator

        # Show agent pipeline progress
        progress = st.empty()
        status_container = st.container()

        with status_container:
            st.markdown("### 🤖 Agent Pipeline")
            agent_cols = st.columns(4)
            placeholders = {}
            agent_names = [
                ("🔍", "LegalAnalysis"),
                ("🗺️", "CaseStrategy"),
                ("📚", "CaseLaw"),
                ("⚖️", "BiasAudit"),
            ]
            for i, (icon, name) in enumerate(agent_names):
                with agent_cols[i]:
                    placeholders[name] = st.empty()
                    placeholders[name].markdown(f"""<div class="agent-waiting">{icon} <b>{name}</b><br/>⏳ Waiting</div>""", unsafe_allow_html=True)

        with st.spinner("Running multi-agent analysis pipeline..."):
            # Update progress as agents run
            placeholders["LegalAnalysis"].markdown("""<div class="agent-active">🔍 <b>LegalAnalysis</b><br/>🔄 Analyzing...</div>""", unsafe_allow_html=True)

            result = orch.analyze_case(text)

            # Mark all as done
            for name in ["LegalAnalysis", "CaseStrategy", "CaseLaw", "BiasAudit"]:
                icon = {"LegalAnalysis": "🔍", "CaseStrategy": "🗺️", "CaseLaw": "📚", "BiasAudit": "⚖️"}[name]
                placeholders[name].markdown(f"""<div class="agent-done">{icon} <b>{name}</b><br/>✅ Complete</div>""", unsafe_allow_html=True)

        st.session_state.analysis_result = result

        # Display results
        st.markdown("---")
        st.markdown("### 📊 Results")

        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        analysis_data = result.get("results", {}).get("analysis", {}).get("data", {})
        strategy_data = result.get("results", {}).get("strategy", {}).get("data", {})
        bias_data = result.get("results", {}).get("bias", {}).get("data", {})

        with col1:
            case_type = analysis_data.get("case_type_thai", analysis_data.get("case_type", "Unknown"))
            st.metric("Case Type", case_type)
        with col2:
            risk = analysis_data.get("risk_level", "unknown")
            risk_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(risk, "⚪")
            st.metric("Risk Level", f"{risk_emoji} {risk.upper()}")
        with col3:
            win_rate = strategy_data.get("win_rate", "N/A")
            st.metric("Win Probability", f"{win_rate}%")
        with col4:
            bias_score = bias_data.get("bias_score", 0)
            st.metric("Bias Score", f"{bias_score:.1f}%")

        # Tabs for detailed results
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Analysis", "🗺️ Strategy", "📚 Case Law", "⚖️ Bias", "📊 Pipeline"])

        with tab1:
            st.markdown(f"**Summary:** {analysis_data.get('summary', 'N/A')}")
            if analysis_data.get("key_facts"):
                st.markdown("**Key Facts:**")
                for fact in analysis_data["key_facts"]:
                    st.markdown(f"- {fact}")
            if analysis_data.get("applicable_laws"):
                st.markdown("**Applicable Laws:**")
                for law in analysis_data["applicable_laws"]:
                    st.markdown(f"- {law}")

        with tab2:
            if strategy_data.get("timeline"):
                st.markdown("**Timeline:**")
                for step in strategy_data["timeline"]:
                    st.markdown(f"- **{step.get('step', '')}** ({step.get('duration_days', '?')} days): {step.get('description', '')}")
            if strategy_data.get("recommendations"):
                st.markdown("**Recommendations:**")
                for rec in strategy_data["recommendations"]:
                    st.markdown(f"- {rec}")

        with tab3:
            case_law_data = result.get("results", {}).get("case_law", {}).get("data", {})
            cases = case_law_data.get("cases", [])
            if cases:
                for case in cases:
                    with st.expander(f"📄 {case.get('case_number', 'N/A')}"):
                        st.markdown(f"**Court:** {case.get('court', 'N/A')}")
                        st.markdown(f"**Issue:** {case.get('issue', 'N/A')}")
                        st.markdown(f"**Summary:** {case.get('summary', 'N/A')}")
                        st.markdown(f"**Key Principle:** {case.get('key_principle', 'N/A')}")
            else:
                st.info("No case law results")

        with tab4:
            if bias_data.get("findings"):
                for finding in bias_data["findings"]:
                    sev = finding.get("severity", "low")
                    emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(sev, "⚪")
                    with st.expander(f"{emoji} {finding.get('category', '')} ({sev})"):
                        st.markdown(f"**Text:** {finding.get('text', '')}")
                        st.markdown(f"**Explanation:** {finding.get('explanation', '')}")
                        if finding.get("suggestion"):
                            st.markdown(f"**Suggestion:** {finding['suggestion']}")
            else:
                st.success("✅ No significant bias detected")

        with tab5:
            st.markdown(f"**Total Execution Time:** {result.get('execution_time', 0):.2f}s")
            st.markdown(f"**Agents Used:** {result.get('agent_count', 0)}")
            if result.get("execution_log"):
                st.markdown("**Execution Log:**")
                for entry in result["execution_log"]:
                    st.markdown(f"- `{entry['event']}`")


def case_map_page():
    """Case map — legal process visualization."""
    st.title("🗺️ Case Map")
    st.markdown("Visualize the legal process as a railway map")

    case_type = st.selectbox("Case Type", ["wage_theft", "unfair_termination", "bonus_dispute"])
    strategy = st.selectbox("Strategy", ["litigation", "mediation", "settlement"])

    if st.button("🗺️ Generate Case Map", type="primary"):
        orch = st.session_state.orchestrator
        with st.spinner("Generating case map..."):
            result = orch.case_strategy.run({
                "action": "map",
                "case_type": case_type,
                "strategy": strategy,
            })

        data = result.data
        if data.get("steps"):
            st.markdown(f"### {case_type.replace('_', ' ').title()} — {strategy.title()} Path")
            st.markdown(f"**Total Steps:** {data.get('total_steps', 'N/A')} | **Duration:** {data.get('total_duration_days', 'N/A')} days")

            # Mermaid diagram
            if data.get("mermaid_diagram"):
                st.markdown("#### Process Flow")
                mermaid = data["mermaid_diagram"]
                st.code(mermaid, language="mermaid")

            # Step details
            st.markdown("#### Step Details")
            for step in data["steps"]:
                risk = step.get("risk_level", "low")
                emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(risk, "⚪")
                with st.expander(f"🚉 Step {step.get('step_number', '?')}: {step.get('title', '')} {emoji}"):
                    st.markdown(f"**Duration:** {step.get('duration_days', '?')} days")
                    st.markdown(f"**Description:** {step.get('description', '')}")
                    st.markdown(f"**Cost:** ฿{step.get('cost_thb', 0):,}")
                    if step.get("required_documents"):
                        st.markdown("**Required Documents:**")
                        for doc in step["required_documents"]:
                            st.markdown(f"- {doc}")
                    if step.get("tips"):
                        st.info(f"💡 {step['tips']}")
        else:
            st.warning("Could not generate case map. Check LLM connection.")


def simulator_page():
    """What-If Simulator."""
    st.title("🔮 What-If Simulator")
    st.markdown("Simulate different legal strategies and their outcomes")

    col1, col2 = st.columns(2)
    with col1:
        case_type = st.selectbox("Case Type", ["wage_theft", "unfair_termination", "bonus_dispute"], key="sim_case")
    with col2:
        scenario = st.selectbox("Scenario", [
            "proceed_normally",
            "settle_early",
            "go_to_mediation",
            "full_litigation",
            "appeal_judgment",
        ])

    summary = st.text_area("Case Summary", placeholder="Brief description of the case...", height=100)
    key_facts = st.text_area("Key Facts (one per line)", placeholder="Fact 1\nFact 2\nFact 3", height=100)

    if summary and st.button("🔮 Simulate", type="primary"):
        orch = st.session_state.orchestrator
        facts = [f.strip() for f in key_facts.split("\n") if f.strip()] if key_facts else []

        with st.spinner("Running simulation..."):
            result = orch.simulate_scenario(case_type, summary, scenario, facts)

        data = result.get("data", {})
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Win Probability", f"{data.get('win_rate', 'N/A')}%")
        with col2:
            st.metric("Duration", f"{data.get('estimated_duration_days', 'N/A')} days")
        with col3:
            st.metric("Est. Cost", f"฿{data.get('estimated_cost_thb', 0):,}")

        if data.get("risks"):
            st.markdown("### ⚠️ Risks")
            for r in data["risks"]:
                st.markdown(f"- {r}")
        if data.get("recommendations"):
            st.markdown("### 💡 Recommendations")
            for r in data["recommendations"]:
                st.markdown(f"- {r}")
        if data.get("best_case"):
            st.success(f"**Best Case:** {data['best_case']}")
        if data.get("worst_case"):
            st.error(f"**Worst Case:** {data['worst_case']}")


def bias_audit_page():
    """Bias detection page."""
    st.title("⚖️ Bias Audit")
    st.markdown("Detect bias in legal texts using AI")

    text = st.text_area("Paste text to audit for bias", height=200, placeholder="ใส่ข้อความภาษาไทยที่นี่...")

    if text and st.button("🔍 Audit Bias", type="primary"):
        orch = st.session_state.orchestrator
        with st.spinner("Running bias audit..."):
            result = orch.audit_bias(text)

        data = result.get("data", {})
        col1, col2 = st.columns(2)
        with col1:
            score = data.get("bias_score", 0)
            st.metric("Bias Score", f"{score:.1f}%",
                      delta="⚠️ Bias Detected" if score > 30 else "✅ Fair",
                      delta_color="inverse" if score > 30 else "normal")
        with col2:
            categories = data.get("bias_categories", {})
            if categories:
                top = max(categories.items(), key=lambda x: x[1])
                st.metric("Highest Category", f"{top[0]}: {top[1]:.1f}%")

        if data.get("findings"):
            st.markdown("### 🔎 Findings")
            for finding in data["findings"]:
                sev = finding.get("severity", "low")
                emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(sev, "⚪")
                with st.expander(f"{emoji} {finding.get('category', '')} ({sev})"):
                    st.markdown(f"**Text:** {finding.get('text', '')}")
                    st.markdown(f"**Explanation:** {finding.get('explanation', '')}")
                    if finding.get("suggestion"):
                        st.markdown(f"**Suggestion:** {finding['suggestion']}")

        if data.get("corrected_text"):
            st.markdown("### ✨ Corrected Text")
            st.text_area("Debiased version", data["corrected_text"], height=200)


def pii_masking_page():
    """PII masking page."""
    st.title("🔒 PII Masking")
    st.markdown("Protect personal information in legal documents")

    text = st.text_area("Paste text to mask PII", height=200, placeholder="วางเอกสารที่ต้องการปิดบังข้อมูลส่วนตัว...")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        mask_name = st.checkbox("Names", value=True)
    with col2:
        mask_id = st.checkbox("National ID", value=True)
    with col3:
        mask_addr = st.checkbox("Address", value=True)
    with col4:
        mask_phone = st.checkbox("Phone", value=True)

    if text and st.button("🔒 Mask PII", type="primary"):
        orch = st.session_state.orchestrator
        pii_config = {"name": mask_name, "national_id": mask_id, "address": mask_addr, "phone": mask_phone}

        with st.spinner("Masking PII..."):
            result = orch.mask_pii(text, pii_config)

        data = result.get("data", {})
        summary = data.get("summary", {})

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total PII Found", summary.get("total_detected", 0))
        with col2:
            st.metric("Names", summary.get("names", 0))
        with col3:
            st.metric("National IDs", summary.get("national_ids", 0))

        st.markdown("### ✨ Masked Text")
        masked = data.get("masked_text", "")
        st.text_area("Result", masked, height=250)
        st.download_button("📥 Download Masked Document", masked, file_name="masked_document.txt", mime="text/plain")


def case_law_page():
    """Case law search page."""
    st.title("📚 Case Law Search")
    st.markdown("Search Thai court precedents using AI")

    query = st.text_input("🔍 Search query", placeholder="e.g., ค่าจ้าง นายจ้าง ไม่จ่าย...")

    col1, col2 = st.columns(2)
    with col1:
        court = st.selectbox("Court", ["", "ศาลแรงงาน", "ศาลฎีกา", "ศาลปกครอง", "ศาลแพ่ง"])
    with col2:
        case_type = st.selectbox("Case Type", ["", "wage_theft", "unfair_termination", "bonus_dispute"])

    if query and st.button("🔍 Search", type="primary"):
        orch = st.session_state.orchestrator
        with st.spinner("Searching case law..."):
            result = orch.search_case_law(query, case_type=case_type, court=court)

        data = result.get("data", {})
        cases = data.get("cases", [])
        st.markdown(f"### 📋 Results ({len(cases)} cases)")

        if cases:
            for case in cases:
                with st.expander(f"📄 {case.get('case_number', 'N/A')} — {case.get('issue', '')}"):
                    st.markdown(f"**Court:** {case.get('court', 'N/A')}")
                    st.markdown(f"**Year:** {case.get('year', 'N/A')}")
                    st.markdown(f"**Summary:** {case.get('summary', 'N/A')}")
                    st.markdown(f"**Key Principle:** {case.get('key_principle', 'N/A')}")
                    if case.get("applicable_sections"):
                        st.markdown(f"**Sections:** {', '.join(case['applicable_sections'])}")
                    st.progress(case.get("relevance_score", 0.5))
        else:
            st.info("No results found. Try a different query.")


def document_summary_page():
    """Document summarization page."""
    st.title("📝 Document Summary")
    st.markdown("Summarize legal documents using AI")

    text = st.text_area("Paste document to summarize", height=200, placeholder="วางเอกสารที่ต้องการสรุป...")
    length = st.select_slider("Summary Length", options=["short", "medium", "long"], value="medium")

    if text and st.button("📝 Summarize", type="primary"):
        orch = st.session_state.orchestrator
        with st.spinner("Summarizing..."):
            result = orch.summarize_document(text, length=length)

        data = result.get("data", {})
        st.markdown("### 📋 Summary")
        st.markdown(data.get("summary", "Could not generate summary"))

        if data.get("key_points"):
            st.markdown("### 🎯 Key Points")
            for point in data["key_points"]:
                st.markdown(f"- {point}")

        if data.get("entities"):
            with st.expander("🏷️ Extracted Entities"):
                for etype, entities in data["entities"].items():
                    if entities:
                        st.markdown(f"**{etype}:** {', '.join(entities)}")


def agent_dashboard_page():
    """Agent status dashboard."""
    st.title("📊 Agent Dashboard")
    st.markdown("Monitor the multi-agent system")

    orch = st.session_state.orchestrator

    # LLM Status
    st.markdown("### ⚡ LLM Service")
    health = orch.llm.health_check()
    if health["status"] == "healthy":
        st.success(f"✅ Connected — Models: {', '.join(health.get('models', []))}")
    else:
        st.error(f"❌ Disconnected — {health.get('error', 'Unknown error')}")
        st.info(f"**Endpoint:** {orch.llm.config.base_url}")
        st.info("Make sure vLLM is running on your AMD Developer Cloud instance.")

    # Agent cards
    st.markdown("### 🤖 Agents")
    cols = st.columns(4)
    for i, agent in enumerate(orch.agents):
        with cols[i]:
            tasks = len(agent.history)
            st.markdown(f"""
            <div class="metric-card">
                <h3>{agent.name}</h3>
                <p>{agent.description}</p>
                <h2>{tasks}</h2>
                <p>tasks completed</p>
            </div>
            """, unsafe_allow_html=True)

    # Execution log
    if orch._execution_log:
        st.markdown("### 📋 Recent Execution Log")
        for entry in reversed(orch._execution_log[-20:]):
            st.markdown(f"- `{entry['event']}` — {entry.get('data', '')}")

    # Architecture diagram
    st.markdown("### 🏗️ Architecture")
    st.code("""
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
    """, language="text")


def main():
    """Main application entry point."""
    init_session_state()
    menu = sidebar()

    if menu == "🏠 Home":
        home_page()
    elif menu == "🔍 Full Case Analysis":
        full_analysis_page()
    elif menu == "🗺️ Case Map":
        case_map_page()
    elif menu == "🔮 What-If Simulator":
        simulator_page()
    elif menu == "⚖️ Bias Audit":
        bias_audit_page()
    elif menu == "🔒 PII Masking":
        pii_masking_page()
    elif menu == "📚 Case Law Search":
        case_law_page()
    elif menu == "📝 Document Summary":
        document_summary_page()
    elif menu == "📊 Agent Dashboard":
        agent_dashboard_page()


if __name__ == "__main__":
    main()
