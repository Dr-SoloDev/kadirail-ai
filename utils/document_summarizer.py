"""
Document Summarizer Module - สรุปเอกสารคดี
Challenge 4: สรุปเอกสาร ยกร่างรายงาน
"""

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class CaseSummary:
    title: str
    parties: str
    case_type: str
    key_issues: List[str]
    timeline: List[Dict[str, str]]
    claim_amount: str
    current_status: str
    recommendations: List[str]


def extract_parties_from_text(text: str) -> Dict[str, str]:
    """ดึงข้อมูลคู่ความจากเอกสาร"""
    parties = {"plaintiff": None, "defendant": None}

    plaintiff_patterns = [
        r"โจทก์\s*[:\-]?\s*([ก-๙\s]+?)(?:\n|$)",
        r"ฟ้อง\s*[:\-]?\s*([ก-๙\s]+?)(?:\n|$)",
        r"นาย\s+([ก-๙]+)\s+โจทก์",
    ]

    defendant_patterns = [
        r"จำเลย\s*[:\-]?\s*([ก-๙\s]+?)(?:\n|$)",
        r"จำเลย\s+([ก-๙\s]+?)(?:\n|$)",
    ]

    for pattern in plaintiff_patterns:
        match = re.search(pattern, text)
        if match:
            parties["plaintiff"] = match.group(1).strip()
            break

    for pattern in defendant_patterns:
        match = re.search(pattern, text)
        if match:
            parties["defendant"] = match.group(1).strip()
            break

    return parties


