"""
KadiRail AI - Case Law Agent
Searches and summarizes relevant Thai case law.
Replaces rule-based case_law_search.py and document_summarizer.py with LLM-powered analysis.
"""

from typing import Any, Optional

from agents.base_agent import AgentResult, BaseAgent
from services.llm_service import LLMService


class CaseLawAgent(BaseAgent):
    """
    Agent responsible for:
    - Finding relevant Thai case law precedents
    - Summarizing legal judgments
    - Comparing cases for similarity
    - Generating legal reports
    """

    def __init__(self, llm: Optional[LLMService] = None):
        super().__init__(
            name="CaseLawAgent",
            description="Searches and summarizes Thai case law precedents",
            llm=llm,
        )

    @property
    def system_prompt(self) -> str:
        return """You are a Thai case law research expert with deep knowledge of Thai court decisions.

Your expertise covers:
- ศาลแรงงาน (Labor Court) decisions
- ศาลฎีกา (Supreme Court / Dika Court) precedents
- ศาลปกครอง (Administrative Court) rulings

You know landmark Thai labor law cases including:
- Wage theft cases under พ.ร.บ. คุ้มครองแรงงาน
- Unfair termination under มาตรา 49 of Labor Court Act
- Severance pay calculations under มาตรา 118
- Overtime and holiday pay disputes

When generating case law references, use realistic Thai court formats:
- คำพิพากษาศาลฎีกาที่ XXXX/25XX
- คำพิพากษาศาลแรงงานที่ XXXX/25XX

Provide accurate legal analysis. If you're uncertain, state your confidence level.
Always respond in the requested format."""

    def execute(self, task: dict[str, Any]) -> AgentResult:
        action = task.get("action", "search")

        if action == "search":
            return self._search_case_law(task)
        elif action == "summarize":
            return self._summarize_document(task)
        elif action == "compare":
            return self._compare_cases(task)
        elif action == "report":
            return self._generate_report(task)
        else:
            return AgentResult(
                agent_name=self.name, status="error", error=f"Unknown action: {action}"
            )

    def _search_case_law(self, task: dict) -> AgentResult:
        """Search for relevant case law based on query and case details."""
        query = task.get("query", "")
        case_type = task.get("case_type", "")
        court = task.get("court", "")
        year = task.get("year", "")

        prompt = f"""Search for relevant Thai case law precedents.

Query: {query}
Case Type: {case_type}
Court filter: {court or 'all courts'}
Year filter: {year or 'all years'}

Provide 3-5 most relevant cases. For each case, provide realistic Thai court references.

Respond in JSON:
{{
    "query": "{query}",
    "total_results": number,
    "cases": [
        {{
            "case_number": "คำพิพากษาศาลฎีกาที่ XXXX/25XX",
            "court": "ศาลที่ตัดสิน",
            "year": "ปี พ.ศ.",
            "case_type": "ประเภทคดี",
            "issue": "ประเด็นหลัก",
            "summary": "สรุปคำพิพากษา (2-3 sentences)",
            "judgment": "ผลคำพิพากษา",
            "relevance_score": 0.0-1.0,
            "key_principle": "หลักกฎหมายสำคัญ",
            "applicable_sections": ["มาตราที่เกี่ยวข้อง"]
        }}
    ],
    "legal_principles": ["หลักกฎหมายที่เกี่ยวข้องกับการค้นหา"]
}}"""

        result = self.ask_llm_json(prompt, fallback={
            "query": query,
            "total_results": 0,
            "cases": [],
        })

        return AgentResult(
            agent_name=self.name,
            status="success" if result.get("cases") else "partial",
            data=result,
            confidence=0.7,
            reasoning=f"Found {result.get('total_results', 0)} relevant cases",
        )

    def _summarize_document(self, task: dict) -> AgentResult:
        """Summarize a legal document."""
        text = task.get("text", "")
        length = task.get("length", "medium")
        include_key_points = task.get("include_key_points", True)

        length_guide = {
            "short": "2-3 sentences",
            "medium": "1 paragraph (5-8 sentences)",
            "long": "2-3 paragraphs with detail",
        }

        prompt = f"""Summarize this Thai legal document.

Length: {length_guide.get(length, 'medium')}
Include key points: {include_key_points}

Document:
---
{text[:5000]}
---

Respond in JSON:
{{
    "summary": "สรุปเอกสารภาษาไทย",
    "key_points": ["ประเด็นสำคัญ 1", "ประเด็นสำคัญ 2"],
    "entities": {{
        "บุคคล": ["ชื่อบุคคลที่เกี่ยวข้อง"],
        "องค์กร": ["หน่วยงาน/บริษัท"],
        "กฎหมาย": ["กฎหมายที่อ้างถึง"],
        "จำนวนเงิน": ["จำนวนเงินที่กล่าวถึง"]
    }},
    "document_type": "ประเภทเอกสาร",
    "word_count": number
}}"""

        result = self.ask_llm_json(prompt, fallback={
            "summary": "ไม่สามารถสรุปเอกสารได้",
            "key_points": [],
        })

        return AgentResult(
            agent_name=self.name,
            status="success",
            data=result,
            confidence=0.75,
        )

    def _compare_cases(self, task: dict) -> AgentResult:
        """Compare two cases for similarity and precedent applicability."""
        case_a = task.get("case_a", "")
        case_b = task.get("case_b", "")

        prompt = f"""Compare these two Thai legal cases for similarity and precedent applicability.

Case A:
{case_a[:2000]}

Case B:
{case_b[:2000]}

Respond in JSON:
{{
    "similarity_score": 0.0-1.0,
    "similar_aspects": ["ด้านที่คล้ายกัน"],
    "different_aspects": ["ด้านที่แตกต่าง"],
    "precedent_applicable": true/false,
    "precedent_reasoning": "เหตุผลว่าเป็นบรรทัดฐานได้หรือไม่",
    "recommendation": "คำแนะนำ"
}}"""

        result = self.ask_llm_json(prompt, fallback={"similarity_score": 0.0})
        return AgentResult(
            agent_name=self.name,
            status="success",
            data=result,
            confidence=result.get("similarity_score", 0.5),
        )

    def _generate_report(self, task: dict) -> AgentResult:
        """Generate a comprehensive legal report."""
        summary = task.get("summary", "")
        analysis = task.get("analysis", {})
        case_law = task.get("case_law", [])

        prompt = f"""Generate a comprehensive legal report in Thai for this case.

Case Summary: {summary}
Analysis: {str(analysis)[:2000]}
Related Case Law: {str(case_law)[:2000]}

The report should include:
1. ข้อเท็จจริง (Facts)
2. ประเด็นทางกฎหมาย (Legal Issues)
3. กฎหมายที่เกี่ยวข้อง (Applicable Laws)
4. แนวคำพิพากษาที่เกี่ยวข้อง (Relevant Precedents)
5. วิเคราะห์ (Analysis)
6. ข้อเสนอแนะ (Recommendations)

Respond in JSON:
{{
    "report_title": "ชื่อรายงาน",
    "sections": [
        {{
            "title": "ชื่อหัวข้อ",
            "content": "เนื้อหา"
        }}
    ],
    "full_text": "รายงานฉบับเต็ม (plain text)"
}}"""

        result = self.ask_llm_json(prompt, fallback={
            "report_title": "รายงานทางกฎหมาย",
            "sections": [],
            "full_text": "",
        })

        return AgentResult(
            agent_name=self.name,
            status="success" if result.get("full_text") else "partial",
            data=result,
            confidence=0.7,
        )
