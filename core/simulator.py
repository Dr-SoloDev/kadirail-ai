"""
What-If Simulator for legal case outcome prediction.
"""

import random
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class ScenarioOption:
    """A scenario option for comparison."""

    name: str
    win_rate: int
    estimated_time: int
    estimated_cost: int
    risks: List[str]
    recommendations: List[str]


class WhatIfSimulator:
    """
    Simulator for predicting legal case outcomes.

    Provides What-If analysis for different decision paths.
    """

    # Historical data templates (MVP - would be ML model in production)
    CASE_STATS = {
        "wage": {
            "mediation_win_rate": 65,
            "labor_court_win_rate": 72,
            "appeal_win_rate": 45,
            "avg_time_mediation": 30,
            "avg_time_court": 180,
            "avg_time_appeal": 365,
            "cost_mediation": 5000,
            "cost_court": 50000,
            "cost_appeal": 100000,
        },
        "termination": {
            "mediation_win_rate": 55,
            "labor_court_win_rate": 68,
            "appeal_win_rate": 40,
            "avg_time_mediation": 45,
            "avg_time_court": 240,
            "avg_time_appeal": 420,
            "cost_mediation": 8000,
            "cost_court": 80000,
            "cost_appeal": 150000,
        },
        "bonus": {
            "mediation_win_rate": 70,
            "labor_court_win_rate": 75,
            "appeal_win_rate": 50,
            "avg_time_mediation": 21,
            "avg_time_court": 120,
            "avg_time_appeal": 300,
            "cost_mediation": 3000,
            "cost_court": 40000,
            "cost_appeal": 80000,
        },
    }

    def __init__(self, case_map):
        """
        Initialize simulator with a case map.

        Args:
            case_map: KadiRailMap instance
        """
        self.case_map = case_map
        self.case_type = case_map.case_type
        self.stats = self.CASE_STATS.get(self.case_type, self.CASE_STATS["wage"])

    def simulate(self, option_name: str) -> Dict[str, Any]:
        """
        Simulate a scenario option.

        Args:
            option_name: Name of the option to simulate

        Returns:
            Dictionary with simulation results
        """
        # Determine scenario type
        scenario = self._classify_scenario(option_name)

        # Calculate outcomes
        win_rate = self._calculate_win_rate(scenario)
        time_days = self._calculate_time(scenario)
        cost = self._calculate_cost(scenario)
        risks = self._identify_risks(scenario)
        recommendations = self._generate_recommendations(scenario)

        return {
            "option": option_name,
            "scenario": scenario,
            "win_rate": win_rate,
            "estimated_time": time_days,
            "estimated_cost": cost,
            "risks": risks,
            "recommendations": recommendations,
            "confidence": self._calculate_confidence(scenario),
        }

    def _classify_scenario(self, option_name: str) -> str:
        """Classify the scenario based on option name."""
        option_lower = option_name.lower()

        if "ไกล่เกลี่ย" in option_name or "mediation" in option_lower:
            return "mediation"
        elif "ศาล" in option_name or "court" in option_lower:
            return "labor_court"
        elif "อุทธรณ์" in option_name or "appeal" in option_lower:
            return "appeal"
        else:
            return "mediation"  # Default

    def _calculate_win_rate(self, scenario: str) -> int:
        """Calculate win rate based on scenario."""
        rate_map = {
            "mediation": self.stats["mediation_win_rate"],
            "labor_court": self.stats["labor_court_win_rate"],
            "appeal": self.stats["appeal_win_rate"],
        }

        base_rate = rate_map.get(scenario, 50)

        # Add some variance based on case specifics
        variance = random.randint(-10, 10)

        # Adjust for current step progress
        progress_factor = 1.0 + (self.case_map.current_step * 0.02)

        return min(95, max(5, int((base_rate + variance) * progress_factor)))

    def _calculate_time(self, scenario: str) -> int:
        """Calculate estimated time in days."""
        time_map = {
            "mediation": self.stats["avg_time_mediation"],
            "labor_court": self.stats["avg_time_court"],
            "appeal": self.stats["avg_time_appeal"],
        }

        base_time = time_map.get(scenario, 60)

        # Add remaining steps time
        remaining_steps = len(self.case_map.steps) - self.case_map.current_step - 1
        remaining_time = sum(
            s.duration_days
            for s in self.case_map.steps[self.case_map.current_step + 1 :]
        )

        return base_time + remaining_time

    def _calculate_cost(self, scenario: str) -> int:
        """Calculate estimated cost in THB."""
        cost_map = {
            "mediation": self.stats["cost_mediation"],
            "labor_court": self.stats["cost_court"],
            "appeal": self.stats["cost_appeal"],
        }

        base_cost = cost_map.get(scenario, 20000)

        # Add legal fees estimate
        legal_fee = 15000 if scenario != "mediation" else 0

        return base_cost + legal_fee

    def _identify_risks(self, scenario: str) -> List[str]:
        """Identify potential risks for the scenario."""
        risks = []

        if scenario == "mediation":
            risks = [
                "นายจ้างอาจไม่ยอมเข้าร่วมไกล่เกลี่ย",
                "อาจไม่สามารถตกลงกันได้",
                "ข้อตกลงไม่มีผลผูกพันทางกฎหมายเท่ากับคำพิพากษา",
            ]
        elif scenario == "labor_court":
            risks = ["ใช้เวลาพิจารณาคดีนาน", "มีค่าใช้จ่ายในการจ้างทนายความ", "ผลคดีไม่แน่นอน"]
        elif scenario == "appeal":
            risks = ["ใช้เวลามากที่สุด", "มีค่าใช้จ่ายสูง", "โอกาสชนะต่ำกว่าขั้นตอนแรก"]

        return risks

    def _generate_recommendations(self, scenario: str) -> List[str]:
        """Generate recommendations based on scenario."""
        recommendations = []

        if scenario == "mediation":
            recommendations = [
                "เตรียมหลักฐานให้พร้อมก่อนเข้าไกล่เกลี่ย",
                "กำหนดขั้นต่ำที่ยอมรับได้ล่วงหน้า",
                "พิจารณาปรึกษาทนายความก่อนเข้าสู้กระบวนการ",
            ]
        elif scenario == "labor_court":
            recommendations = [
                "จ้างทนายความที่มีประสบการณ์คดีแรงงาน",
                "รวบรวมพยานหลักฐานให้ครบถ้วน",
                "เตรียมข้อเท็จจริงและข้อกฎหมายให้ชัดเจน",
            ]
        elif scenario == "appeal":
            recommendations = [
                "ปรึกษาทนายความผู้เชี่ยวชาญการอุทธรณ์",
                "พิจารณาข้อผิดพลาดทางกฎหมายที่อาจอุทธรณ์ได้",
                "เตรียมค่าใช้จ่ายสำหรับการดำเนินคดีต่อ",
            ]

        return recommendations

    def _calculate_confidence(self, scenario: str) -> float:
        """Calculate confidence score for the prediction."""
        # Base confidence
        base_confidence = 0.75

        # Adjust based on data availability
        if self.case_map.current_step == 0:
            return base_confidence - 0.1

        return base_confidence

    def compare_options(self, options: List[str]) -> List[Dict[str, Any]]:
        """
        Compare multiple options.

        Args:
            options: List of option names to compare

        Returns:
            List of simulation results
        """
        return [self.simulate(opt) for opt in options]


