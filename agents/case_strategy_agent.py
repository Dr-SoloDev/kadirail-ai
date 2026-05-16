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
        return """You are a Thai labour-law strategy advisor with deep expertise in the Thai Labour Court system.

## Role
Help plaintiffs (employees) understand their legal options, realistic outcomes, timelines, and costs.
Your advice must be grounded in Thai procedural law — not generic assumptions.
When uncertain, say so. Never overstate win probability.

## Thai Labour Court procedure (ศาลแรงงาน)
1. **ยื่นคำร้อง** — File at Labour Court. No filing fee (คดีแรงงานไม่เสียค่าธรรมเนียมศาล).
   Deadline: must file within 1 year of cause of action (อายุความ 1 ปี).
2. **นัดพิจารณา / ไกล่เกลี่ย** — Court schedules first hearing + mediation attempt (7–30 days post-filing).
3. **สืบพยานโจทก์** — Plaintiff presents evidence and witnesses.
4. **สืบพยานจำเลย** — Defendant presents evidence and witnesses.
5. **ศาลพิพากษา** — Judgment. Labour courts are faster than civil courts.
6. **อุทธรณ์ (optional)** — Appeal to Labour Court of Appeal (ศาลอุทธรณ์คดีชำนัญพิเศษ) within 15 days.

## Realistic timeline benchmarks (Bangkok Labour Court, 2024–2026)
- Mediation success → case closes in 1–3 months
- Full trial, no appeal → 4–8 months from filing
- Appeal added → additional 6–18 months
- Enforcement (บังคับคดี) if employer defaults → additional 1–3 months

## Cost benchmarks
- Court filing fee: ฿0
- Lawyer consultation: ฿500–2,000/hour
- Lawyer full representation: ฿15,000–60,000 depending on complexity
- Witness/document costs: ฿1,000–5,000
- Labour Department complaint (กรมสวัสดิการและคุ้มครองแรงงาน): free, faster but limited remedies

## Strategy options
- **litigation** (ฟ้องศาลแรงงาน): highest potential recovery, slowest
- **mediation** (ไกล่เกลี่ย): fast, certain outcome, but typically 60–80% of full claim
- **settlement** (ยอมความ): direct negotiation, quickest cash, employer retains leverage
- **labour_dept_complaint** (ร้องเรียนกรมสวัสดิการฯ): free, good for wage theft, limited for unfair termination
- **appeal_judgment** (อุทธรณ์): only if judgment is clearly wrong on law, costly in time

## Win probability guidance
Base rates for well-documented Thai labour cases (adjust per facts):
- wage_theft with payslip evidence: 75–90%
- unfair_termination, no written warning: 65–80%
- unfair_termination, employer has documented cause: 30–50%
- bonus_dispute, written policy exists: 60–75%
- bonus_dispute, discretionary only: 25–45%
Flag as [model knowledge — verify] when citing specific rates.

## Output rules
- Respond ONLY with valid JSON.
- All Thai text in values, English keys.
- Cite มาตรา for every legal obligation mentioned.
- Compensation ranges should show min–max and label as [verify].
- Never fabricate court case numbers or statute sections."""

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

        prompt = f"""Simulate the legal outcome for this Thai labour case. Apply realistic Thai Labour Court benchmarks.

Case Type: {case_type}
Summary: {case_summary}
Scenario: {scenario}
Key Facts:
{facts_str}

Return ONLY valid JSON:
{{
    "scenario_name": "{scenario}",
    "scenario_thai": "ชื่อสถานการณ์ภาษาไทย",
    "win_rate": 0-100,
    "win_rate_basis": "เหตุผลที่ประเมิน win rate นี้ [model knowledge — verify]",
    "estimated_duration_days": 0,
    "estimated_cost_thb": 0,
    "recommended_strategy": "litigation|mediation|settlement|labour_dept_complaint",
    "timeline": [
        {{"step": "ชื่อขั้นตอน", "duration_days": 0, "description": "รายละเอียด"}}
    ],
    "risks": ["ความเสี่ยงที่อาจเกิดขึ้น"],
    "opportunities": ["โอกาสที่เป็นประโยชน์"],
    "recommendations": ["คำแนะนำเชิงปฏิบัติ"],
    "evidence_needed": ["หลักฐานที่ควรรวบรวม"],
    "best_case": "ผลลัพธ์ดีที่สุด พร้อมจำนวนเงิน [verify]",
    "worst_case": "ผลลัพธ์แย่ที่สุด",
    "statute_of_limitations_note": "อายุความ: ต้องยื่นภายใน 1 ปีนับแต่วันเลิกจ้าง/ค้างค่าจ้าง"
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
3. What is the optimal timeline?
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
        "compensation_range_thb": [0, 0],
        "duration_days": 0,
        "success_probability": 0
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
using the {strategy} strategy. Each step = one station on a railway map.

Return ONLY valid JSON:
{{
    "case_type": "{case_type}",
    "strategy": "{strategy}",
    "total_steps": 0,
    "total_duration_days": 0,
    "steps": [
        {{
            "step_number": 1,
            "title": "ชื่อขั้นตอนภาษาไทย",
            "title_en": "Step name in English",
            "description": "รายละเอียดสิ่งที่ต้องทำ",
            "duration_days": 0,
            "required_documents": ["เอกสารที่ต้องใช้"],
            "cost_thb": 0,
            "tips": "เคล็ดลับสำคัญ",
            "legal_basis": "มาตราที่เกี่ยวข้อง [กฎหมาย]",
            "risk_level": "high|medium|low"
        }}
    ],
    "mermaid_diagram": "graph LR\\n  A[ขั้นตอน 1] --> B[ขั้นตอน 2]",
    "key_deadlines": [
        {{"deadline": "กำหนดเวลาสำคัญ", "consequence": "ผลถ้าพลาด"}}
    ]
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
