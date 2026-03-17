import json
import random
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List


@dataclass
class MockLaborCase:
    case_number: str
    case_type: str
    case_category: str
    plaintiff: str
    defendant: str
    claim_amount: float
    filed_date: str
    court: str
    status: str
    summary: str
    key_issues: List[str]
    outcome: str
    outcome_probability: float
    timeline: List[Dict[str, str]]


CASE_TYPES = [
    ("ค่าจ้าง", "wage"),
    ("ค่าล่วงเวลา", "overtime"),
    ("ค่าทำงานวันหยุด", "holiday"),
    ("ไล่ออก", "termination"),
    ("เลิกจ้าง", "termination"),
    ("ค่าชดเชย", "compensation"),
    ("ค่าเสียหาย", "damages"),
    ("ทุกข์ทรมาน", "suffering"),
    ("การเลือกปฏิบัติ", "discrimination"),
    ("สภาพการจ้าง", "employment"),
    ("ประกันสังคม", "social_security"),
    ("ลาป่วย", "leave"),
    ("ลาคลอด", "maternity"),
]

PLAINTIFF_TITLES = ["นาย", "นาง", "นางสาว", "น.ส.", "นาย", "นาง", "นางสาว"]
FIRST_NAMES = [
    "สมชาย",
    "สมศักดิ์",
    "วิชัย",
    "สุรชัย",
    "ประเสริฐ",
    "ธนากร",
    "พิศาล",
    "โชคชัย",
    "วรรณา",
    "สุนีย์",
    "พิมพ์ใจ",
    "วันทนา",
    "ศิริพร",
    "นลินี",
    "ศศิธร",
    "วิไล",
    "อนุชา",
    "ธนา",
    "ภูมิ",
    "ณรงค์",
    "วิทยา",
    "สำรวย",
    "ชัยวัฒน์",
    "ประยุทธ์",
]

DEFENDANT_COMPANIES = [
    "บริษัท อมรอินดัสเตรียล จำกัด",
    "บริษัท พีทีที คอร์ปอเรชั่น จำกัด",
    "บริษัท ซีพี ออลล์ จำกัด",
    "บริษัท ไทยเบฟเวอเรจ จำกัด",
    "บริษัท กสท. โทรคมนาคม จำกัด",
    "บริษัท ทรู คอร์ปอเรชั่น จำกัด",
    "บริษัท แอดวานซ์ อินโฟร์ เซอร์วิส จำกัด",
    "บริษัท บมจ. ปตท.",
    "บริษัท ไทยออยล์ จำกัด",
    "บริษัท พีเอสจี กรุ๊ป จำกัด",
    "ห้างหุ้นส่วนจำกัด สยามเมคเกอร์",
    "บริษัท วงศ์สกุลเมตตา จำกัด",
    "บริษัท ซิงเกอร์ประเทศไทย จำกัด",
    "บริษัท โตโยต้า มอเตอร์ ประเทศไทย จำกัด",
    "บริษัท ฮอนด้า ออโตโมบิล ประเทศไทย จำกัด",
]

COURTS = [
    "ศาลแรงงานกลาง",
    "ศาลแรงงานเขต 1",
    "ศาลแรงงานเขต 2",
    "ศาลแรงงานเขต 3",
    "ศาลแรงงานเขต 4",
    "ศาลแรงงานภาค",
]

OUTCOMES = [
    "ชนะคดี",
    "ชนะบางส่วน",
    "แพ้คดี",
    "คดีถึงที่สุด",
    "คดียุติ",
    "อยู่ระหว่างพิจารณา",
]

STATUSES = [
    "รับฟ้อง",
    "สืบพยาน",
    "สืบพยานฝ่ายโจทก์",
    "สืบพยานฝ่ายจำเลย",
    "คู่ความให้การ",
    "อ่านคำพิพากษา",
    "ยุติคดี",
]


def generate_case_number(year: int, sequence: int) -> str:
    return f"พ.{year % 100:02d}/{sequence:05d}"


def generate_patient_name() -> str:
    title = random.choice(PLAINTIFF_TITLES)
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(FIRST_NAMES)
    return f"{title} {first_name} {last_name}"


def generate_case_type() -> tuple:
    return random.choice(CASE_TYPES)


def generate_claim_amount(case_category: str) -> float:
    ranges = {
        "wage": (50000, 500000),
        "overtime": (30000, 300000),
        "holiday": (20000, 200000),
        "termination": (100000, 2000000),
        "compensation": (50000, 1000000),
        "damages": (50000, 500000),
        "suffering": (30000, 300000),
        "discrimination": (50000, 500000),
        "employment": (30000, 300000),
        "social_security": (20000, 200000),
        "leave": (10000, 100000),
        "maternity": (30000, 200000),
    }
    min_val, max_val = ranges.get(case_category, (10000, 100000))
    return random.randint(min_val, max_val)


def generate_filed_date() -> str:
    days_ago = random.randint(1, 730)
    date = datetime.now() - timedelta(days=days_ago)
    return date.strftime("%d/%m/%Y")


