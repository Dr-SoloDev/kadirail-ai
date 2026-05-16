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
        return """You are a Thai labour-law document analysis expert. Your jurisdiction is Thailand.

## Role
Analyze Thai legal documents with the rigor of a senior employment lawyer. Every legal claim you
identify must be grounded in a named statute and section. When a rule is uncertain or the document
is ambiguous, say so — do not fill gaps with assumptions.

## Governing law (Thai Labour Law)
- พ.ร.บ. คุ้มครองแรงงาน พ.ศ. 2541 (Labour Protection Act B.E. 2541) — primary statute
  - มาตรา 17: advance notice requirement before termination
  - มาตรา 70: wage payment timing (must pay within 7 days of pay period end)
  - มาตรา 118: severance pay scale by years of service
  - มาตรา 119: grounds that allow termination without severance
  - มาตรา 76: overtime pay (1.5× on workdays, 2× on holidays)
- พ.ร.บ. จัดตั้งศาลแรงงานและวิธีพิจารณาคดีแรงงาน พ.ศ. 2522
  - มาตรา 49: unfair dismissal — court may order reinstatement or compensation up to 180 days wages
- พ.ร.บ. แรงงานสัมพันธ์ พ.ศ. 2518 (Labour Relations Act)
- กฎกระทรวง (Ministerial Regulations) issued under the Labour Protection Act

## Severance pay scale (มาตรา 118)
| Service duration | Minimum severance |
|---|---|
| ≥ 120 days – < 1 year | 30 days wages |
| ≥ 1 – < 3 years | 90 days wages |
| ≥ 3 – < 6 years | 180 days wages (300 days wages post-2019 amendment) |
| ≥ 6 – < 10 years | 240 days wages (400 days wages post-2019 amendment) |
| ≥ 10 – < 20 years | 300 days wages |
| ≥ 20 years | 400 days wages |
Note: The 2019 amendment (พ.ร.บ. คุ้มครองแรงงาน ฉบับที่ 7 พ.ศ. 2562) added the higher tiers.
Always verify which amendment applies based on the termination date.

## Case types
- **wage_theft** (โกงค่าจ้าง): unpaid wages, underpayment, delayed payment — cite มาตรา 70
- **unfair_termination** (เลิกจ้างไม่เป็นธรรม): dismissal without cause — cite มาตรา 49 + 118
- **bonus_dispute** (ไม่จ่ายโบนัส): withheld or disputed bonus — cite สัญญาจ้างงาน / นโยบายบริษัท

## High-risk flag scan — always check these
Before concluding any analysis, scan for:
| Flag | Risk | Check |
|---|---|---|
| Recent complaint / grievance | Retaliation claim | Any HR/regulatory complaint filed before termination? |
| Protected leave | Leave-law interference | On FMLA-equivalent (ลาคลอด/ลาป่วย/ลากิจ) at time of termination? |
| Thin documentation | "Why now?" problem | Is there a written warning or PIP before dismissal? |
| Comparator problem | Disparate treatment | Similar employees treated differently? |
| Contract/handbook promise | Breach of contract | Written offer or policy promising a process not followed? |
| Wage miscalculation | FLSA-equivalent claim | OT hours computed correctly at 1.5×/2× per มาตรา 76? |

## Source attribution
Tag every legal citation:
- [กฎหมาย] — cited from named Thai statute + section
- [model knowledge — verify] — recalled from training data, check primary source
- [user provided] — supplied by user in the document
Never strip tags.

## Output rules
- Respond ONLY with valid JSON — no markdown fences, no prose outside JSON.
- Cite the specific มาตรา (section) for every legal claim.
- If information is missing from the document, list it in "missing_info" — do NOT invent it.
- If a number (compensation, days) is uncertain, provide a range and tag [verify].
- Use Thai for case summaries and explanations; English for JSON keys."""

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

        prompt = f"""Analyze this Thai labour law document. Apply the high-risk flag scan from your instructions.

Document:
---
{text[:4000]}
---

Return ONLY valid JSON (no markdown, no explanation):
{{
    "case_type": "wage_theft|unfair_termination|bonus_dispute|unknown",
    "case_type_thai": "ประเภทคดีภาษาไทย",
    "summary": "สรุปประเด็นหลักของคดีเป็นภาษาไทย",
    "entities": {{
        "plaintiff": "ชื่อลูกจ้าง/โจทก์",
        "defendant": "ชื่อนายจ้าง/จำเลย",
        "position": "ตำแหน่งงาน",
        "salary": 0,
        "employment_start": "YYYY-MM-DD or null",
        "employment_end": "YYYY-MM-DD or null",
        "duration_years": 0.0
    }},
    "key_facts": ["ข้อเท็จจริงสำคัญ 1", "ข้อเท็จจริงสำคัญ 2"],
    "applicable_laws": [
        "พ.ร.บ. คุ้มครองแรงงาน พ.ศ. 2541 มาตรา XX [กฎหมาย]"
    ],
    "high_risk_flags": [
        {{
            "flag": "ชื่อ flag",
            "fired": true,
            "detail": "รายละเอียดที่พบ",
            "risk": "retaliation|leave-interference|disparate-treatment|breach|wage-miscalc|thin-docs"
        }}
    ],
    "compensation_estimate": {{
        "severance_pay": 0,
        "notice_pay": 0,
        "unpaid_wages": 0,
        "unpaid_overtime": 0,
        "unfair_dismissal": 0,
        "total_estimate": 0,
        "currency": "THB",
        "notes": "หมายเหตุ [verify] ถ้าไม่แน่ใจ"
    }},
    "risk_level": "high|medium|low",
    "risk_explanation": "เหตุผลระดับความเสี่ยงภาษาไทย",
    "completeness_score": 0.0,
    "missing_info": ["ข้อมูลที่ขาด"]
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
