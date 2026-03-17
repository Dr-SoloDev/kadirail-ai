"""
Document Validation Module - ตรวจสอบความครบถ้วนของเอกสารคดี
Challenge 2.2: ตรวจสอบความครบถ้วนขององค์ประกอบทางกฎหมายและเอกสารประกอบ
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import re


@dataclass
class ValidationResult:
    is_valid: bool
    score: float
    missing_fields: List[str]
    warnings: List[str]
    suggestions: List[str]


LABOR_CASE_REQUIREMENTS = {
    "คำฟ้อง": {
        "required": [
            "ชื่อ-นามสกุลโจทก์",
            "ชื่อ-นามสกุลจำเลย",
            "ที่อยู่คู่ความ",
            "มูลความ",
            "ข้อหา",
            "พฤติการณ์",
            "คำขอ",
            "ลายมือชื่อโจทก์",
            "วันที่ยื่นฟ้อง",
        ],
        "optional": [
            "หลักฐานประกอบ",
            "พยานบุคคล",
            "พยานเอกสาร",
            "คำให้การแก้ฟ้อง",
        ],
    },
    "ทะเบียนบ้านโจทก์": {
        "required": [
            "สำเนาทะเบียนบ้าน",
            "ชื่อ-นามสกุลตรงกับคำฟ้อง",
        ]
    },
    "ทะเบียนบ้านจำเลย": {
        "required": [
            "สำเนาทะเบียนบ้าน หรือ หนังสือรับรองบริษัท",
        ]
    },
    "หลักฐานการทำงาน": {
        "required": [
            "สัญญาจ้าง",
            "หนังสือบอกเลิกสัญญาจ้าง",
            "ใบเสร็จค่าจ้าง",
        ],
        "optional": [
            "บันทึกข้อความ",
            "อีเมล",
            "ภาพถ่าย",
        ],
    },
}


CIVIL_CASE_REQUIREMENTS = {
    "คำฟ้อง": {
        "required": [
            "ชื่อ-นามสกุลโจทก์",
            "ชื่อ-นามสกุลจำเลย",
            "ที่อยู่คู่ความ",
            "มูลความ",
            "ข้อหา",
            "พฤติการณ์",
            "คำขอ",
            "ลายมือชื่อโจทก์",
            "วันที่ยื่นฟ้อง",
            "ค่าขาด",
            "อัตราดอกเบี้ย",
        ],
        "optional": [
            "สัญญา",
            "หนังสือผูกพัน",
            "ใบเสร็จ",
        ],
    },
}


ADMIN_CASE_REQUIREMENTS = {
    "คำฟ้อง": {
        "required": [
            "ชื่อ-นามสกุลโจทก์",
            "ชื่อหน่วยงานจำเลย",
            "ที่อยู่หน่วยงาน",
            "มูลความ (การกระทำที่ผิดกฎหมาย)",
            "ข้อหา (ชอบด้วยกฎหมายที่อ้าง)",
            "พฤติการณ์",
            "คำขอ (ให้เพิกถอน/ให้ปฏิบัติ)",
            "ลายมือชื่อ",
            "วันที่ยื่นฟ้อง",
        ],
        "optional": [
            "หนังสือแจ้งการตัดสินใจ",
            "คำสั่งที่ถูกฟ้อง",
            "หลักฐานประกอบ",
        ],
    },
}


def validate_labor_case(text: str) -> ValidationResult:
    """ตรวจสอบความครบถ้วนของคำฟ้องคดีแรงงาน"""
    missing_fields = []
    warnings = []
    suggestions = []

    text_lower = text.lower()

    for field in LABOR_CASE_REQUIREMENTS["คำฟ้อง"]["required"]:
        found = False

        if "ชื่อ" in field and "นามสกุล" in field:
            found = bool(re.search(r"นาย|นาง|นางสาว|น\.ส\.", text))
        elif "ที่อยู่" in field:
            found = "ที่อยู่" in text_lower or "อ." in text or "ต." in text
        elif "มูลความ" in field:
            found = len(text) > 100
        elif "ข้อหา" in field:
            found = "ข้อหา" in text_lower or "ฟ้องว่า" in text
        elif "พฤติการณ์" in field:
            found = "พฤติการณ์" in text_lower or "เนื่องจาก" in text
        elif "คำขอ" in field:
            found = "คำขอ" in text_lower or "ขอให้" in text
        elif "ลายมือชื่อ" in field:
            found = bool(re.search(r"ลงชื่อ|ลายมือชื่อ", text))
        elif "วันที่" in field:
            found = bool(re.search(r"\d{1,2}/\d{1,2}/\d{4}|วันที่", text))

        if not found:
            missing_fields.append(field)
            suggestions.append(f"กรุณาระบุ{field}")

    if len(text) < 200:
        warnings.append("เนื้อหาคำฟ้องสั้นเกินไป อาจไม่ครบถ้วน")

    if not re.search(r"\d{4}", text):
        warnings.append("ไม่พบปี พ.ศ. ในเอกสาร")

    if not re.search(r"\d[\d,]+", text):
        warnings.append("ไม่พบจำนวนเงินในเอกสาร")

    score = (
        len(LABOR_CASE_REQUIREMENTS["คำฟ้อง"]["required"]) - len(missing_fields)
    ) / len(LABOR_CASE_REQUIREMENTS["คำฟ้อง"]["required"])

    return ValidationResult(
        is_valid=len(missing_fields) == 0,
        score=score,
        missing_fields=missing_fields,
        warnings=warnings,
        suggestions=suggestions,
    )


def validate_admin_case(text: str) -> ValidationResult:
    """ตรวจสอบความครบถ้วนของคำฟ้องคดีปกครอง"""
    missing_fields = []
    warnings = []
    suggestions = []

    text_lower = text.lower()

    for field in ADMIN_CASE_REQUIREMENTS["คำฟ้อง"]["required"]:
        found = False

        if "ชื่อ" in field and "นามสกุล" in field:
            found = bool(re.search(r"นาย|นาง|นางสาว", text))
        elif "ชื่อหน่วยงาน" in field:
            found = (
                "กรม" in text or "สำนัก" in text or "ส่วนราชการ" in text or "บริษัท" in text
            )
        elif "ที่อยู่" in field:
            found = "ที่อยู่" in text_lower
        elif "มูลความ" in field:
            found = len(text) > 150
        elif "ข้อหา" in field:
            found = "ข้อหา" in text_lower or "กฎหมาย" in text_lower
        elif "คำขอ" in field:
            found = (
                "คำขอ" in text_lower or "ขอให้" in text_lower or "เพิกถอน" in text_lower
            )
        elif "ลายมือชื่อ" in field:
            found = bool(re.search(r"ลงชื่อ|ลายมือชื่อ", text))
        elif "วันที่" in field:
            found = bool(re.search(r"\d{1,2}/\d{1,2}/\d{4}", text))

        if not found:
            missing_fields.append(field)
            suggestions.append(f"กรุณาระบุ{field}")

    score = (
        len(ADMIN_CASE_REQUIREMENTS["คำฟ้อง"]["required"]) - len(missing_fields)
    ) / len(ADMIN_CASE_REQUIREMENTS["คำฟ้อง"]["required"])

    return ValidationResult(
        is_valid=len(missing_fields) == 0,
        score=score,
        missing_fields=missing_fields,
        warnings=warnings,
        suggestions=suggestions,
    )


def auto_detect_case_type(text: str) -> str:
    """ตรวจจับประเภทคดีอัตโนมัติ"""
    text_lower = text.lower()

    labor_keywords = ["ค่าจ้าง", "เงินเดือน", "เลิกจ้าง", "ไล่ออก", "แรงงาน", "ศาลแรงงาน"]
    admin_keywords = ["กรม", "สำนัก", "ศาลปกครอง", "คำสั่ง", "กฎหมายปกครอง", "พิพากษา"]
    civil_keywords = ["ทรัพย์สิน", "สัญญา", "หนี้", "ชำระหนี้", "ศาลแพ่ง"]
    criminal_keywords = ["อาญา", "ลักทรัพย์", "ทำร้ายร่างกาย", "ศาลอาญา"]

    labor_score = sum(1 for kw in labor_keywords if kw in text_lower)
    admin_score = sum(1 for kw in admin_keywords if kw in text_lower)
    civil_score = sum(1 for kw in civil_keywords if kw in text_lower)
    criminal_score = sum(1 for kw in criminal_keywords if kw in text_lower)

    scores = {
        "แรงงาน": labor_score,
        "ปกครอง": admin_score,
        "แพ่ง": civil_score,
        "อาญา": criminal_score,
    }

    max_score = max(scores.values()) if scores else 0
    if max_score == 0:
        return "ไม่ระบุ"

    best_case_type = max(scores, key=lambda k: scores.get(k, 0))
    return best_case_type


def validate_document(text: str, case_type: Optional[str] = None) -> Dict[str, Any]:
    """
    ตรวจสอบความครบถ้วนของเอกสาร

    Args:
        text: เนื้อหาจาก OCR
        case_type: ประเภทคดี (auto-detect if None)

    Returns:
        dict with validation results
    """
    if case_type is None:
        case_type = auto_detect_case_type(text)

    if "แรงงาน" in case_type:
        result = validate_labor_case(text)
    elif "ปกครอง" in case_type:
        result = validate_admin_case(text)
    else:
        result = ValidationResult(
            is_valid=True,
            score=1.0,
            missing_fields=[],
            warnings=["ไม่พบรูปแบบคดีที่รองรับ - กรุณาตรวจสอบด้วยตนเอง"],
            suggestions=[],
        )

    return {
        "case_type": case_type,
        "is_valid": result.is_valid,
        "score": result.score,
        "score_percent": f"{result.score * 100:.0f}%",
        "missing_fields": result.missing_fields,
        "warnings": result.warnings,
        "suggestions": result.suggestions,
        "recommendation": "สามารถยื่นฟ้องได้"
        if result.score >= 0.7
        else "กรุณาแก้ไขเอกสารก่อนยื่นฟ้อง",
    }