def generate_key_issues(case_category: str) -> List[str]:
    issues_map = {
        "wage": [
            "ผู้ฟ้องไม่ได้รับค่าจ้างตามที่ตกลง",
            "จำเลยหักค่าจ้างโดยไม่ชอบด้วยกฎหมาย",
            "มีการคำนวณค่าจ้างผิดพลาด",
        ],
        "overtime": [
            "ผู้ฟ้องทำงานล่วงเวลาแต่ไม่ได้รับค่าล่วงเวลา",
            "จำเลยไม่จ่ายค่าล่วงเวลาในอัตราที่กฎหมายกำหนด",
            "ไม่มีการบันทึกเวลาทำงานล่วงเวลา",
        ],
        "termination": [
            "การไล่ออกไม่เป็นธรรม",
            "จำเลยเลิกจ้างโดยไม่แจ้งล่วงหน้า",
            "ไม่ได้รับเงินชดเชยตามกฎหมาย",
            "การเลิกจ้างไม่มีเหตุอันควร",
        ],
        "discrimination": [
            "ถูกเลือกปฏิบัติเนื่องจากเพศ",
            "ถูกเลือกปฏิบัติเนื่องจากอายุ",
            "การปฏิบัติต่อผู้ฟ้องแตกต่างจากพนักงานอื่น",
        ],
    }
    issues = issues_map.get(case_category, ["ข้อพิพาทตามฟ้อง"])
    return random.sample(issues, min(2, len(issues)))


def generate_outcome_probability(case_category: str) -> float:
    probs = {
        "wage": 0.75,
        "overtime": 0.70,
        "holiday": 0.72,
        "termination": 0.65,
        "compensation": 0.60,
        "damages": 0.55,
        "suffering": 0.50,
        "discrimination": 0.45,
        "employment": 0.58,
        "social_security": 0.68,
        "leave": 0.62,
        "maternity": 0.70,
    }
    base_prob = probs.get(case_category, 0.5)
    return base_prob + random.uniform(-0.15, 0.15)


def generate_timeline(
    case_number: str, filed_date: str, status: str
) -> List[Dict[str, str]]:
    timeline = [
        {"date": filed_date, "event": "ยื่นฟ้องคดี", "detail": f"เลขที่คดี {case_number}"},
    ]

    steps = [
        "รับฟ้องและส่งหมายให้จำเลย",
        "จำเลยยื่นคำให้การ",
        "ไกล่เกลี่ยข้อพิพาท",
        "สืบพยานฝ่ายโจทก์",
        "สืบพยานฝ่ายจำเลย",
        "คู่ความนำสืบปากสุดท้าย",
    ]

    selected_steps = random.sample(steps, min(3, len(steps)))

    for step in selected_steps:
        timeline.append(
            {
                "date": f"{(datetime.now() - timedelta(days=random.randint(10, 180))).strftime('%d/%m/%Y')}",
                "event": step,
                "detail": "ดำเนินการแล้ว",
            }
        )

    if status in ["อ่านคำพิพากษา", "ชนะคดี", "แพ้คดี"]:
        timeline.append(
            {
                "date": datetime.now().strftime("%d/%m/%Y"),
                "event": "อ่านคำพิพากษา",
                "detail": random.choice(OUTCOMES),
            }
        )

    return timeline


def generate_single_case(index: int) -> MockLaborCase:
    case_type, case_category = generate_case_type()
    year = random.randint(2563, 2568)
    case_num = generate_case_number(year, index)
    filed_date = generate_filed_date()
    claim_amount = generate_claim_amount(case_category)
    status = random.choice(STATUSES)

    outcomes_weights = {
        "ชนะคดี": 35,
        "ชนะบางส่วน": 25,
        "แพ้คดี": 20,
        "คดีถึงที่สุด": 10,
        "คดียุติ": 5,
        "อยู่ระหว่างพิจารณา": 5,
    }
    outcome = random.choices(
        list(outcomes_weights.keys()), weights=list(outcomes_weights.values())
    )[0]

    return MockLaborCase(
        case_number=case_num,
        case_type=case_type,
        case_category=case_category,
        plaintiff=generate_patient_name(),
        defendant=random.choice(DEFENDANT_COMPANIES),
        claim_amount=claim_amount,
        filed_date=filed_date,
        court=random.choice(COURTS),
        status=status,
        summary=f"คดีแรงงาน{case_type}ระหว่าง{generate_patient_name()}กับ{random.choice(DEFENDANT_COMPANIES)} มูลค่าความเสียหาย {claim_amount:,} บาท",
        key_issues=generate_key_issues(case_category),
        outcome=outcome if status in ["อ่านคำพิพากษา", "ยุติคดี"] else "อยู่ระหว่างพิจารณา",
        outcome_probability=generate_outcome_probability(case_category),
        timeline=generate_timeline(case_num, filed_date, status),
    )


def generate_mock_cases(count: int = 10000) -> List[Dict[str, Any]]:
    cases = []
    for i in range(1, count + 1):
        case = generate_single_case(i)
        cases.append(asdict(case))
    return cases


def save_mock_cases(filename: str = "mock_cases.json", count: int = 10000):
    cases = generate_mock_cases(count)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(cases, f, ensure_ascii=False, indent=2)
    return len(cases)


def load_mock_cases(filename: str = "mock_cases.json") -> List[Dict[str, Any]]:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


if __name__ == "__main__":
    from pathlib import Path

    DATA_DIR = Path(__file__).parent
    count = save_mock_cases(str(DATA_DIR / "mock_cases.json"), 10000)
    print(f"สร้างข้อมูลคดีจำนวน {count} คดี เรียบร้อย!")
