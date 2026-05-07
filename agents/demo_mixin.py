"""
Demo Mode Mixin for OrchestratorAgent
Provides fallback demo data when LLM is not connected.
"""

from data.demo_responses import (
    DEMO_ANALYSIS,
    DEMO_STRATEGY,
    DEMO_BIAS,
    DEMO_CASE_LAW,
    DEMO_PII_MASKED,
    DEMO_CASE_MAP,
    DEMO_DOCUMENT_SUMMARY,
    is_demo_mode,
)


class DemoModeMixin:
    """Mixin that provides demo fallback for all orchestrator methods."""

    def _demo_analyze_case(self, text: str) -> dict:
        return {
            "status": "success",
            "mode": "demo",
            "agent_count": 4,
            "execution_time": 2.34,
            "results": {
                "analysis": {"status": "success", "data": DEMO_ANALYSIS},
                "strategy": {"status": "success", "data": DEMO_STRATEGY},
                "bias": {"status": "success", "data": DEMO_BIAS},
                "case_law": {"status": "success", "data": DEMO_CASE_LAW},
            },
            "execution_log": [
                {"event": "pipeline_start", "data": "demo_mode"},
                {"event": "legal_analysis_complete", "data": "2.1s"},
                {"event": "parallel_agents_complete", "data": "strategy+case_law+bias"},
                {"event": "pipeline_complete", "data": "2.34s"},
            ],
        }

    def _demo_simulate_scenario(self, case_type: str, summary: str, scenario: str, key_facts: list) -> dict:
        return {"status": "success", "mode": "demo", "data": DEMO_STRATEGY}

    def _demo_search_case_law(self, query: str, **kwargs) -> dict:
        return {"status": "success", "mode": "demo", "data": DEMO_CASE_LAW}

    def _demo_audit_bias(self, text: str) -> dict:
        return {"status": "success", "mode": "demo", "data": DEMO_BIAS}

    def _demo_mask_pii(self, text: str, config: dict = None) -> dict:
        return {"status": "success", "mode": "demo", "data": DEMO_PII_MASKED}

    def _demo_summarize_document(self, text: str, **kwargs) -> dict:
        return {"status": "success", "mode": "demo", "data": DEMO_DOCUMENT_SUMMARY}

    def _demo_generate_case_map(self, case_type: str, strategy: str) -> dict:
        return {"status": "success", "mode": "demo", "data": DEMO_CASE_MAP}
