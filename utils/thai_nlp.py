import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ThaiLegalKeyword:
    term: str
    category: str
    weight: float


LABOR_CASE_KEYWORDS = {
    "ชำระค่าจ้าง": "wage",
    "ค่าจ้างขั้นต่ำ": "wage",
    "ค่าล่วงเวลา": "overtime",
    "ค่าทำงานวันหยุด": "holiday",
    "ค่าทำงานในวันสังคม": "holiday",
    "ไล่ออก": "termination",
    "เลิกจ้าง": "termination",
    "เลิกสัญญา": "termination",
    "เสียหาย": "damages",
    "ชดเชย": "compensation",
    "เงินทดรอง": "advance",
    "ค่าเสียหาย": "damages",
    "ทุกข์ทรมาน": "suffering",
    "การกระทำที่เป็นธรรม": "fair_action",
    "การเลือกปฏิบัติ": "discrimination",
    "ความเท่าเทียม": "equality",
    "สภาพการจ้าง": "employment",
    "สิทธิประโยชน์": "benefits",
    "ประกันสังคม": "social_security",
    "กองทุนเงินทดรอง": "provident_fund",
    "กองทุนสำรองเลี้ยงชีพ": "provident_fund",
    "ลาป่วย": "leave",
    "ลากิจ": "leave",
    "ลาพักร้อน": "leave",
    "ลาคลอด": "maternity",
    "การลงโทษ": "punishment",
    "การเลื่อนตำแหน่ง": "promotion",
    "การลดเงินเดือน": "salary_reduction",
    "การปรับอัตราเงินเดือน": "salary_adjustment",
    "สัญญาจ้าง": "contract",
    "ระยะเวลาจ้าง": "contract",
    "ทดลองงาน": "probation",
    "พนักงาน": "employee",
    "นายจ้าง": "employer",
    "ลูกจ้าง": "employee",
    "สหภาพแรงงาน": "union",
    "การนัดหยุดงาน": "strike",
    "การประท้วง": "protest",
    "ความปลอดภัย": "safety",
    "สภาพแวดล้อมการทำงาน": "work_environment",
    "อุบัติเหตุ": "accident",
    "โรคจากการทำงาน": "occupational_disease",
    "ค่าตอบแทน": "compensation",
    "การคืนเงิน": "refund",
    "การชำระเงิน": "payment",
}


CASE_TYPES = {
    "ค่าจ้าง": "Labor Case - Wage Dispute",
    "ค่าล่วงเวลา": "Labor Case - Overtime Payment",
    "ค่าทำงานวันหยุด": "Labor Case - Holiday Work",
    "ไล่ออก": "Labor Case - Unfair Dismissal",
    "เลิกจ้าง": "Labor Case - Termination",
    "เสียหาย": "Labor Case - Damages",
    "ชดเชย": "Labor Case - Compensation",
    "ทุกข์ทรมาน": "Labor Case - Mental Distress",
    "การเลือกปฏิบัติ": "Labor Case - Discrimination",
    "สภาพการจ้าง": "Labor Case - Employment Condition",
    "ประกันสังคม": "Labor Case - Social Security",
    "ลาป่วย": "Labor Case - Sick Leave",
    "ลาคลอด": "Labor Case - Maternity Leave",
    "การลงโทษ": "Labor Case - Unfair Punishment",
    "การเลื่อนตำแหน่ง": "Labor Case - Promotion",
    "การลดเงินเดือน": "Labor Case - Salary Reduction",
}


def detect_case_type(text: str) -> List[Dict[str, Any]]:
    text = text.lower()
    matches = []

    for keyword, category in LABOR_CASE_KEYWORDS.items():
        if keyword in text:
            matches.append(
                {
                    "keyword": keyword,
                    "category": category,
                    "case_type": CASE_TYPES.get(keyword, "Labor Case - Other"),
                    "position": text.find(keyword),
                }
            )

    matches.sort(key=lambda x: x["position"])
    return matches