def extract_claim_amount(text: str) -> Optional[str]:
    """ดึงมูลค่าความเสียหาย"""
    patterns = [
        r"([\d,]+)\s*บาท",
        r"มูลค่า\s*([\d,]+)\s*บาท",
        r"ค่าสินไหม\s*ทดแทน\s*([\d,]+)\s*บาท",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return f"{match.group(1)} บาท"

    return None


def extract_case_type(text: str) -> str:
    """ดึงประเภทคดี"""
    keywords = {
        "ค่าจ้าง": "คดีแรงงาน ค่าจ้าง",
        "ค่าล่วงเวลา": "คดีแรงงาน ค่าล่วงเวลา",
        "เลิกจ้าง": "คดีแรงงาน การเลิกจ้าง",
        "ไล่ออก": "คดีแรงงาน การไล่ออก",
        "ประกันสังคม": "คดีประกันสังคม",
        "ศาลปกครอง": "คดีปกครอง",
        "ศาลแพ่ง": "คดีแพ่ง",
        "ศาลอาญา": "คดีอาญา",
    }

    text_lower = text.lower()
    for kw, case_type in keywords.items():
        if kw in text_lower:
            return case_type

    return "คดีทั่วไป"


def summarize_labor_case(text: str) -> CaseSummary:
    """สรุปคดีแรงงาน"""
    parties = extract_parties_from_text(text)
    claim_amount = extract_claim_amount(text)
    case_type = extract_case_type(text)

    issues = []
    if "ค่าจ้าง" in text:
        issues.append("ข้อพิพาทเรื่องค่าจ้าง")
    if "เลิกจ้าง" in text or "ไล่ออก" in text:
        issues.append("ข้อพิพาทเรื่องการเลิกจ้าง")
    if "ค่าล่วงเวลา" in text:
        issues.append("ข้อพิพาทเรื่องค่าล่วงเวลา")
    if "ชดเชย" in text:
        issues.append("ข้อพิพาทเรื่องค่าชดเชย")

    recommendations = []
    if len(issues) == 0:
        recommendations.append("ตรวจสอบประเด็นข้อพิพาทเพิ่มเติม")
    if not claim_amount:
        recommendations.append("ระบุมูลค่าความเสียหายให้ชัดเจน")
    if not parties.get("defendant"):
        recommendations.append("ตรวจสอบชื่อจำเลยให้ถูกต้อง")

    return CaseSummary(
        title=f"สรุปคดี{case_type}",
        parties=f"โจทก์: {parties.get('plaintiff', 'ไม่ระบุ')} | จำเลย: {parties.get('defendant', 'ไม่ระบุ')}",
        case_type=case_type,
        key_issues=issues if issues else ["ข้อพิพาทตามคำฟ้อง"],
        timeline=[{"date": "ยื่นฟ้อง", "status": "อยู่ระหว่างดำเนินการ"}],
        claim_amount=claim_amount or "ไม่ระบุ",
        current_status="อยู่ระหว่างพิจารณา",
        recommendations=recommendations if recommendations else ["ดำเนินการตามขั้นตอนศาล"],
    )


def summarize_admin_case(text: str) -> CaseSummary:
    """สรุปคดีปกครอง"""
    parties = extract_parties_from_text(text)
    case_type = "คดีปกครอง"

    issues = []
    if "ฟ้อง" in text and "เพิกถอน" in text:
        issues.append("ขอให้เพิกถอนคำสั่ง")
    if "ผิด" in text and "กฎหมาย" in text:
        issues.append("การกระทำผิดกฎหมาย")
    if "อำนาจ" in text:
        issues.append("ข้อพิพาทเรื่องอำนาจ")

    return CaseSummary(
        title="สรุปคดีปกครอง",
        parties=f"โจทก์: {parties.get('plaintiff', 'ไม่ระบุ')} | จำเลย: {parties.get('defendant', 'ไม่ระบุ')}",
        case_type=case_type,
        key_issues=issues if issues else ["ข้อพิพาทตามคำฟ้อง"],
        timeline=[{"date": "ยื่นฟ้อง", "status": "อยู่ระหว่างดำเนินการ"}],
        claim_amount="ไม่ระบุ",
        current_status="อยู่ระหว่างพิจารณา",
        recommendations=["ตรวจสอบความครบถ้วนของเอกสาร", "เตรียมหลักฐานประกอบ"],
    )


def summarize_document(
    text: str,
    case_type: Optional[str] = None,
    length: str = "medium",
    include_key_points: bool = True,
) -> Dict[str, Any]:
    """
    สรุปเอกสารคดี

    Args:
        text: เนื้อหาเอกสาร
        case_type: ประเภทคดี (auto-detect if None)

    Returns:
        dict with summary
    """
    if case_type is None:
        case_type = extract_case_type(text)

    if "แรงงาน" in case_type or "ประกันสังคม" in case_type:
        summary = summarize_labor_case(text)
    elif "ปกครอง" in case_type:
        summary = summarize_admin_case(text)
    else:
        summary = summarize_labor_case(text)

    return {
        "title": summary.title,
        "parties": summary.parties,
        "case_type": summary.case_type,
        "key_issues": summary.key_issues,
        "timeline": summary.timeline,
        "claim_amount": summary.claim_amount,
        "current_status": summary.current_status,
        "recommendations": summary.recommendations,
    }


def generate_report(case_data: Dict, summary: Dict) -> str:
    """สร้างรายงานคดีอัตโนมัติ"""

    report = f"""
# รายงานสรุปคดี

## ข้อมูลคดี
- **ประเภทคดี:** {summary.get("case_type", "ไม่ระบุ")}
- **มูลค่าความเสียหาย:** {summary.get("claim_amount", "ไม่ระบุ")}
- **สถานะ:** {summary.get("current_status", "ไม่ระบุ")}

## คู่ความ
{summary.get("parties", "ไม่ระบุ")}

## ประเด็นสำคัญ
"""

    for issue in summary.get("key_issues", []):
        report += f"- {issue}\n"

    report += """
## ขั้นตอนต่อไป
"""

    for rec in summary.get("recommendations", []):
        report += f"- {rec}\n"

    report += """
---
สร้างโดย KadiRail AI
"""

    return report
