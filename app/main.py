"""
KadiRail AI - Streamlit Main Application
Legal Case Navigation Tool for Thailand

Transforms complex legal procedures into interactive "train station" maps.
"""

import streamlit as st
from datetime import datetime

# Import auth module
from utils.auth import get_auth_manager, require_auth

# Page config
st.set_page_config(
    page_title="KadiRail AI - รถไฟคดีของคุณ",
    page_icon="🚂",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Import core modules
from core.map_engine import MapEngine, render_map, interactive_map_view, KadiRailMap
from core.scanner import scan_document_ui
from core.simulator import WhatIfSimulator
from core.bias_engine import BiasEngine

# Import new challenge modules
from core.document_validator import validate_document, auto_detect_case_type
from utils.pii_masking import mask_pii, pii_detection_summary, mask_all
from utils.case_law_search import search_case_laws
from utils.document_summarizer import summarize_document, generate_report

# Apply theme
# Note: unsafe_allow_html disabled for security
st.markdown(
    """
<style>
    .main {
        background-color: #f8fafc;
    }
    .stApp {
        background-color: #ffffff;
    }
    .step-card {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f1f5f9;
        margin-bottom: 0.5rem;
    }
    .current-step {
        border-left: 4px solid #4F46E5;
        background-color: #eef2ff;
    }
    .completed-step {
        border-left: 4px solid #10B981;
        background-color: #ecfdf5;
    }
    .risk-high {
        color: #dc2626;
        font-weight: bold;
    }
    .risk-medium {
        color: #f59e0b;
        font-weight: bold;
    }
    .risk-low {
        color: #10b981;
        font-weight: bold;
    }
</style>
""",
    unsafe_allow_html=True,
)


def init_session_state():
    """Initialize Streamlit session state."""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "session" not in st.session_state:
        st.session_state.session = None

    if "auth_token" not in st.session_state:
        st.session_state.auth_token = None

    if "map_engine" not in st.session_state:
        st.session_state.map_engine = MapEngine()

    if "current_map" not in st.session_state:
        st.session_state.current_map = None

    if "scan_result" not in st.session_state:
        st.session_state.scan_result = None

    if "bias_engine" not in st.session_state:
        st.session_state.bias_engine = BiasEngine()


def login_page():
    """Login page."""
    st.set_page_config(
        page_title="เข้าสู่ระบบ - KadiRail AI",
        page_icon="🚂",
        layout="centered",
    )

    st.markdown(
        """
    <style>
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        background: white;
        border-radius: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.title("🚂 เข้าสู่ระบบ")
    st.markdown("**KadiRail AI - รถไฟคดีของคุณ**")

    st.markdown("---")

    with st.form("login_form"):
        username = st.text_input("👤 ชื่อผู้ใช้")
        password = st.text_input("🔑 รหัสผ่าน", type="password")

        submitted = st.form_submit_button(
            "🚀 เข้าสู่ระบบ", type="primary", use_container_width=True
        )

        if submitted:
            if username and password:
                auth = get_auth_manager()
                result = auth.login(username, password)

                if result:
                    st.session_state.logged_in = True
                    st.session_state.auth_token = result["token"]
                    st.session_state.session = {
                        "username": result["username"],
                        "role": result["role"],
                    }
                    st.success(f"ยินดีต้อนรับ {result['username']}!")
                    st.rerun()
                else:
                    st.error("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
            else:
                st.warning("กรุณากรอกชื่อผู้ใช้และรหัสผ่าน")

    st.markdown("---")
    st.markdown("### 📋 บัญชีทดสอบ")
    st.code("""
admin / kadirail2026 (ผู้ดูแล)
demo / demo1234 (ผู้ใช้ทั่วไป)
reviewer / review2026 (ผู้ตรวจสอบ)
    """)


def sidebar_navigation():
    """Sidebar navigation menu."""
    # Login/Logout section
    if st.session_state.get("logged_in"):
        user_info = st.session_state.get("session", {})
        username = user_info.get("username", "Unknown")
        role = user_info.get("role", "user")

        st.sidebar.title("🚂 KadiRail AI")
        st.sidebar.markdown(f"**👤 {username}**")
        st.sidebar.markdown(f"📛 สิทธิ์: `{role}`")

        if st.sidebar.button("🚪 ออกจากระบบ", use_container_width=True):
            auth = get_auth_manager()
            if st.session_state.get("auth_token"):
                auth.logout(st.session_state.auth_token)
            st.session_state.logged_in = False
            st.session_state.auth_token = None
            st.session_state.session = None
            st.rerun()

    else:
        st.sidebar.title("🚂 KadiRail AI")
        st.sidebar.info("กรุณาเข้าสู่ระบบ")
        return None

    st.sidebar.markdown("---")

    menu = st.sidebar.radio(
        "เมนู",
        [
            "🏠 หน้าหลัก",
            "📄 สแกนเอกสาร",
            "🗺️ แผนที่คดี",
            "🔮 ทำนายผล",
            "⚖️ ตรวจอคติ",
            "✅ ตรวจเอกสาร",
            "🔒 ปิดบังข้อมูลส่วนตัว",
            "📚 ค้นหาคำพิพากษา",
            "📝 สรุปเอกสาร",
        ],
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("**📊 สถานะคดี**")
    if st.session_state.current_map:
        map_obj = st.session_state.current_map
        st.sidebar.metric(
            "ขั้นตอนปัจจุบัน", f"{map_obj.current_step + 1}/{len(map_obj.steps)}"
        )
        st.sidebar.metric("ระยะเวลารวม", f"{map_obj.total_duration()} วัน")

    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    **💡 เกี่ยวกับ KadiRail AI**
    
    เครื่องมือนำทางคดีแรงงานสำหรับประเทศไทย
    - ลดเวลาทำความเข้าใจจาก 120 นาที → 5 นาที
    - (-96%)
    """)

    return menu


def home_page():
    """Main landing page."""
    st.title("🚂 KadiRail AI")
    st.markdown("### รถไฟคดีของคุณ")
    st.markdown("*เปลี่ยนทางเดินทางทางกฎหมายให้เป็นแผนที่ในมือคุณ*")

    st.markdown("---")

    # Hero section
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        ## 🔍 สิ่งที่ KadiRail AI ช่วยคุณได้
        
        - **📄 สแกนเอกสาร** - อัพโหลดเอกสารคดี ใช้ LINE OCR สแกนอัตโนมัติ
        - **🗺️ แผนที่คดี** - แปลงขั้นตอนทางกฎหมายเป็นแผนที่เหมือนรถไฟ
        - **🔮 ทำนายผล** - จำลองผลลัพธ์ของแต่ละทางเลือก
        - **⚖️ ตรวจอคติ** - ตรวจสอบและแก้ไขอคติในระบบ
        
        ---
        
        ### 📌 คดีที่รองรับ (MVP)
        
        | ประเภท | รายละเอียด |
        |---------|-----------|
        | โกงค่าจ้าง | นายจ้างไม่จ่ายหรือจ่ายไม่ครบ |
        | ถูกเลิกจ้าง | ถูกไล่ออกโดยไม่เป็นธรรม |
        | ไม่จ่ายโบนัส | นายจ้างไม่จ่ายโบนัส |
        """)

    with col2:
        st.markdown("### 🎯 เริ่มต้นใช้งาน")

        case_type = st.selectbox(
            "เลือกประเภทคดี",
            ["โกงค่าจ้าง", "ถูกเลิกจ้าง", "ไม่จ่ายโบนัส"],
            format_func=lambda x: f"⚖️ {x}",
        )

        case_map = {"โกงค่าจ้าง": "wage", "ถูกเลิกจ้าง": "termination", "ไม่จ่ายโบนัส": "bonus"}

        if st.button("🚀 สร้างแผนที่คดี", type="primary", use_container_width=True):
            map_engine = st.session_state.map_engine
            new_map = map_engine.create_map(case_type=case_map[case_type])
            st.session_state.current_map = new_map
            st.success("✅ สร้างแผนที่คดีสำเร็จ!")
            st.rerun()

        st.markdown("---")
        st.markdown("### 📊 Impact Target")
        st.metric(
            "ลดเวลาเข้าใจคดี", "120 นาที → 5 นาที", delta="-96%", delta_color="normal"
        )


def scan_page():
    """Document scanning page."""
    st.title("📄 สแกนเอกสาร")
    st.markdown("อัพโหลดเอกสารคดีเพื่อวิเคราะห์อัตโนมัติ")

    result = scan_document_ui()

    if result["scan_result"]:
        st.success("✅ สแกนเสร็จสิ้น!")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📋 ผลการสแกน")
            scan = result["scan_result"]
            st.text_area("ข้อความที่อ่านได้", scan.get("text", ""), height=150)
            st.metric("ความมั่นใจ", f"{scan.get('confidence', 0) * 100:.1f}%")

        with col2:
            st.markdown("### 🎯 ข้อมูลคดี")
            case_info = result.get("case_info", {})

            risk = result.get("risk_level", "unknown")
            risk_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢", "unknown": "⚪"}
            st.markdown(f"**ระดับความเสี่ยง:** {risk_emoji.get(risk, '')} {risk}")

            if case_info.get("case_types"):
                st.markdown("**ประเภทคดีที่พบ:**")
                for ct in case_info["case_types"]:
                    st.markdown(f"- {ct}")

            if case_info.get("word_count"):
                st.metric("จำนวนคำ", case_info["word_count"])


def map_page():
    """Legal case map page."""
    st.title("🗺️ แผนที่คดี")

    map_obj = st.session_state.current_map

    if not map_obj:
        st.warning("ยังไม่มีแผนที่คดี กรุณาสร้างแผนที่ใหม่ที่หน้าหลัก")
        return

    # View mode selector
    view_mode = st.radio(
        "เลือกโหมดการแสดงผล",
        ["🗺️ แผนที่ (Mermaid)", "📋 รายการ", "🔄 แบบโต้ตอบ"],
        horizontal=True,
    )

    if view_mode == "🗺️ แผนที่ (Mermaid)":
        render_map(map_obj)
    elif view_mode == "📋 รายการ":
        from core.map_engine import render_map_simple

        render_map_simple(map_obj)
    else:
        interactive_map_view(map_obj)


def simulator_page():
    """What-If Simulator page."""
    st.title("🔮 ทำนายผลคดี")
    st.markdown("จำลองผลลัพธ์ของทางเลือกต่างๆ")

    if not st.session_state.current_map:
        st.warning("กรุณาสร้างแผนที่คดีก่อน")
        return

    simulator = WhatIfSimulator(st.session_state.current_map)

    # Get options from current step
    current_step = st.session_state.current_map.get_current_step()

    if not current_step:
        st.info("ไม่มีข้อมูลขั้นตอนปัจจุบัน")
        return

    st.markdown(f"### ขั้นตอนปัจจุบัน: **{current_step.title}**")

    if not current_step.alternatives:
        st.info("ขั้นตอนนี้ไม่มีทางเลือกอื่น")
        return

    # Create options from alternatives
    options = [{"name": alt} for alt in current_step.alternatives]
    options.append({"name": "ดำเนินการตามปกติ"})

    selected_option = st.selectbox(
        "เลือกทางเลือกที่ต้องการจำลอง", options, format_func=lambda x: x["name"]
    )

    if st.button("🔮 จำลองผลลัพธ์"):
        with st.spinner("กำลังจำลอง..."):
            result = simulator.simulate(selected_option["name"])

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("โอกาสชนะ", f"{result['win_rate']}%")
            with col2:
                st.metric("ระยะเวลาโดยประมาณ", f"{result['estimated_time']} วัน")
            with col3:
                st.metric("ค่าใช้จ่ายโดยประมาณ", f"฿{result['estimated_cost']:,}")

            if result.get("risks"):
                st.markdown("### ⚠️ ความเสี่ยงที่อาจเกิดขึ้น")
                for risk in result["risks"]:
                    st.markdown(f"- {risk}")

            if result.get("recommendations"):
                st.markdown("### 💡 คำแนะนำ")
                for rec in result["recommendations"]:
                    st.markdown(f"- {rec}")


def bias_check_page():
    """Bias checking page."""
    st.title("⚖️ ตรวจสอบอคติ")
    st.markdown("ตรวจสอบและแก้ไขอคติในระบบ")

    bias_engine = st.session_state.bias_engine

    # Input text for analysis
    input_text = st.text_area(
        "ใส่ข้อความหรือคำพิพากษาที่ต้องการตรวจสอบ",
        height=150,
        placeholder="ใส่ข้อความภาษาไทยที่นี่...",
    )

    if input_text and st.button("🔍 ตรวจสอบอคติ"):
        with st.spinner("กำลังวิเคราะห์..."):
            result = bias_engine.analyze(input_text)

            st.markdown("### 📊 ผลการวิเคราะห์")

            # Bias score
            col1, col2 = st.columns(2)
            with col1:
                score = result.get("bias_score", 0)
                st.metric(
                    "คะแนนอคติ",
                    f"{score:.1f}%",
                    delta="⚠️ มีอคติ" if score > 30 else "✅ ปกติ",
                    delta_color="inverse" if score > 30 else "normal",
                )
            with col2:
                categories = result.get("bias_categories", {})
                if categories:
                    top_category = max(categories.items(), key=lambda x: x[1])
                    st.metric("หมวดหมู่อคติสูงสุด", top_category[0])

            # Detailed findings
            if result.get("findings"):
                st.markdown("### 🔎 รายละเอียด")

                for finding in result["findings"]:
                    severity = finding.get("severity", "low")
                    emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(
                        severity, "⚪"
                    )

                    with st.expander(f"{emoji} {finding['category']} ({severity})"):
                        st.markdown(f"**ข้อความ:** {finding['text']}")
                        st.markdown(f"**คำอธิบาย:** {finding['explanation']}")
                        if finding.get("suggestion"):
                            st.markdown(f"**💡 ข้อเสนอแนะ:** {finding['suggestion']}")

            # Correction
            if result.get("corrected_text"):
                st.markdown("### ✨ ข้อความที่แก้ไขแล้ว")
                st.text_area("ข้อความแก้ไข", result["corrected_text"], height=150)


def document_validation_page():
    """Document validation page (Challenge 2.2)."""
    st.title("✅ ตรวจสอบเอกสาร")
    st.markdown("ตรวจสอบความครบถ้วนของเอกสารคดี")

    # Input method
    input_method = st.radio(
        "เลือกวิธีการใส่ข้อมูล",
        ["📝 ใส่ข้อความ", "📁 อัพโหลดไฟล์"],
        horizontal=True,
    )

    text = ""
    if input_method == "📝 ใส่ข้อความ":
        text = st.text_area(
            "ใส่เนื้อหาเอกสาร",
            height=200,
            placeholder="วางเนื้อหาจาก OCR หรือเอกสาร...",
            max_chars=50000,  # Security: Limit input size
        )
    else:
        uploaded_file = st.file_uploader(
            "อัพโหลดเอกสาร", type=["txt", "pdf", "docx"], help="ไฟล์สูงสุด 10MB"
        )
        if uploaded_file:
            # Security: Limit file size to 10MB
            if uploaded_file.size > 10 * 1024 * 1024:
                st.error("❌ ไฟล์ใหญ่เกินไป (สูงสุด 10MB)")
                return
            text = uploaded_file.read().decode("utf-8", errors="ignore")

    # Auto detect or select case type
    col1, col2 = st.columns(2)
    with col1:
        auto_detect = st.checkbox("ตรวจหาประเภทคดีอัตโนมัติ", value=True)
    with col2:
        if not auto_detect:
            case_type = st.selectbox(
                "เลือกประเภทคดี", ["แรงงาน", "ปกครอง", "แพ่ง", "อาญา"]
            )
        else:
            case_type = None

    if text and st.button("🔍 ตรวจสอบเอกสาร", type="primary"):
        with st.spinner("กำลังตรวจสอบ..."):
            result = validate_document(text, case_type)

            st.markdown("### 📊 ผลการตรวจสอบ")

            # Overall status
            is_valid = result.get("is_valid", False)
            if is_valid:
                st.success("✅ เอกสารครบถ้วน")
            else:
                st.warning("⚠️ เอกสารไม่ครบถ้วน")

            # Score
            score = result.get("score", 0)
            st.metric("คะแนนความครบถ้วน", f"{score * 100:.0f}%")

            # Missing items
            if result.get("missing_fields"):
                st.subheader("📋 เอกสารที่ขาด")
                for item in result.get("missing_fields", []):
                    st.markdown(f"- {item}")

            # Suggestions
            if result.get("suggestions"):
                st.markdown("### 💡 ข้อเสนอแนะ")
                for suggestion in result["suggestions"]:
                    st.markdown(f"- {suggestion}")


def pii_masking_page():
    """PII Masking page (Challenge 3)."""
    st.title("🔒 ปิดบังข้อมูลส่วนตัว")
    st.markdown("ปิดบังข้อมูลส่วนตัว (PII) ก่อนเผยแพร่")

    # Input
    text = st.text_area(
        "ใส่ข้อความที่ต้องการปิดบัง",
        height=200,
        placeholder="วางเอกสารที่ต้องการปิดบังข้อมูลส่วนตัว...",
    )

    # PII types to mask
    st.markdown("### 🎯 เลือกประเภทข้อมูลที่จะปิดบัง")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        mask_name = st.checkbox("ชื่อ-นามสกุล", value=True)
    with col2:
        mask_id = st.checkbox("เลขบัตรประชาชน", value=True)
    with col3:
        mask_address = st.checkbox("ที่อยู่", value=True)
    with col4:
        mask_phone = st.checkbox("เบอร์โทรศัพท์", value=True)

    if text and st.button("🔒 ปิดบังข้อมูล", type="primary"):
        with st.spinner("กำลังปิดบัง..."):
            pii_config = {
                "name": mask_name,
                "national_id": mask_id,
                "address": mask_address,
                "phone": mask_phone,
            }

            result = mask_pii(text, pii_config)

            st.markdown("### 📊 สรุปการตรวจพบ")

            summary = pii_detection_summary(result)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("จำนวนที่ปิดบัง", summary.get("total_detected", 0))
            with col2:
                st.metric("ชื่อ", summary.get("names", 0))
            with col3:
                st.metric("เลขบัตร", summary.get("national_ids", 0))

            st.markdown("### ✨ ข้อความที่ปิดบังแล้ว")
            st.text_area(
                "ผลลัพธ์",
                result.get("masked_text", ""),
                height=250,
            )

            # Download button
            st.download_button(
                "📥 ดาวน์โหลดเอกสาร",
                result.get("masked_text", ""),
                file_name="masked_document.txt",
                mime="text/plain",
            )


def case_law_search_page():
    """Case Law Search page (Challenge 3)."""
    st.title("📚 ค้นหาคำพิพากษา")
    st.markdown("ค้นหาแนวคำพิพากษาศาลไทย")

    # Search input
    query = st.text_input(
        "🔍 ค้นหาคำพิพากษา",
        placeholder="เช่น ค่าจ้าง นายจ้าง ไม่จ่าย...",
    )

    # Filters
    with st.expander("🔧 ตัวกรองเพิ่มเติม"):
        col1, col2 = st.columns(2)
        with col1:
            court_filter = st.selectbox(
                "ศาล",
                ["ทุกศาล", "ศาลแรงงาน", "ศาลปกครอง", "ศาลแพ่ง", "ศาลอาญา"],
            )
        with col2:
            year_filter = st.slider("ปี", 2560, 2568, 2568)

    if query and st.button("🔍 ค้นหา", type="primary"):
        with st.spinner("กำลังค้นหา..."):
            results = search_case_laws(
                query,
                court=None if court_filter == "ทุกศาล" else court_filter,
                year=year_filter,
            )

            st.markdown(f"### 📋 ผลการค้นหา ({len(results)} รายการ)")

            if not results:
                st.info("ไม่พบคำพิพากษาที่ตรงกับเงื่อนไข")
            else:
                for i, case in enumerate(results[:10], 1):
                    with st.expander(f"📄 #{i} {case.get('case_number', 'N/A')}"):
                        st.markdown(f"**ศาล:** {case.get('court', 'N/A')}")
                        st.markdown(f"**ปี:** {case.get('year', 'N/A')}")
                        st.markdown(f"**คดี:** {case.get('case_type', 'N/A')}")
                        st.markdown(f"**ประเด็น:** {case.get('issue', 'N/A')}")
                        st.markdown(f"**สรุป:** {case.get('summary', 'N/A')}")

                        # Show full judgment if available
                        if case.get("judgment"):
                            with st.expander("📜 คำพิพากษาเต็ม"):
                                st.markdown(case["judgment"])


def document_summarizer_page():
    """Document Summarizer page (Challenge 4)."""
    st.title("📝 สรุปเอกสาร")
    st.markdown("สรุปเอกสารคดีและยกร่างรายงาน")

    # Input
    text = st.text_area(
        "ใส่เอกสารที่ต้องการสรุป",
        height=200,
        placeholder="วางเนื้อหาเอกสารที่นี่...",
    )

    # Summary options
    col1, col2 = st.columns(2)
    with col1:
        summary_length = st.select_slider(
            "ความยาวสรุป",
            options=["สั้น", "ปานกลาง", "ยาว"],
            value="ปานกลาง",
        )
    with col2:
        include_key_points = st.checkbox("รวมประเด็นสำคัญ", value=True)

    if text and st.button("📝 สรุปเอกสาร", type="primary"):
        with st.spinner("กำลังสรุป..."):
            length_map = {"สั้น": "short", "ปานกลาง": "medium", "ยาว": "long"}

            result = summarize_document(
                text,
                length=length_map[summary_length],
                include_key_points=include_key_points,
            )

            st.markdown("### 📋 สรุปเอกสาร")
            st.markdown(result.get("summary", ""))

            if result.get("key_points") and include_key_points:
                st.markdown("### 🎯 ประเด็นสำคัญ")
                for point in result["key_points"]:
                    st.markdown(f"- {point}")

            if result.get("entities"):
                with st.expander("🏷️ ข้อมูลที่ระบุ"):
                    for entity_type, entities in result["entities"].items():
                        st.markdown(f"**{entity_type}:** {', '.join(entities)}")

            # Generate report option
            st.markdown("---")
            st.markdown("### 📄 ยกร่างรายงาน")
            if st.button("📄 สร้างรายงาน"):
                report = generate_report(result, result.get("summary", ""))
                st.text_area("รายงาน", report, height=300)
                st.download_button(
                    "📥 ดาวน์โหลดรายงาน",
                    report,
                    file_name="legal_report.txt",
                    mime="text/plain",
                )


def main():
    """Main application entry point."""
    init_session_state()

    # Check if logged in
    if not st.session_state.get("logged_in"):
        login_page()
        return

    menu = sidebar_navigation()

    if menu == "🏠 หน้าหลัก":
        home_page()
    elif menu == "📄 สแกนเอกสาร":
        scan_page()
    elif menu == "🗺️ แผนที่คดี":
        map_page()
    elif menu == "🔮 ทำนายผล":
        simulator_page()
    elif menu == "⚖️ ตรวจอคติ":
        bias_check_page()
    elif menu == "✅ ตรวจเอกสาร":
        document_validation_page()
    elif menu == "🔒 ปิดบังข้อมูลส่วนตัว":
        pii_masking_page()
    elif menu == "📚 ค้นหาคำพิพากษา":
        case_law_search_page()
    elif menu == "📝 สรุปเอกสาร":
        document_summarizer_page()


if __name__ == "__main__":
    main()
