"""
KadiRail Map Engine - Core mapping logic with Mermaid.js visualization.
"""

import streamlit as st
import json
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class LegalStep:
    """A single step in the legal process."""

    id: str
    title: str
    description: str
    duration_days: int
    requirements: List[str]
    optional: bool = False
    parallel: bool = False
    alternatives: List[str] = field(default_factory=list)


@dataclass
class KadiRailMap:
    """
    Legal case navigation map.
    Represents a legal case as a train station map.
    """

    case_type: str
    case_subtype: str
    steps: List[LegalStep]
    current_step: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def get_step(self, step_id: str) -> Optional[LegalStep]:
        """Get step by ID."""
        for step in self.steps:
            if step.id == step_id:
                return step
        return None

    def next_step(self) -> None:
        """Move to next step."""
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1

    def prev_step(self) -> None:
        """Move to previous step."""
        if self.current_step > 0:
            self.current_step -= 1

    def get_current_step(self) -> Optional[LegalStep]:
        """Get current step."""
        if 0 <= self.current_step < len(self.steps):
            return self.steps[self.current_step]
        return None

    def total_duration(self) -> int:
        """Calculate total duration in days."""
        return sum(s.duration_days for s in self.steps if not s.optional)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "case_type": self.case_type,
            "case_subtype": self.case_subtype,
            "steps": [
                {
                    "id": s.id,
                    "title": s.title,
                    "description": s.description,
                    "duration_days": s.duration_days,
                    "requirements": s.requirements,
                    "optional": s.optional,
                    "parallel": s.parallel,
                    "alternatives": s.alternatives,
                }
                for s in self.steps
            ],
            "current_step": self.current_step,
            "metadata": self.metadata,
            "total_duration": self.total_duration(),
        }


