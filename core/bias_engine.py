"""
Bias Engine for detecting and correcting bias in legal information.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class BiasFinding:
    """A single bias finding."""

    category: str
    text: str
    severity: str
    explanation: str
    suggestion: Optional[str] = None


class BiasEngine:
    """
    Engine for detecting and correcting bias in legal content.

    Implements Responsible AI principles:
    - Bias Correction Layer
    - Trauma-Informed Design
    - Privacy by Design
    - Explainability
    """

    # Bias patterns for Thai legal text
    BIAS_PATTERNS = {
        "gender": {
            "keywords": ["ผู้ชาย", "ผู้หญิง", "สามี", "ภรรยา", "พ่อ", "แม่", "ลูกชาย", "ลูกสาว"],
            "severity": "medium",
            "explanation": "ข้อความอาจมีอคติทางเพศสภาพ",
            "suggestion": "พิจารณาใช้ภาษาที่เป็นกลางทางเพศ",
        },
        "age": {
            "keywords": ["เด็ก", "คนชรา", "คนแก่", "วัยรุ่น", "วัยเด็ก", "วัยชรา"],
            "severity": "medium",
            "explanation": "ข้อความอาจมีอคติทางวัย",
            "suggestion": "หลีกเลี่ยงการอ้างอิงอายุโดยไม่จำเป็น",
        },
        "occupation": {
            "keywords": ["กรรมกร", "พนักงาน", "นายจ้าง", "เจ้านาย", "ลูกจ้าง", "นายทุน"],
            "severity": "low",
            "explanation": "ข้อความอาจสะท้อนอคติทางอาชีพ",
            "suggestion": "ใช้คำที่เป็นกลาง",
        },
        "social_class": {
            "keywords": ["ชนชั้น", "รวย", "จน", "มั่งมี", "ยากจน", "ฐานะ"],
            "severity": "high",
            "explanation": "ข้อความอาจมีอคติทางชนชั้น",
            "suggestion": "หลีกเลี่ยงการอ้างถึงสถานะทางเศรษฐกิจ",
        },
        "region": {
            "keywords": ["กรุงเทพ", "ต่างจังหวัด", "ภาคเหนือ", "ภาคอีสาน", "ภาคใต้"],
            "severity": "medium",
            "explanation": "ข้อความอาจมีอคติทางภูมิภาค",
            "suggestion": "ไม่ควรใช้ภูมิภาคเป็นเกณฑ์",
        },
        "trauma_keywords": {
            "keywords": [
                "ฆ่าตัวตาย",
                "ทำร้าย",
                "บาดเจ็บ",
                "เจ็บปวด",
                "ทุกข์",
                "ทรมาน",
                "สะเทือนขวัญ",
            ],
            "severity": "high",
            "explanation": "ข้อความอาจกระทบต่อผู้ที่มีประสบการณ์ trauma",
            "suggestion": "พิจารณาใช้ภาษาที่รุนแรงน้อยกว่า",
        },
        "discriminatory": {
            "keywords": ["ต่างชาติ", "ต่างชาติ", "ต่างด้าว", "คนต่างด้าว"],
            "severity": "high",
            "explanation": "ข้อความอาจมีการเลือกปฏิบัติ",
            "suggestion": "ใช้ภาษาที่เป็นกลางและเคารพศักดิ์ศรี",
        },
    }

    # Correction rules
    CORRECTION_RULES = {
        "gender": {
            "สามี": "คู่สมรสชาย",
            "ภรรยา": "คู่สมรสหญิง",
            "พ่อ": "บิดา",
            "แม่": "มารดา",
            "ลูกชาย": "บุตร",
            "ลูกสาว": "บุตรี",
        },
        "occupation": {"กรรมกร": "ลูกจ้าง", "นายจ้าง": "ผู้จ้างงาน", "เจ้านาย": "ผู้บังคับบัญชา"},
        "social_class": {"คนจน": "ผู้มีรายได้น้อย", "คนรวย": "ผู้มีรายได้สูง"},
    }

    def __init__(self):
        """Initialize the bias engine."""
        self.findings: List[BiasFinding] = []

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyze text for bias.

        Args:
            text: Thai legal text to analyze

        Returns:
            Dictionary with analysis results
        """
        self.findings = []

        # Check for each bias category
        for category, pattern_data in self.BIAS_PATTERNS.items():
            keywords = pattern_data["keywords"]

            for keyword in keywords:
                if keyword in text:
                    finding = BiasFinding(
                        category=category,
                        text=keyword,
                        severity=pattern_data["severity"],
                        explanation=pattern_data["explanation"],
                        suggestion=pattern_data.get("suggestion"),
                    )
                    self.findings.append(finding)

        # Calculate bias score
        bias_score = self._calculate_bias_score()

        # Get bias categories
        bias_categories = self._get_bias_categories()

        # Generate corrected text
        corrected_text = self.correct_text(text)

        return {
            "findings": [f.__dict__ for f in self.findings],
            "bias_score": bias_score,
            "bias_categories": bias_categories,
            "corrected_text": corrected_text if self.findings else text,
            "word_count": len(text.split()),
        }

    def _calculate_bias_score(self) -> float:
        """Calculate overall bias score (0-100)."""
        if not self.findings:
            return 0.0

        severity_weights = {"high": 3, "medium": 2, "low": 1}

        total_weight = sum(severity_weights.get(f.severity, 1) for f in self.findings)

        max_possible = len(self.BIAS_PATTERNS) * 3

        return min(100, (total_weight / max_possible) * 100)

    def _get_bias_categories(self) -> Dict[str, int]:
        """Get counts by bias category."""
        categories = {}

        for finding in self.findings:
            categories[finding.category] = categories.get(finding.category, 0) + 1

        return categories

    def correct_text(self, text: str) -> str:
        """
        Apply bias corrections to text.

        Args:
            text: Original text

        Returns:
            Corrected text
        """
        corrected = text

        # Apply correction rules
        for category, rules in self.CORRECTION_RULES.items():
            for old, new in rules.items():
                corrected = corrected.replace(old, new)

        return corrected

    def get_finding_summary(self) -> Dict[str, Any]:
        """Get summary of findings."""
        if not self.findings:
            return {
                "total": 0,
                "high_severity": 0,
                "medium_severity": 0,
                "low_severity": 0,
                "categories": [],
            }

        return {
            "total": len(self.findings),
            "high_severity": sum(1 for f in self.findings if f.severity == "high"),
            "medium_severity": sum(1 for f in self.findings if f.severity == "medium"),
            "low_severity": sum(1 for f in self.findings if f.severity == "low"),
            "categories": list(set(f.category for f in self.findings)),
        }

    def explain_finding(self, finding: BiasFinding) -> str:
        """
        Generate explanation for a finding.

        Args:
            finding: BiasFinding instance

        Returns:
            Explanation string
        """
        explanations = {
            "gender": "การใช้คำที่ระบุเพศโดยไม่จำเป็นอาจสะท้อนอคติ",
            "age": "การอ้างอายุอาจนำไปสู่การเลือกปฏิบัติตามวัย",
            "occupation": "คำเรียกอาชีพบางคำอาจมีความหมายเชิงลบ",
            "social_class": "การอ้างถึงชนชั้นอาจสะท้อนอคติทางสังคม",
            "region": "การแบ่งแยกตามภูมิภาคอาจไม่เหมาะสม",
            "trauma_keywords": "คำบางคำอาจกระทบต่อผู้ที่มีประสบการณ์ trauma",
            "discriminatory": "การเลือกปฏิบัติต่างชาติ/ชาติพันธุ์ผิดกฎหมาย",
        }

        return explanations.get(finding.category, finding.explanation)


def create_bias_report(analysis_result: Dict[str, Any]) -> str:
    """
    Create a formatted bias report.

    Args:
        analysis_result: Result from BiasEngine.analyze()

    Returns:
        Formatted report string
    """
    lines = ["# รายงานการตรวจสอบอคติ", ""]

    # Summary
    score = analysis_result.get("bias_score", 0)
    lines.append("## สรุปผล")
    lines.append(f"- คะแนนอคติ: {score:.1f}%")

    if score > 70:
        lines.append("- ระดับ: 🔴 สูง")
    elif score > 30:
        lines.append("- ระดับ: 🟡 ปานกลาง")
    else:
        lines.append("- ระดับ: 🟢 ต่ำ")

    lines.append("")

    # Findings
    findings = analysis_result.get("findings", [])
    if findings:
        lines.append("## รายการที่พบ")

        for f in findings:
            severity_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(
                f["severity"], "⚪"
            )
            lines.append(f"- {severity_emoji} **{f['category']}**: {f['text']}")
            lines.append(f"  - {f['explanation']}")
            if f.get("suggestion"):
                lines.append(f"  - 💡 {f['suggestion']}")
            lines.append("")

    return "\n".join(lines)
