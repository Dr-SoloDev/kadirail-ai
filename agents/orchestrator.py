"""
KadiRail AI - Orchestrator Agent
Coordinates all specialized agents for end-to-end legal case analysis.
This is the core of the multi-agent system.
"""

import logging
import time
from typing import Any, Optional

from agents.base_agent import AgentResult, BaseAgent
from agents.bias_audit_agent import BiasAuditAgent
from agents.case_law_agent import CaseLawAgent
from agents.case_strategy_agent import CaseStrategyAgent
from agents.legal_analysis_agent import LegalAnalysisAgent
from services.llm_service import LLMService, get_llm_service

logger = logging.getLogger(__name__)


class OrchestratorAgent:
    """
    Multi-Agent Orchestrator for KadiRail AI.

    Coordinates the workflow between specialized agents:
    1. LegalAnalysisAgent — Document analysis & classification
    2. CaseStrategyAgent — Outcome simulation & recommendations
    3. BiasAuditAgent — Bias detection & PII masking
    4. CaseLawAgent — Case law search & summarization

    Workflow:
    Document → LegalAnalysis → [CaseStrategy + CaseLaw + BiasAudit] → Final Report
    """

    def __init__(self, llm: Optional[LLMService] = None):
        self.llm = llm or get_llm_service()
        self.legal_analysis = LegalAnalysisAgent(llm=self.llm)
        self.case_strategy = CaseStrategyAgent(llm=self.llm)
        self.bias_audit = BiasAuditAgent(llm=self.llm)
        self.case_law = CaseLawAgent(llm=self.llm)
        self._execution_log: list[dict] = []

    @property
    def agents(self) -> list[BaseAgent]:
        return [self.legal_analysis, self.case_strategy, self.bias_audit, self.case_law]

    def _log(self, event: str, data: Any = None):
        entry = {
            "timestamp": time.time(),
            "event": event,
            "data": data,
        }
        self._execution_log.append(entry)
        logger.info(f"[Orchestrator] {event}")

    def analyze_case(self, text: str) -> dict[str, Any]:
        """
        Full case analysis pipeline.
        Runs all agents in the optimal order and combines results.
        """
        start = time.time()
        self._log("pipeline_start", {"text_length": len(text)})
        results = {}

        # Step 1: Legal Analysis (must run first — other agents depend on it)
        self._log("step_1_legal_analysis")
        analysis = self.legal_analysis.run({"action": "analyze", "text": text})
        results["analysis"] = analysis.to_dict()

        case_type = analysis.data.get("case_type", "unknown")
        summary = analysis.data.get("summary", "")
        key_facts = analysis.data.get("key_facts", [])

        # Step 2: Run remaining agents (can conceptually run in parallel)
        # 2a: Case Strategy
        self._log("step_2a_case_strategy")
        strategy = self.case_strategy.run({
            "action": "simulate",
            "case_type": case_type,
            "summary": summary,
            "key_facts": key_facts,
            "scenario": "proceed_normally",
        })
        results["strategy"] = strategy.to_dict()

        # 2b: Case Law Search
        self._log("step_2b_case_law")
        case_law = self.case_law.run({
            "action": "search",
            "query": summary,
            "case_type": case_type,
        })
        results["case_law"] = case_law.to_dict()

        # 2c: Bias Audit
        self._log("step_2c_bias_audit")
        bias = self.bias_audit.run({"action": "audit", "text": text})
        results["bias"] = bias.to_dict()

        # Step 3: Generate case map
        self._log("step_3_case_map")
        case_map = self.case_strategy.run({
            "action": "map",
            "case_type": case_type,
            "strategy": strategy.data.get("recommended_strategy", "litigation"),
        })
        results["case_map"] = case_map.to_dict()

        # Compile final result
        elapsed = time.time() - start
        self._log("pipeline_complete", {"elapsed": elapsed})

        return {
            "status": "success",
            "case_type": case_type,
            "summary": summary,
            "results": results,
            "execution_time": elapsed,
            "execution_log": self._execution_log.copy(),
            "agent_count": len(self.agents),
        }

    def simulate_scenario(self, case_type: str, summary: str, scenario: str, key_facts: list = None) -> dict:
        """Run a What-If simulation for a specific scenario."""
        self._log("simulate_scenario", {"scenario": scenario})
        result = self.case_strategy.run({
            "action": "simulate",
            "case_type": case_type,
            "summary": summary,
            "scenario": scenario,
            "key_facts": key_facts or [],
        })
        return result.to_dict()

    def search_case_law(self, query: str, case_type: str = "", court: str = "", year: str = "") -> dict:
        """Search for relevant case law."""
        self._log("search_case_law", {"query": query})
        result = self.case_law.run({
            "action": "search",
            "query": query,
            "case_type": case_type,
            "court": court,
            "year": year,
        })
        return result.to_dict()

    def audit_bias(self, text: str) -> dict:
        """Run bias detection on text."""
        self._log("audit_bias")
        result = self.bias_audit.run({"action": "audit", "text": text})
        return result.to_dict()

    def mask_pii(self, text: str, pii_config: dict = None) -> dict:
        """Mask PII in text."""
        self._log("mask_pii")
        result = self.bias_audit.run({
            "action": "mask_pii",
            "text": text,
            "pii_config": pii_config or {"name": True, "national_id": True, "address": True, "phone": True},
        })
        return result.to_dict()

    def summarize_document(self, text: str, length: str = "medium") -> dict:
        """Summarize a legal document."""
        self._log("summarize_document")
        result = self.case_law.run({
            "action": "summarize",
            "text": text,
            "length": length,
            "include_key_points": True,
        })
        return result.to_dict()

    def generate_report(self, text: str) -> dict:
        """Generate a comprehensive legal report by running the full pipeline + report generation."""
        # Run full analysis first
        analysis_results = self.analyze_case(text)

        # Generate report from combined results
        self._log("generate_report")
        report = self.case_law.run({
            "action": "report",
            "summary": analysis_results.get("summary", ""),
            "analysis": analysis_results.get("results", {}).get("analysis", {}).get("data", {}),
            "case_law": analysis_results.get("results", {}).get("case_law", {}).get("data", {}).get("cases", []),
        })

        return {
            "analysis": analysis_results,
            "report": report.to_dict(),
        }

    def get_status(self) -> dict:
        """Get the status of all agents and the LLM service."""
        health = self.llm.health_check()
        return {
            "llm": health,
            "agents": {
                agent.name: {
                    "description": agent.description,
                    "tasks_completed": len(agent.history),
                }
                for agent in self.agents
            },
            "total_tasks": sum(len(a.history) for a in self.agents),
            "execution_log_size": len(self._execution_log),
        }
