"""
Document Scanner with LINE OCR API integration.
"""

import base64
import hashlib
import hmac
from typing import Optional

import streamlit as st


class DocumentScanner:
    """Scanner using LINE OCR API for document text extraction."""

    def __init__(self, channel_id: str, channel_secret: str, channel_access_token: str):
        self.channel_id = channel_id
        self.channel_secret = channel_secret
        self.channel_access_token = channel_access_token
        self.api_url = "https://api.line.me/v2/bot/message/n/reply"

    def _generate_signature(self, body: bytes) -> str:
        """Generate LINE API signature."""
        signature = hmac.new(
            self.channel_secret.encode("utf-8"), body, hashlib.sha256
        ).digest()
        return base64.b64encode(signature).decode("utf-8")

    def scan_document(self, image_data: bytes) -> dict:
        """
        Scan document using LINE OCR API.

        Args:
            image_data: Raw image bytes (from uploaded file)

        Returns:
            dict with keys: text, confidence, words
        """
        # LINE OCR endpoint (using Vision API)
        headers = {
            "Authorization": f"Bearer {self.channel_access_token}",
            "Content-Type": "application/json",
        }

        # Convert image to base64
        image_base64 = base64.b64encode(image_data).decode("utf-8")

        # Call LINE OCR API
        # Note: Using LINE Messaging API for simplicity
        # In production, you might use LINE Vision API or other OCR service

        payload = {"image": {"type": "base64", "data": image_base64}}

        # For demo purposes, using a mock response structure
        # In production, replace with actual LINE Vision API call
        try:
            # This would be the actual LINE API call:
            # response = requests.post(
            #     "https://api.line.me/v2/bot/vision/analyze",
            #     headers=headers,
            #     json=payload,
            #     timeout=30
            # )
            # result = response.json()

            # Mock response for demo
            return {
                "text": "",
                "confidence": 0.0,
                "words": [],
                "raw_response": None,
                "error": "LINE OCR API requires LINE Vision API subscription. Using mock mode.",
            }

        except Exception as e:
            return {
                "text": "",
                "confidence": 0.0,
                "words": [],
                "raw_response": None,
                "error": str(e),
            }

    def scan_from_file(self, uploaded_file) -> dict:
        """Scan from Streamlit uploaded file."""
        image_data = uploaded_file.read()
        return self.scan_document(image_data)

    def extract_case_info(self, ocr_result: dict) -> dict:
        """
        Extract case information from OCR result.

        Args:
            ocr_result: Result from scan_document()

        Returns:
            dict with extracted case info
        """
        text = ocr_result.get("text", "")

        # Keywords for labor case types (Thai)
        case_keywords = {
            "wage": ["ค่าจ้าง", "เงินเดือน", "ชั่วโมงทำงาน", "OT", "ล่วงเวลา"],
            "termination": ["เลิกจ้าง", "ไล่ออก", "ปลด", "ให้ออก"],
            "social": ["ประกันสังคม", "สิทธิประโยชน์", "เงินช่วยเหลือ"],
            "bonus": ["โบนัส", "ค่าตอบแทน", "ปันผล"],
        }

        detected_types = []
        for case_type, keywords in case_keywords.items():
            if any(kw in text for kw in keywords):
                detected_types.append(case_type)

        return {
            "case_types": detected_types,
            "full_text": text,
            "confidence": ocr_result.get("confidence", 0.0),
            "word_count": len(text.split()),
        }

    def get_risk_level(self, case_info: dict) -> str:
        """Determine risk level based on case information."""
        case_types = case_info.get("case_types", [])

        if not case_types:
            return "unknown"

        # Simple risk scoring
        high_risk = ["termination"]
        medium_risk = ["wage", "bonus"]

        if any(ct in high_risk for ct in case_types):
            return "high"
        elif any(ct in medium_risk for ct in case_types):
            return "medium"
        else:
            return "low"


@st.cache_resource
def create_scanner() -> Optional[DocumentScanner]:
    """
    Create scanner instance from Streamlit secrets.

    Returns:
        DocumentScanner instance or None if not configured
    """
    try:
        # Try to get from Streamlit secrets
        if hasattr(st, "secrets"):
            secrets = st.secrets
            if "LINE_CHANNEL_ID" in secrets:
                return DocumentScanner(
                    channel_id=secrets["LINE_CHANNEL_ID"],
                    channel_secret=secrets["LINE_CHANNEL_SECRET"],
                    channel_access_token=secrets["LINE_CHANNEL_ACCESS_TOKEN"],
                )
    except Exception:
        pass

    return None


def scan_document_ui() -> dict:
    """
    Streamlit UI for document scanning.

    Returns:
        dict with scan results
    """
    st.subheader("📄 สแกนเอกสาร")

    scanner = create_scanner()

    if scanner is None:
        st.info("⚠️ LINE OCR API ยังไม่ได้ตั้งค่า กำลังใช้โหมดทดลอง")
        st.markdown("""
        **การตั้งค่า LINE OCR:**
        เพิ่ม secrets ใน `.streamlit/secrets.toml`:
        ```toml
        LINE_CHANNEL_ID = "your_channel_id"
        LINE_CHANNEL_SECRET = "your_channel_secret"
        LINE_CHANNEL_ACCESS_TOKEN = "your_access_token"
        ```
        """)

    uploaded_file = st.file_uploader(
        "อัพโหลดเอกสาร (ภาพหรือ PDF)",
        type=["jpg", "jpeg", "png", "pdf"],
        help="รองรับไฟล์ภาพและ PDF",
    )

    if uploaded_file is not None:
        with st.spinner("กำลังสแกนเอกสาร..."):
            # Create scanner (or mock)
            if scanner:
                result = scanner.scan_from_file(uploaded_file)
            else:
                # Mock result for demo
                result = {
                    "text": "[Mock OCR] ค่าจ้าง 15,000 บาท/เดือน แผนกผลิต บริษัท เอบีซี จำกัด",
                    "confidence": 0.85,
                    "words": ["ค่าจ้าง", "15000", "บาท", "บริษัท", "ABC"],
                    "raw_response": None,
                    "error": None,
                }

            if result.get("error"):
                st.warning(f"เกิดข้อผิดพลาด: {result['error']}")

            # Extract case info
            if scanner:
                case_info = scanner.extract_case_info(result)
                risk_level = scanner.get_risk_level(case_info)
            else:
                case_info = {
                    "case_types": ["wage"],
                    "full_text": result.get("text", ""),
                    "confidence": result.get("confidence", 0.0),
                }
                risk_level = "medium"

            return {
                "scan_result": result,
                "case_info": case_info,
                "risk_level": risk_level,
                "uploaded_file": uploaded_file,
            }

    return {
        "scan_result": None,
        "case_info": None,
        "risk_level": None,
        "uploaded_file": None,
    }
