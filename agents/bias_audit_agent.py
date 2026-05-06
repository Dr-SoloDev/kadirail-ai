"""
KadiRail AI - Bias Audit Agent
Detects bias in legal texts and masks PII data.
Replaces rule-based bias_engine.py and pii_masking.py with LLM-powered analysis.
"""

from typing import Any, Optional

from agents.base_agent import AgentResult, BaseAgent
from services.llm_service import LLMService


class BiasAuditAgent(BaseAgent):
    """
    Agent responsible for:
    - Detecting bias in legal texts (gender, age, nationality, socioeconomic)
    - Suggesting debiased alternatives
    - PII detection and masking
    - Fairness scoring
    """

    def __init__(self, llm: Optional[LLMService] = None):
        super().__init__(
            name="BiasAuditAgent",
            description="Detects bias in legal texts and protects personal information",
            llm=llm,
        )

    @property
    def system_prompt(self) -> str:
        return """You are a legal fairness and privacy expert specializing in Thai law.

Your responsibilities:
1. BIAS DETECTION: Identify language that may indicate bias based on gender, age,
   nationality, socioeconomic status, or ethnicity in legal documents.
2. PII PROTECTION: Detect and mask personally identifiable information including
   Thai national IDs (เลขบัตรประชาชน), names, addresses, phone numbers.
3. FAIRNESS AUDIT: Score documents for overall fairness and suggest improvements.

Thai PII patterns:
- National ID: X-XXXX-XXXXX-XX-X (13 digits)
- Phone: 0XX-XXX-XXXX or 0XXXXXXXX
- Names: Thai names (ชื่อ-นามสกุล)
- Addresses: Thai addresses with จังหวัด/อำเภอ/ตำบล

Bias categories in Thai legal context:
- เพศ (Gender): ผู้ชาย/ผู้หญิง stereotypes
- อายุ (Age): discrimination against young/old workers
- สัญชาติ (Nationality): bias against migrant workers
- สถานะทางเศรษฐกิจ (Socioeconomic): class-based assumptions

Always be thorough and precise. Respond in the requested format."""

    def execute(self, task: dict[str, Any]) -> AgentResult:
        action = task.get("action", "audit")

        if action == "audit":
            return self._audit_bias(task)
        elif action == "mask_pii":
            return self._mask_pii(task)
        elif action == "full_audit":
            return self._full_audit(task)
        else:
            return AgentResult(
                agent_name=self.name, status="error", error=f"Unknown action: {action}"
            )

    def _audit_bias(self, task: dict) -> AgentResult:
        """Detect bias in legal text."""
        text = task.get("text", "")
        if not text:
            return AgentResult(
                agent_name=self.name, status="error", error="No text provided"
            )

        prompt = f"""Analyze this Thai legal text for potential bias.

Text:
---
{text[:4000]}
---

Respond in JSON:
{{
    "bias_score": 0.0-100.0,
    "bias_level": "high|medium|low|none",
    "bias_categories": {{
        "gender": 0.0-100.0,
        "age": 0.0-100.0,
        "nationality": 0.0-100.0,
        "socioeconomic": 0.0-100.0
    }},
    "findings": [
        {{
            "category": "bias category",
            "severity": "high|medium|low",
            "text": "problematic text excerpt",
            "explanation": "คำอธิบายภาษาไทย",
            "suggestion": "ข้อเสนอแนะการแก้ไข"
        }}
    ],
    "corrected_text": "ข้อความที่แก้ไขอคติแล้ว (full corrected version)",
    "fairness_recommendations": ["คำแนะนำเพื่อความเป็นธรรม"]
}}"""

        result = self.ask_llm_json(prompt, fallback={
            "bias_score": 0.0,
            "bias_level": "none",
            "findings": [],
        })

        return AgentResult(
            agent_name=self.name,
            status="success",
            data=result,
            confidence=0.8,
            reasoning=f"Bias score: {result.get('bias_score', 0)}%",
        )

    def _mask_pii(self, task: dict) -> AgentResult:
        """Detect and mask PII in text."""
        text = task.get("text", "")
        pii_config = task.get("pii_config", {
            "name": True, "national_id": True, "address": True, "phone": True
        })

        enabled_types = [k for k, v in pii_config.items() if v]

        prompt = f"""Detect and mask personally identifiable information (PII) in this Thai text.

PII types to mask: {', '.join(enabled_types)}

Text:
---
{text[:4000]}
---

Rules:
- Replace names with [ชื่อ-X] where X is a number
- Replace national IDs with [เลขบัตร-XXXXX]
- Replace addresses with [ที่อยู่-X]
- Replace phone numbers with [โทร-XXX]
- Keep the rest of the text intact

Respond in JSON:
{{
    "masked_text": "ข้อความที่ปิดบังแล้ว",
    "pii_found": [
        {{
            "type": "name|national_id|address|phone",
            "original": "ข้อมูลจริง",
            "masked": "ข้อมูลที่ปิดบัง",
            "position": "approximate location in text"
        }}
    ],
    "summary": {{
        "total_detected": number,
        "names": number,
        "national_ids": number,
        "addresses": number,
        "phones": number
    }}
}}"""

        result = self.ask_llm_json(prompt, fallback={
            "masked_text": text,
            "pii_found": [],
            "summary": {"total_detected": 0},
        })

        return AgentResult(
            agent_name=self.name,
            status="success",
            data=result,
            confidence=0.85,
            reasoning=f"Found {result.get('summary', {}).get('total_detected', 0)} PII items",
        )

    def _full_audit(self, task: dict) -> AgentResult:
        """Run both bias detection and PII masking."""
        bias_result = self._audit_bias(task)
        pii_result = self._mask_pii(task)

        combined = {
            "bias": bias_result.data,
            "pii": pii_result.data,
            "overall_score": (
                (100 - bias_result.data.get("bias_score", 0)) * 0.5 +
                (100 if not pii_result.data.get("pii_found") else 50) * 0.5
            ),
        }

        return AgentResult(
            agent_name=self.name,
            status="success",
            data=combined,
            confidence=0.8,
            reasoning="Combined bias and PII audit",
        )
