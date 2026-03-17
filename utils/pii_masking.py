"""
PII (Personally Identifiable Information) Masking Module
Challenge 3: ระบบจัดการข้อมูลที่สามารถปกปิดข้อมูลส่วนบุคคลได้อย่างปลอดภัย
"""

import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import hashlib


@dataclass
class PIIEntity:
    type: str
    original: str
    masked: str
    start: int
    end: int


THAI_ID_PATTERN = r"\d{13}"
PHONE_PATTERN = r"0\d{8,9}"
EMAIL_PATTERN = r"[\w.-]+@[\w.-]+\.\w+"
PASSPORT_PATTERN = r"[A-Z]{1,2}\d{6,9}"
TAX_ID_PATTERN = r"\d{10,13}"
ADDRESS_KEYWORDS = r"(ที่อยู่|อยู่บ้านเลขที่|ต\.)"


NAME_TITLES = [
    "นาย",
    "นาง",
    "นางสาว",
    "น.ส.",
    "ด.ช.",
    "ด.ญ.",
    "พ.ต.อ.",
    "ร.ต.อ.",
    "ส.ต.อ.",
    "จ.ส.อ.",
    "นางพยาบาล",
    "นายแพทย์",
    "แพทย์",
    "ทันตแพทย์",
    "เภสัชกร",
]


def mask_thai_id(text: str) -> Tuple[str, List[PIIEntity]]:
    """ปกปิดเลขประจำตัวประชาชน (13 หลัก)"""
    entities = []

    def replace(match):
        original = match.group(0)
        masked = original[:1] + "X" * 11 + original[-1:]
        entities.append(
            PIIEntity(
                type="เลขประจำตัวประชาชน",
                original=original,
                masked=masked,
                start=match.start(),
                end=match.end(),
            )
        )
        return masked

    masked_text = re.sub(THAI_ID_PATTERN, replace, text)
    return masked_text, entities


def mask_phone(text: str) -> Tuple[str, List[PIIEntity]]:
    """ปกปิดเบอร์โทรศัพท์"""
    entities = []

    def replace(match):
        original = match.group(0)
        if len(original) == 10:
            masked = original[:3] + "XXX" + original[-4:]
        else:
            masked = original[:2] + "XXXXXXX"
        entities.append(
            PIIEntity(
                type="เบอร์โทรศัพท์",
                original=original,
                masked=masked,
                start=match.start(),
                end=match.end(),
            )
        )
        return masked

    masked_text = re.sub(PHONE_PATTERN, replace, text)
    return masked_text, entities


def mask_email(text: str) -> Tuple[str, List[PIIEntity]]:
    """ปกปิดอีเมล"""
    entities = []

    def replace(match):
        original = match.group(0)
        at_idx = original.find("@")
        if at_idx > 2:
            masked = original[:2] + "***" + original[at_idx:]
        else:
            masked = "***" + original[at_idx:]
        entities.append(
            PIIEntity(
                type="อีเมล",
                original=original,
                masked=masked,
                start=match.start(),
                end=match.end(),
            )
        )
        return masked

    masked_text = re.sub(EMAIL_PATTERN, replace, text)
    return masked_text, entities


def mask_passport(text: str) -> Tuple[str, List[PIIEntity]]:
    """ปกปิดเลขหนังสือเดินทาง"""
    entities = []

    def replace(match):
        original = match.group(0)
        masked = original[:2] + "X" * (len(original) - 2)
        entities.append(
            PIIEntity(
                type="เลขหนังสือเดินทาง",
                original=original,
                masked=masked,
                start=match.start(),
                end=match.end(),
            )
        )
        return masked

    masked_text = re.sub(PASSPORT_PATTERN, replace, text)
    return masked_text, entities


def mask_tax_id(text: str) -> Tuple[str, List[PIIEntity]]:
    """ปกปิดเลขประจำตัวผู้เสียภาษี"""
    entities = []

    def replace(match):
        original = match.group(0)
        masked = original[:2] + "X" * (len(original) - 4) + original[-2:]
        entities.append(
            PIIEntity(
                type="เลขประจำตัวผู้เสียภาษี",
                original=original,
                masked=masked,
                start=match.start(),
                end=match.end(),
            )
        )
        return masked

    masked_text = re.sub(TAX_ID_PATTERN, replace, text)
    return masked_text, mask_tax_id(text.replace("-", ""))[0], entities


