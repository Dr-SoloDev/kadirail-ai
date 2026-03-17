"""
Case Law Search Module - ค้นหาแนวคำพิพากษา
Challenge 3: ค้นหาแนวคำพิพากษาได้อย่างแม่นยำ
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class CaseLaw:
    case_number: str
    year: int
    court: str
    parties: str
    issue: str
    principle: str
    holding: str
    keywords: List[str]
    relevance_score: float


SUPREME_COURT_PRECDENTS = [
    {
        "case_number": "๔๑๕๔/๒๕๕๕",
        "year": 2555,
        "court": "ศาลฎีกา",
        "issue": "การไล่ออกโดยไม่เป็นธรรม",
        "principle": "นายจ้างที่ไล่ลูกจ้างออกโดยไม่มีเหตุอันควร ต้องจ่ายค่าชดเชย",
        "holding": "จำเลยไล่โจทก์ออกโดยไม่มีเหตุอันควร ต้องรับผิดชดใช้ค่าจ้างและค่าชดเชย",
        "keywords": ["ไล่ออก", "ไม่เป็นธรรม", "ค่าชดเชย", "ลูกจ้าง"],
    },
    {
        "case_number": "๖๑๑๓/๒๕๕๔",
        "year": 2554,
        "court": "ศาลฎีกา",
        "issue": "ค่าล่วงเวลา",
        "principle": "ลูกจ้างมีสิทธิได้รับค่าล่วงเวลาตามกฎหมาย",
        "holding": "จำเลยไม่จ่ายค่าล่วงเวลาให้โจทก์ ต้องชำระค่าล่วงเวลาพร้อมดอกเบี้ย",
        "keywords": ["ค่าล่วงเวลา", "OT", "ชั่วโมงทำงาน", "สิทธิลูกจ้าง"],
    },
    {
        "case_number": "๓๒๗๑/๒๕๕๓",
        "year": 2553,
        "court": "ศาลฎีกา",
        "issue": "การเลิกจ้างกรณีปรับลดอัตรากำลัง",
        "principle": "การเลิกจ้างเพราะปรับลดอัตรากำลังต้องจ่ายค่าชดเชยตามกฎหมาย",
        "holding": "การเลิกจ้างเป็นธรรมหากมีเหตุผลอันสมควรและจ่ายค่าชดเชยครบถ้วน",
        "keywords": ["เลิกจ้าง", "ปรับลดอัตรากำลัง", "ค่าชดเชย", "ลูกจ้าง"],
    },
    {
        "case_number": "๘๓๔๗/๒๕๕๖",
        "year": 2556,
        "court": "ศาลฎีกา",
        "issue": "การลาป่วยโดยไม่ได้รับอนุญาต",
        "principle": "การลาป่วยติดต่อกันเกินกว่า 3 วันต้องมีใบรับรองแพทย์",
        "holding": "โจทก์ลาป่วยโดยไม่มีใบรับรองแพทย์ถือว่าขาดงานโดยไม่มีเหตุอันควร",
        "keywords": ["ลาป่วย", "ใบรับรองแพทย์", "ขาดงาน", "การลงโทษ"],
    },
    {
        "case_number": "๕๓๒๑/๒๕๕๗",
        "year": 2557,
        "court": "ศาลฎีกา",
        "issue": "สิทธิประโยชน์ตามกฎหมายคุ้มครองแรงงาน",
        "principle": "นายจ้างต้องจ่ายค่าจ้างตรงต่อเวลา ห้ามหักโดยไม่ชอบด้วยกฎหมาย",
        "holding": "การหักค่าจ้างต้องได้รับความยินยอมจากลูกจ้างก่อน",
        "keywords": ["หักค่าจ้าง", "สิทธิลูกจ้าง", "กฎหมายแรงงาน", "ค่าจ้างขั้นต่ำ"],
    },
]

LABOR_COURT_PRECDENTS = [
    {
        "case_number": "น.๑๒๓/๒๕๖๐",
        "year": 2560,
        "court": "ศาลแรงงานกลาง",
        "issue": "ค่าจ้างที่ไม่ได้รับ",
        "principle": "นายจ้างต้องจ่ายค่าจ้างให้ลูกจ้างตรงเวลา",
        "holding": "จำเลยผิดสัญญาจ้าง ไม่จ่ายค่าจ้าง ให้ชำระค่าจ้างพร้อมดอกเบี้ย",
        "keywords": ["ค่าจ้าง", "ไม่จ่าย", "ผิดสัญญา"],
    },
    {
        "case_number": "น.๔๕๖/๒๕๖๑",
        "year": 2561,
        "court": "ศาลแรงงานกลาง",
        "issue": "การเลิกจ้างโดยไม่แจ้งล่วงหน้า",
        "principle": "การเลิกจ้างต้องแจ้งล่วงหน้าตามกฎหมาย",
        "holding": "การเลิกจ้างโดยไม่แจ้งล่วงหน้า ให้จ่ายค่าจ้างแทนการแจ้งล่วงหน้า",
        "keywords": ["เลิกจ้าง", "แจ้งล่วงหน้า", "ค่าจ้างแทน"],
    },
]

ADMIN_COURT_PRECDENTS = [
    {
        "case_number": "อ.๑๐๒๓/๒๕๖๐",
        "year": 2560,
        "court": "ศาลปกครองกลาง",
        "issue": "การอนุญาตที่ผิดกฎหมาย",
        "principle": "เจ้าหน้าที่ต้องปฏิบัติตามกฎหมายอย่างเคร่งครัด",
        "holding": "การอนุญาตที่ขัดต่อกฎหมายเป็นโมฆะ",
        "keywords": ["ศาลปกครอง", "การอนุญาต", "โมฆะ", "เจ้าหน้าที่"],
    },
]


def search_case_laws(
    query: str,
    case_type: str = "labor",
    limit: int = 10,
    court: Optional[str] = None,
    year: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """
    ค้นหาแนวคำพิพากษาตามคำค้น

    Args:
        query: คำค้นหา
        case_type: ประเภทคดี (labor, civil, admin)
        limit: จำนวนผลลัพธ์

    Returns:
        list of matching case laws
    """
    query_lower = query.lower()
    query_keywords = query_lower.split()

    all_precedents = []

    if case_type == "labor":
        all_precedents = SUPREME_COURT_PRECDENTS + LABOR_COURT_PRECDENTS
    elif case_type == "admin":
        all_precedents = ADMIN_COURT_PRECDENTS
    else:
        all_precedents = SUPREME_COURT_PRECDENTS + ADMIN_COURT_PRECDENTS

    scored_precedents = []

    for precedent in all_precedents:
        score = 0.0

        issue_text = precedent["issue"].lower()
        principle_text = precedent["principle"].lower()
        keywords_text = " ".join(precedent["keywords"]).lower()

        for kw in query_keywords:
            if kw in issue_text:
                score += 3.0
            if kw in principle_text:
                score += 2.0
            if kw in keywords_text:
                score += 1.0

        for kw in precedent["keywords"]:
            if kw in query_lower:
                score += 0.5

        if score > 0:
            scored_precedents.append((precedent, score))

    scored_precedents.sort(key=lambda x: x[1], reverse=True)

    results = []
    for precedent, score in scored_precedents[:limit]:
        result = precedent.copy()
        result["relevance_score"] = round(score / 10.0, 2)
        results.append(result)

    return results


def get_case_law_by_issue(issue: str) -> List[Dict[str, Any]]:
    """ค้นหาจากประเด็น"""
    return search_case_laws(issue, limit=3)


def get_related_laws(query: str) -> List[Dict[str, str]]:
    """ค้นหากฎหมายที่เกี่ยวข้อง"""

    law_map = {
        "ค่าจ้าง": "พระราชบัญญัติคุ้มครองแรงงาน พ.ศ. 2541 มาตรา 43-50",
        "เลิกจ้าง": "พระราชบัญญัติคุ้มครองแรงงาน พ.ศ. 2541 มาตรา 57-58",
        "ค่าล่วงเวลา": "พระราชบัญญัติคุ้มครองแรงงาน พ.ศ. 2541 มาตรา 51-53",
        "ประกันสังคม": "พระราชบัญญัติประกันสังคม พ.ศ. 2533",
        "ชดเชย": "พระราชบัญญัติคุ้มครองแรงงาน พ.ศ. 2541 มาตรา 57-60",
        "ไล่ออก": "พระราชบัญญัติคุ้มครองแรงงาน พ.ศ. 2541 มาตรา 57",
        "สิทธิลูกจ้าง": "พระราชบัญญัติคุ้มครองแรงงาน พ.ศ. 2541",
    }

    query_lower = query.lower()
    related = []

    for key, law in law_map.items():
        if key in query_lower:
            related.append({"keyword": key, "law": law})

    return related


def format_case_law_response(results: List[Dict[str, Any]]) -> str:
    """จัดรูปแบบผลลัพธ์สำหรับแสดง"""
    if not results:
        return "ไม่พบแนวคำพิพากษาที่เกี่ยวข้อง"

    response = "📚 **แนวคำพิพากษาที่เกี่ยวข้อง**\n\n"

    for i, case in enumerate(results, 1):
        response += f"**{i}. {case['issue']}**\n"
        response += f"   - เลขคดี: {case['case_number']} ปี {case['year']}\n"
        response += f"   - ศาล: {case['court']}\n"
        response += f"   - หลักกฎหมาย: {case['principle']}\n"
        response += f"   - คำพิพากษา: {case['holding']}\n\n"

    return response