class MapEngine:
    """
    Engine for building and managing legal case maps.
    """

    # Case type templates
    CASE_TEMPLATES = {
        "wage": {
            "title": "คดีเรียกค่าจ้าง (Wage Case)",
            "description": "กรณีนายจ้างไม่จ่ายค่าจ้าง หรือจ่ายไม่ครบ",
            "steps": [
                {
                    "id": "step_1",
                    "title": "รวบรวมหลักฐาน",
                    "description": "รวบรวมสัญญาจ้าง สลิปเงินเดือน บันทึกการทำงาน",
                    "duration_days": 7,
                    "requirements": ["สัญญาจ้าง", "สลิปเงินเดือน", "หนังสือบอกเลิกสัญญา"],
                },
                {
                    "id": "step_2",
                    "title": "ยื่นข้อร้องเรียนต่อพนักงานสอบสวน",
                    "description": "ยื่นคำร้องต่อพนักงานสอบสวนประจำท้องที่ หรือ กอ.รมน.ภาค",
                    "duration_days": 1,
                    "requirements": ["คำร้อง", "หลักฐานที่รวบรวม"],
                },
                {
                    "id": "step_3",
                    "title": "สอบสวนข้อเท็จจริง",
                    "description": "พนักงานสอบสวนนัดสอบสวนทั้งสองฝ่าย",
                    "duration_days": 30,
                    "requirements": ["พยานหลักฐาน"],
                    "alternatives": ["ไกล่เกลี่ย", "ดำเนินคดีเอง"],
                },
                {
                    "id": "step_4",
                    "title": "ส่งเรื่องศาลแรงงาน",
                    "description": "หากไม่สามารถตกลงกันได้ ยื่นฟ้องต่อศาลแรงงาน",
                    "duration_days": 1,
                    "requirements": ["ฟ้องศาลแรงงาน", "ค่าธรรมเนียมศาล"],
                },
                {
                    "id": "step_5",
                    "title": "ศาลนัดพิจารณา",
                    "description": "ศาลนัดไต่สวนและพิพากษา",
                    "duration_days": 60,
                    "requirements": ["ทนายความ (แนะนำ)"],
                },
            ],
        },
        "termination": {
            "title": "คดีถูกเลิกจ้าง (Termination Case)",
            "description": "กรณีถูกไล่ออกโดยไม่เป็นธรรม",
            "steps": [
                {
                    "id": "step_1",
                    "title": "ตรวจสอบสิทธิ์",
                    "description": "ตรวจสอบว่าการเลิกจ้างชอบด้วยกฎหมายหรือไม่",
                    "duration_days": 7,
                    "requirements": ["สัญญาจ้าง", "เอกสารการเลิกจ้าง"],
                },
                {
                    "id": "step_2",
                    "title": "ยื่นข้อร้องเรียน",
                    "description": "ยื่นข้อร้องเรียนต่อกรมสวัสดิการและคุ้มครองแรงงาน",
                    "duration_days": 1,
                    "requirements": ["คำร้อง", "เอกสาร"],
                },
                {
                    "id": "step_3",
                    "title": "ไกล่เกลี่ย",
                    "description": "นัดไกล่เกลี่ยระหว่างนายจ้างและลูกจ้าง",
                    "duration_days": 15,
                    "requirements": [],
                    "alternatives": ["ฟ้องศาลโดยตรง"],
                },
                {
                    "id": "step_4",
                    "title": "ยื่นฟ้องศาล",
                    "description": "ยื่นฟ้องต่อศาลแรงงานกลาง/ภาค",
                    "duration_days": 1,
                    "requirements": ["ฟ้อง", "ค่าธรรมเนียม"],
                },
                {
                    "id": "step_5",
                    "title": "พิจารณาคดี",
                    "description": "ศาลพิจารณาและมีคำพิพากษา",
                    "duration_days": 90,
                    "requirements": ["ทนายความ"],
                },
            ],
        },
        "bonus": {
            "title": "คดีโบนัส (Bonus Case)",
            "description": "กรณีนายจ้างไม่จ่ายโบนัส",
            "steps": [
                {
                    "id": "step_1",
                    "title": "ตรวจสอบสิทธิ์",
                    "description": "ตรวจสอบว่ามีสิทธิ์ได้รับโบนัสตามกฎหมายหรือข้อตกลง",
                    "duration_days": 3,
                    "requirements": ["สัญญาจ้าง", "ข้อบังคับบริษัท"],
                },
                {
                    "id": "step_2",
                    "title": "เจรจา",
                    "description": "เจรจากับนายจ้างโดยตรง",
                    "duration_days": 7,
                    "requirements": [],
                },
                {
                    "id": "step_3",
                    "title": "ยื่นข้อร้อง กสพ.",
                    "description": "ยื่นข้อร้องต่อกรมสวัสดิการและคุ้มครองแรงงาน",
                    "duration_days": 1,
                    "requirements": ["คำร้อง"],
                },
                {
                    "id": "step_4",
                    "title": "ศาลแรงงาน",
                    "description": "ยื่นฟ้องหากเจรจาไม่สำเร็จ",
                    "duration_days": 30,
                    "requirements": ["ฟ้อง"],
                },
            ],
        },
    }

    def __init__(self):
        self.current_map: Optional[KadiRailMap] = None

    def create_map(
        self,
        case_type: str,
        case_subtype: str = "",
        custom_steps: Optional[List[Dict]] = None,
    ) -> KadiRailMap:
        """
        Create a new legal case map.

        Args:
            case_type: Type of case (wage, termination, bonus, etc.)
            case_subtype: Subtype of case
            custom_steps: Optional custom steps

        Returns:
            KadiRailMap instance
        """
        if case_type not in self.CASE_TEMPLATES:
            raise ValueError(f"Unknown case type: {case_type}")

        template = self.CASE_TEMPLATES[case_type]

        if custom_steps:
            steps = [LegalStep(**s) for s in custom_steps]
        else:
            steps = [LegalStep(**s) for s in template["steps"]]

        self.current_map = KadiRailMap(
            case_type=case_type,
            case_subtype=case_subtype,
            steps=steps,
            metadata={
                "title": template["title"],
                "description": template["description"],
                "created_at": datetime.now().isoformat(),
            },
        )

        return self.current_map

    def get_current_map(self) -> Optional[KadiRailMap]:
        """Get current active map."""
        return self.current_map