def extract_claim_amount(text: str) -> Optional[float]:
    patterns = [
        r"(\d[\d,]*)[\s-]*บาท",
        r"ค่าสินไหม\s*[ทด]*\s*(\d[\d,]*)",
        r"(\d[\d,]*)[\s,-]*万",
        r"฿\s*(\d[\d,]*)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            amount_str = match.group(1).replace(",", "")
            return float(amount_str)

    return None


def extract_dates(text: str) -> List[Dict[str, str]]:
    dates = []

    date_patterns = [
        (r"(\d{1,2})\s*/\s*(\d{1,2})\s*/\s*(\d{4})", "dd/mm/yyyy"),
        (r"(\d{1,2})\s*เดือน\s*(\w+)\s*พ\.ศ\.\s*(\d{4})", "dd month be"),
        (r"(\d{4})-(\d{2})-(\d{2})", "yyyy-mm-dd"),
    ]

    for pattern, format_type in date_patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            dates.append(
                {
                    "full_match": match.group(0),
                    "format": format_type,
                    "groups": match.groups(),
                }
            )

    return dates


def extract_parties(text: str) -> Dict[str, Optional[str]]:
    parties: Dict[str, Optional[str]] = {"plaintiff": None, "defendant": None}

    plaintiff_patterns = [
        r"(โจทก์|ผู้ฟ้องคดี)\s*[:\-]?\s*([^,\n]+)",
        r"นาย\s+(\w+)\s+ฟ้อง",
        r"นางสาว\s+(\w+)\s+ฟ้อง",
        r"นาง\s+(\w+)\s+ฟ้อง",
    ]

    defendant_patterns = [
        r"(จำเลย)\s*[:\-]?\s*([^,\n]+)",
        r"บริษัท\s+([^,\n]+)",
        r"ห้างหุ้นส่วน\s+([^,\n]+)",
    ]

    for pattern in plaintiff_patterns:
        match = re.search(pattern, text)
        if match:
            parties["plaintiff"] = (
                match.group(1) if match.lastindex == 1 else match.group(2)
            )
            break

    for pattern in defendant_patterns:
        match = re.search(pattern, text)
        if match:
            parties["defendant"] = (
                match.group(1) if match.lastindex == 1 else match.group(2)
            )
            break

    return parties


def extract_case_number(text: str) -> Optional[str]:
    patterns = [
        r"(?:คดีหมายเลข|เลขคดี)\s*[:\-]?\s*([ก-๙\d/\-]+)",
        r"([ก-๙]{1,2})\s*/\s*(\d{4})\s*/\s*(\d{4,7})",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)

    return None


def analyze_thai_legal_text(text: str) -> Dict[str, Any]:
    return {
        "case_type": detect_case_type(text),
        "claim_amount": extract_claim_amount(text),
        "dates": extract_dates(text),
        "parties": extract_parties(text),
        "case_number": extract_case_number(text),
    }


def get_recommended_offices(case_type: str, case_category: str) -> List[Dict[str, str]]:
    office_map = {
        "wage": [
            {"office": "สำนักงานสวัสดิการและคุ้มครองแรงงาน", "province": "กรุงเทพมหานคร"},
            {"office": "สำนักงานบังคับคดีแรงงาน", "province": "กรุงเทพมหานคร"},
        ],
        "termination": [
            {"office": "ศาลแรงงานกลาง", "province": "กรุงเทพมหานคร"},
            {"office": "สำนักงานสวัสดิการและคุ้มครองแรงงาน", "province": "กรุงเทพมหานคร"},
        ],
        "discrimination": [
            {"office": "คณะกรรมการคุ้มครองสิทธิ", "province": "กรุงเทพมหานคร"},
            {"office": "สำนักงานสวัสดิการและคุ้มครองแรงงาน", "province": "กรุงเทพมหานคร"},
        ],
    }

    return office_map.get(
        case_category,
        [
            {"office": "สำนักงานสวัสดิการและคุ้มครองแรงงาน", "province": "กรุงเทพมหานคร"},
        ],
    )