def render_simulation_results(result: Dict[str, Any]) -> None:
    """
    Render simulation results in Streamlit.

    Args:
        result: Simulation result dictionary
    """
    import streamlit as st

    st.markdown(f"### 🎯 ผลการจำลอง: {result['option']}")

    # Key metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        win_rate = result["win_rate"]
        emoji = "🟢" if win_rate >= 70 else ("🟡" if win_rate >= 50 else "🔴")
        st.metric(f"{emoji} โอกาสชนะ", f"{win_rate}%")

    with col2:
        st.metric("⏱️ เวลาโดยประมาณ", f"{result['estimated_time']} วัน")

    with col3:
        cost = result["estimated_cost"]
        st.metric("💰 ค่าใช้จ่าย", f"฿{cost:,}")

    # Confidence
    confidence = result.get("confidence", 0.75)
    st.progress(confidence, text=f"ความมั่นใจ: {confidence * 100:.0f}%")

    # Risks
    if result.get("risks"):
        st.markdown("### ⚠️ ความเสี่ยง")
        for risk in result["risks"]:
            st.markdown(f"- {risk}")

    # Recommendations
    if result.get("recommendations"):
        st.markdown("### 💡 คำแนะนำ")
        for rec in result["recommendations"]:
            st.markdown(f"- {rec}")