def render_map(map_obj: KadiRailMap) -> None:
    """
    Render the legal case map using Mermaid.js.

    Uses streamlit components to embed Mermaid diagram.
    """
    if not map_obj:
        st.warning("ไม่มีแผนที่คดี")
        return

    # Generate Mermaid diagram
    from utils.mermaid_gen import generate_case_map_mermaid

    mermaid_code = generate_case_map_mermaid(map_obj)

    # HTML template for Mermaid.js
    mermaid_html = f"""
    <div id="mermaid-diagram"></div>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ 
            startOnLoad: true,
            theme: 'default',
            themeVariables: {{
                primaryColor: '#4F46E5',
                primaryTextColor: '#fff',
                primaryBorderColor: '#4F46E5',
                lineColor: '#6B7280',
                secondaryColor: '#10B981',
                tertiaryColor: '#F59E0B'
            }},
            flowchart: {{
                useMaxWidth: true,
                htmlLabels: true,
                curve: 'basis'
            }}
        }});
        
        const element = document.getElementById('mermaid-diagram');
        const graphDefinition = `{mermaid_code}`;
        
        await mermaid.run({{
            nodes: [element],
            markdown: graphDefinition
        }});
    </script>
    """

    # Use Streamlit components
    try:
        from streamlit.components.v1 import html

        html(mermaid_html, height=600)
    except ImportError:
        # Fallback for older Streamlit versions
        st.components.v1.html(mermaid_html, height=600)

    # Display metadata
    with st.expander("📋 รายละเอียดแผนที่"):
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📅 ระยะเวลารวม", f"{map_obj.total_duration()} วัน")
            st.metric("📍 จำนวนขั้นตอน", f"{len(map_obj.steps)} ขั้น")
        with col2:
            st.markdown("**ประเภท:** " + map_obj.metadata.get("title", ""))
            st.markdown("**สถานะ:** ขั้นตอนที่ " + str(map_obj.current_step + 1))


def render_map_simple(map_obj: KadiRailMap) -> None:
    """
    Simplified map rendering without Mermaid (fallback).
    """
    if not map_obj:
        return

    st.subheader(f"🗺️ แผนที่คดี: {map_obj.metadata.get('title', map_obj.case_type)}")

    # Timeline view
    for i, step in enumerate(map_obj.steps):
        with st.expander(f"ขั้นตอนที่ {i + 1}: {step.title}"):
            st.markdown(f"**รายละเอียด:** {step.description}")
            st.markdown(f"**ระยะเวลา:** {step.duration_days} วัน")
            if step.requirements:
                st.markdown("**เอกสารที่ต้องเตรียม:**")
                for req in step.requirements:
                    st.markdown(f"- {req}")
            if step.optional:
                st.caption("⏭️ ขั้นตอนนี้เป็นทางเลือก")


def interactive_map_view(map_obj: KadiRailMap) -> None:
    """
    Interactive map view with navigation.
    """
    st.subheader("🗺️ แผนที่คดีแบบโต้ตอบ")

    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ ก่อนหน้า") and map_obj.current_step > 0:
            map_obj.prev_step()
            st.rerun()
    with col2:
        current = map_obj.get_current_step()
        if current:
            st.markdown(f"**ขั้นตอนที่ {map_obj.current_step + 1}/{len(map_obj.steps)}**")
            st.progress((map_obj.current_step + 1) / len(map_obj.steps))
    with col3:
        if st.button("ถัดไป ➡️") and map_obj.current_step < len(map_obj.steps) - 1:
            map_obj.next_step()
            st.rerun()

    # Current step details
    current = map_obj.get_current_step()
    if current:
        st.markdown("### " + current.title)
        st.markdown(current.description)

        col1, col2 = st.columns(2)
        with col1:
            st.info(f"⏱️ ระยะเวลา: {current.duration_days} วัน")
        with col2:
            if current.optional:
                st.caption("⏭️ ขั้นตอนเลือกได้")
            if current.parallel:
                st.caption("🔄 ทำคู่กับขั้นตอนอื่นได้")

        if current.requirements:
            st.markdown("#### 📄 เอกสารที่ต้องเตรียม:")
            for req in current.requirements:
                st.markdown(f"- {req}")

        if current.alternatives:
            st.markdown("#### 🔀 ทางเลือก:")
            for alt in current.alternatives:
                st.markdown(f"- {alt}")

    # Summary
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("ระยะเวลารวม", f"{map_obj.total_duration()} วัน")
    with col2:
        completed = map_obj.current_step + 1
        remaining = len(map_obj.steps) - completed
        st.metric("ขั้นตอนคงเหลือ", f"{remaining}")