def mask_bank_account(text: str) -> Tuple[str, List[PIIEntity]]:
    """ปกปิดเลขบัญชีธนาคาร"""
    entities = []

    pattern = r"\d{10,16}"

    def replace(match):
        original = match.group(0)
        masked = original[:4] + "X" * (len(original) - 8) + original[-4:]
        entities.append(
            PIIEntity(
                type="เลขบัญชีธนาคาร",
                original=original,
                masked=masked,
                start=match.start(),
                end=match.end(),
            )
        )
        return masked

    masked_text = re.sub(pattern, replace, text)
    return masked_text, entities


def mask_names(text: str) -> Tuple[str, List[PIIEntity]]:
    """ปกปิดชื่อ-นามสกุล (Thai)"""
    entities = []

    name_pattern = r"(นาย|นาง|นางสาว|น\.ส\.|ด\.ช\.|ด\.ญ\.)\s+([ก-๙]+)\s+([ก-๙]+)"

    def replace(match):
        title = match.group(1)
        first_name = match.group(2)
        last_name = match.group(3)

        original = match.group(0)
        masked = f"{title} [ชื่อ] [นามสกุล]"

        entities.append(
            PIIEntity(
                type="ชื่อ-นามสกุล",
                original=original,
                masked=masked,
                start=match.start(),
                end=match.end(),
            )
        )
        return masked

    masked_text = re.sub(name_pattern, replace, text)
    return masked_text, entities


def mask_addresses(text: str) -> Tuple[str, List[PIIEntity]]:
    """ปกปิดที่อยู่"""
    entities = []

    address_patterns = [
        r"บ้านเลขที่\s*[\d/]+",
        r"หมู่\s*\d+",
        r"ตำบล\s*[\ก-๙]+",
        r"อำเภอ\s*[\ก-๙]+",
        r"จังหวัด\s*[\ก-๙]+",
        r"รหัสไปรษณีย์\s*\d{5}",
    ]

    masked_text = text
    for pattern in address_patterns:

        def replace(match):
            original = match.group(0)
            entities.append(
                PIIEntity(
                    type="ที่อยู่",
                    original=original,
                    masked="[ที่อยู่]",
                    start=match.start(),
                    end=match.end(),
                )
            )
            return "[ที่อยู่]"

        masked_text = re.sub(pattern, replace, masked_text)

    return masked_text, entities


def mask_all(
    text: str, include_names: bool = True, include_address: bool = True
) -> Dict[str, any]:
    """
    ปกปิด PII ทั้งหมดในเอกสาร

    Args:
        text: เนื้อหาต้นฉบับ
        include_names: รวมชื่อ-นามสกุล
        include_address: รวมที่อยู่

    Returns:
        dict with masked_text and list of masked entities
    """
    all_entities = []

    text, entities = mask_thai_id(text)
    all_entities.extend(entities)

    text, entities = mask_phone(text)
    all_entities.extend(entities)

    text, entities = mask_email(text)
    all_entities.extend(entities)

    text, entities = mask_passport(text)
    all_entities.extend(entities)

    text, entities = mask_tax_id(text)
    all_entities.extend(entities)

    text, entities = mask_bank_account(text)
    all_entities.extend(entities)

    if include_names:
        text, entities = mask_names(text)
        all_entities.extend(entities)

    if include_address:
        text, entities = mask_addresses(text)
        all_entities.extend(entities)

    return {
        "original_text": text,
        "masked_text": text,
        "entities_masked": len(all_entities),
        "entities": [e.__dict__ for e in all_entities],
    }


def generate_hash(text: str, salt: str = "") -> str:
    """สร้าง hash สำหรับ de-identification"""
    return hashlib.sha256((text + salt).encode()).hexdigest()[:16]


def anonymize_case(case_data: Dict, salt: str = "kadirail") -> Dict:
    """
    Anonymize ข้อมูลคดีสำหรับการวิจัย/วิเคราะห์

    Args:
        case_data: dict ข้อมูลคดี
        salt: salt สำหรับ hash

    Returns:
        dict ข้อมูลคดีที่ถูก anonymize แล้ว
    """
    anonymized = case_data.copy()

    fields_to_mask = [
        "plaintiff",
        "defendant",
        "plaintiff_id",
        "defendant_id",
        "phone",
        "email",
        "address",
    ]

    for field in fields_to_mask:
        if field in anonymized and anonymized[field]:
            anonymized[field] = (
                f"[{field.upper()}_{generate_hash(str(anonymized[field]), salt)}]"
            )

    return anonymized
