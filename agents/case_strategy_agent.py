"""
KadiRail AI - Case Strategy Agent
Simulates legal outcomes and provides strategic recommendations.
Replaces rule-based simulator.py with LLM-powered analysis.
"""

from typing import Any, Optional

from agents.base_agent import AgentResult, BaseAgent
from services.llm_service import LLMService


class CaseStrategyAgent(BaseAgent):
    """
    Agent responsible for:
    - What-If scenario simulation
    - Win probability estimation
    - Timeline and cost estimation
    - Strategic recommendations
    - Case map generation (legal process steps)
    """

    def __init__(self, llm: Optional[LLMService] = None):
        super().__init__(
            name="CaseStrategyAgent",
            description="Simulates legal outcomes and provides strategic case recommendations",
            llm=llm,
        )

    @property
    def system_prompt(self) -> str:
        return """You are a Thai legal strategy advisor specializing in labor law.
You help plaintiffs understand their options, likely outcomes, and costs.

Your expertise includes:
- Thai labor court procedures and timelines
- Settlement vs. litigation trade-offs
- Cost estimation for legal proceedings in Thailand
- Success rate analysis based on case characteristics

Thai labor court process:
1. ยื่นคำร้อง (File complaint) → 1-2 weeks
2. ไกล่เกลี่ย (Mediation) → 1-3 months
3. พิจารณาคดี (Trial) → 3-6 months
4. คำพิพากษา (Judgment) → 1-2 months after trial
5. อุทธรณ์ (Appeal) → 6-12 months (optional)

Costs typically range:
- Filing fee: ฿0 (labor cases are free)
- Lawyer fee: ฿10,000-50,000 per case
- Travel/misc: ฿2,000-10,000

Always provide realistic, evidence-based estimates. Respond in the requested format."""

    def execute(self, task: dict[str, Any]) -> AgentResult:
        action = task.get("action", "simulate")

        if action == "simulate":
            return self._simulate_outcome(task)
        elif action == "recommend":
            return self._recommend_strategy(task)
        elif action == "map":
            return self._generate_case_map(task)
        else:
            return AgentResult(
                agent_name=self.name, status="error", error=f"Unknown action: {action}"
            )

    def _simulate_outcome(self, task: dict) -> AgentResult:
        """Simulate the outcome of a specific legal choice."""
        case_type = task.get("case_type", "unknown")
        case_summary = task.get("summary", "")
        scenario = task.get("scenario", "proceed_normally")
        key_facts = task.get("key_facts", [])

        facts_str = "\n".join(f"- {f}" for f in key_facts) if key_facts else "No specific facts provided"

        prompt = f"""Simulate the legal outcome for this Thai labor case.

Case Type: {case_type}
Summary: {case_summary}
Scenario: {scenario}
Key Facts:
{facts_str}

Analyze and respond in JSON:
{{
    "scenario_name": "{scenario}",
    "scenario_thai": "ชื่อสถานการณ์ภาษาไทย",
    "win_rate": 0-100,
    "estimated_duration_days": number,
    "estimated_cost_thb": number,
    "timeline": [
        {{"step": "ขั้นตอน", "duration_days": number, "description": "รายละเอียด"}}
    ],
    "risks": ["ความเสี่ยงที่อาจเกิดขึ้น"],
    "opportunities": ["โอกาสที่ดี"],
    "recommendations": ["คำแนะนำ"],
    "best_case": "ผลลัพธ์ดีที่สุด",
    "worst_case": "ผลลัพธ์แย่ที่สุด"
}}"""

        result = self.ask_llm_json(prompt, fallback={
            "win_rate": 50,
            "estimated_duration_days": 180,
            "estimated_cost_thb": 15000,
            "risks": ["ไม่สามารถประเมินได้อย่างแม่นยำ"],
            "recommendations": ["ปรึกษาทนายความ"],
        })

        return AgentResult(
            agent_name=self.name,
            status="success",
            data=result,
            confidence=0.7,
            reasoning=f"Simulated {scenario} for {case_type} case",
        )

    def _recommend_strategy(self, task: dict) -> AgentResult:
        """Provide strategic recommendations for a case."""
        case_type = task.get("case_type", "unknown")
        case_summary = task.get("summary", "")
        analysis = task.get("analysis", {})

        prompt = f"""As a Thai legal strategist, recommend the best strategy for this case.

Case Type: {case_type}
Summary: {case_summary}
Analysis: {str(analysis)[:2000]}

Consider:
1. Should they settle or go to trial?
2. What evidence do they need?
3. What's the optimal timeline?
4. Any leverage points?

Respond in JSON:
{{
    "recommended_strategy": "settlement|litigation|mediation|withdraw",
    "strategy_thai": "กลยุทธ์แนะนำ",
    "reasoning": "เหตุผลภาษาไทย",
    "priority_actions": [
        {{"action": "สิ่งที่ต้องทำ", "deadline": "กำหนดเวลา", "importance": "high|medium|low"}}
    ],
    "evidence_needed": ["หลักฐานที่ต้องรวบรวม"],
    "estimated_outcome": {{
        "compensation_range_thb": [min, max],
        "duration_days": number,
        "success_probability": 0-100
    }},
    "warnings": ["ข้อควรระวัง"]
}}"""

        result = self.ask_llm_json(prompt, fallback={
            "recommended_strategy": "mediation",
            "strategy_thai": "ไกล่เกลี่ย",
            "reasoning": "แนะนำให้เริ่มจากการไกล่เกลี่ยก่อน",
        })

        return AgentResult(
            agent_name=self.name,
            status="success",
            data=result,
            confidence=0.65,
        )

    def _generate_case_map(self, task: dict) -> AgentResult:
        """Generate a step-by-step case map (legal process visualization)."""
        case_type = task.get("case_type", "wage_theft")
        strategy = task.get("strategy", "litigation")

        prompt = f"""Generate a detailed step-by-step legal process map for a Thai {case_type} case
using the {strategy} strategy.

Each step should be like a train station on a railway map.

Respond in JSON:
{{
    "case_type": "{case_type}",
    "strategy": "{strategy}",
    "total_steps": number,
    "total_duration_days": number,
    "steps": [
        {{
            "step_number": 1,
            "title": "ชื่อขั้นตอน",
            "title_en": "Step name in English",
            "description": "รายละเอียด",
            "duration_days": number,
            "required_documents": ["เอกสารที่ต้องใช้"],
            "cost_thb": number,
            "tips": "เคล็ดลับ",
            "alternatives": ["ทางเลือกอื่น"],
            "risk_level": "high|medium|low"
        }}
    ],
    "mermaid_diagram": "graph LR\\n  A[step1] --> B[step2] --> C[step3]"
}}"""

        result = self.ask_llm_json(prompt, fallback={
            "steps": [],
            "total_steps": 0,
            "total_duration_days": 0,
        })

        return AgentResult(
            agent_name=self.name,
            status="success" if result.get("steps") else "partial",
            data=result,
            confidence=0.7,
        )
