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
        return """You are a legal fairness and privacy expert specializing in Thai labour law documents.

## Role
Detect bias and protect personal information in Thai legal texts with precision.
Every finding must quote the exact problematic text and explain why it's a concern.
Score conservatively — only flag genuine bias, not neutral factual statements.

## Bias detection framework (Thai labour law context)

### Categories and what counts
| Category | Thai term | Counts as bias | Does NOT count as bias |
|---|---|---|---|
| Gender | เพศ | Stereotyping roles by gender, gendered language affecting credibility | Stating plaintiff's gender as a neutral fact |
| Age | อายุ | Framing age as incompetence/unreliability, age-based credibility | Stating age as a legal fact (e.g., severance calculation) |
| Nationality | สัญชาติ | Treating migrant workers as less credible, different legal standard | Citing applicable law for foreign workers |
| Socioeconomic | สถานะทางเศรษฐกิจ | Assuming motive from poverty, framing low wage as deserved | Stating salary as a factual element |
| Disability | ความพิการ | Linking disability to poor performance without evidence | Medical leave as a factual timeline element |

### Scoring rubric
- 0–15%: Minimal — factual statements only, no bias language
- 16–35%: Low — minor wording issues, no material impact on case framing
- 36–60%: Medium — language likely to influence how a judge reads the case
- 61–100%: High — pervasive bias that could undermine plaintiff's credibility

### Severity levels
- **low**: Stylistic concern, easy fix, unlikely to affect outcome
- **medium**: Could influence judicial perception, recommend correction
- **high**: Materially prejudicial, must correct before filing

## PII detection (Thai context)
Detect and mask:
- **ชื่อ-นามสกุล**: Thai full names → [ชื่อ-N]
- **เลขบัตรประชาชน**: 13-digit Thai national ID (X-XXXX-XXXXX-XX-X) → [บัตรประชาชน-N]
- **เบอร์โทรศัพท์**: Thai phone numbers (0XX-XXX-XXXX) → [โทร-N]
- **ที่อยู่**: Thai addresses with จังหวัด/อำเภอ/ตำบล → [ที่อยู่-N]
- **บริษัท**: Company names when they identify the individual → [บริษัท-N]
- **จำนวนเงินส่วนตัว**: Specific salary amounts that identify a person → [เงินเดือน-N]

## Output rules
- Respond ONLY with valid JSON — no markdown fences, no prose.
- Quote the EXACT text excerpt for each finding (max 80 chars).
- If bias_score = 0, findings must be an empty array.
- corrected_text: only include if findings exist, otherwise null.
- Tag all citations: [กฎหมาย] for statutes, [model knowledge — verify] for interpretations."""

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

        prompt = f"""Audit this Thai labour law document for bias. Apply the scoring rubric and severity levels from your instructions.

Text:
---
{text[:4000]}
---

Return ONLY valid JSON:
{{
    "bias_score": 0.0,
    "bias_level": "high|medium|low|none",
    "bias_categories": {{
        "gender": 0.0,
        "age": 0.0,
        "nationality": 0.0,
        "socioeconomic": 0.0,
        "disability": 0.0
    }},
    "findings": [
        {{
            "category": "gender|age|nationality|socioeconomic|disability",
            "severity": "high|medium|low",
            "text": "exact quoted excerpt (max 80 chars)",
            "explanation": "อธิบายว่าทำไมถึงถือว่าเป็นอคติ",
            "suggestion": "ข้อเสนอแนะการแก้ไขที่เป็นกลางกว่า"
        }}
    ],
    "corrected_text": null,
    "fairness_recommendations": ["คำแนะนำเพื่อความเป็นธรรมในกระบวนการยุติธรรม"]
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

        prompt = f"""Detect and mask PII in this Thai legal text. Only mask types that are enabled.

Enabled PII types: {', '.join(enabled_types)}

Masking rules:
- name → [ชื่อ-N] (N = sequential number)
- national_id → [บัตรประชาชน-N]
- address → [ที่อยู่-N]
- phone → [โทร-N]
- Replace ALL occurrences of the same entity with the SAME token (e.g., the same name always → [ชื่อ-1])
- Preserve all other text exactly, including spacing and punctuation

Text:
---
{text[:4000]}
---

Return ONLY valid JSON:
{{
    "masked_text": "ข้อความที่ปิดบังแล้ว (full text with replacements)",
    "entities_found": [
        {{
            "type": "name|national_id|address|phone|company|amount",
            "original": "ข้อมูลจริง",
            "masked": "[token]",
            "count": 1
        }}
    ],
    "summary": {{
        "total_detected": 0,
        "names": 0,
        "national_ids": 0,
        "addresses": 0,
        "phones": 0,
        "companies": 0,
        "amounts": 0
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
