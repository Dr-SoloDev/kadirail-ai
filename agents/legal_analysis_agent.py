"""
KadiRail AI - Legal Analysis Agent
Analyzes legal documents, extracts key information, classifies case types.
Replaces rule-based scanner.py and thai_nlp.py with LLM-powered analysis.
"""

from typing import Any, Optional

from agents.base_agent import AgentResult, BaseAgent
from services.llm_service import LLMService


class LegalAnalysisAgent(BaseAgent):
    """
    Agent responsible for:
    - Document text analysis and understanding
    - Case type classification (wage theft, unfair termination, bonus disputes)
    - Key entity extraction (parties, dates, amounts, courts)
    - Risk level assessment
    - Document completeness validation
    """

    def __init__(self, llm: Optional[LLMService] = None):
        super().__init__(
            name="LegalAnalysisAgent",
            description="Analyzes legal documents, classifies cases, and extracts key information",
            llm=llm,
        )

    @property
    def system_prompt(self) -> str:
        return """You are a Thai legal document analysis expert specializing in labor law cases.
Your role is to analyze legal documents and extract structured information.

You understand Thai labor law including:
- พ.ร.บ. คุ้มครองแรงงาน (Labor Protection Act)
- พ.ร.บ. จัดตั้งศาลแรงงานฯ (Labor Court Act)
- พ.ร.บ. แรงงานสัมพันธ์ (Labor Relations Act)

Case types you handle:
- wage_theft: โกงค่าจ้าง / ค้างค่าจ้าง / จ่ายไม่ครบ
- unfair_termination: เลิกจ้างไม่เป็นธรรม
- bonus_dispute: ไม่จ่ายโบนัส / โบนัสไม่ตรงสัญญา

Always respond in the requested format. Be precise and cite specific Thai laws when applicable."""

    def execute(self, task: dict[str, Any]) -> AgentResult:
        action = task.get("action", "analyze")

        if action == "analyze":
            return self._analyze_document(task)
        elif action == "classify":
            return self._classify_case(task)
        elif action == "extract":
            return self._extract_entities(task)
        elif action == "validate":
            return self._validate_document(task)
        else:
            return AgentResult(
                agent_name=self.name,
                status="error",
                error=f"Unknown action: {action}",
            )

    def _analyze_document(self, task: dict) -> AgentResult:
        """Full document analysis — classify, extract, assess risk."""
        text = task.get("text", "")
        if not text:
            return AgentResult(
                agent_name=self.name, status="error", error="No text provided"
            )

        prompt = f"""Analyze this Thai legal document and provide a comprehensive analysis.

Document:
---
{text[:4000]}
---

Respond in JSON format:
{{
    "case_type": "wage_theft|unfair_termination|bonus_dispute|unknown",
    "case_type_thai": "ประเภทคดีภาษาไทย",
    "summary": "Brief summary of the case in Thai",
    "parties": {{
        "plaintiff": "ชื่อโจทก์",
        "defendant": "ชื่อจำเลย"
    }},
    "key_facts": ["fact1", "fact2"],
    "dates": ["relevant dates"],
    "amounts": ["monetary amounts mentioned"],
    "applicable_laws": ["relevant Thai laws"],
    "risk_level": "high|medium|low",
    "risk_explanation": "Why this risk level",
    "completeness_score": 0.0-1.0,
    "missing_info": ["what's missing from the document"]
}}"""

        result = self.ask_llm_json(prompt, fallback={
            "case_type": "unknown",
            "summary": "ไม่สามารถวิเคราะห์เอกสารได้",
            "risk_level": "unknown",
            "completeness_score": 0.0,
        })

        return AgentResult(
            agent_name=self.name,
            status="success" if result.get("case_type") != "unknown" else "partial",
            data=result,
            confidence=result.get("completeness_score", 0.5),
            reasoning=result.get("summary", ""),
        )

    def _classify_case(self, task: dict) -> AgentResult:
        """Classify a case into one of the supported types."""
        text = task.get("text", "")
        prompt = f"""Classify this Thai legal text into one of these case types:
- wage_theft (โกงค่าจ้าง)
- unfair_termination (เลิกจ้างไม่เป็นธรรม)
- bonus_dispute (ไม่จ่ายโบนัส)
- unknown

Text: {text[:2000]}

Respond in JSON:
{{
    "case_type": "type",
    "case_type_thai": "ภาษาไทย",
    "confidence": 0.0-1.0,
    "reasoning": "why this classification"
}}"""

        result = self.ask_llm_json(prompt, fallback={"case_type": "unknown", "confidence": 0.0})
        return AgentResult(
            agent_name=self.name,
            status="success",
            data=result,
            confidence=result.get("confidence", 0.5),
        )

    def _extract_entities(self, task: dict) -> AgentResult:
        """Extract named entities from legal text."""
        text = task.get("text", "")
        prompt = f"""Extract all named entities from this Thai legal document.

Text: {text[:3000]}

Respond in JSON:
{{
    "persons": ["names of people"],
    "organizations": ["company/org names"],
    "dates": ["dates mentioned"],
    "amounts": ["monetary amounts"],
    "locations": ["places"],
    "laws": ["referenced laws/regulations"],
    "case_numbers": ["case reference numbers"]
}}"""

        result = self.ask_llm_json(prompt, fallback={"persons": [], "dates": [], "amounts": []})
        return AgentResult(agent_name=self.name, status="success", data=result)

    def _validate_document(self, task: dict) -> AgentResult:
        """Check if a document has all required fields for a legal case."""
        text = task.get("text", "")
        case_type = task.get("case_type", "unknown")

        prompt = f"""Evaluate if this Thai legal document is complete for filing a {case_type} case.

Document: {text[:3000]}

Check for:
1. Party identification (plaintiff/defendant)
2. Dates of events
3. Monetary claims (if applicable)
4. Evidence references
5. Legal basis

Respond in JSON:
{{
    "is_valid": true/false,
    "score": 0.0-1.0,
    "present_fields": ["fields found"],
    "missing_fields": ["fields missing"],
    "suggestions": ["improvement suggestions in Thai"]
}}"""

        result = self.ask_llm_json(prompt, fallback={"is_valid": False, "score": 0.0})
        return AgentResult(
            agent_name=self.name,
            status="success",
            data=result,
            confidence=result.get("score", 0.0),
        )
