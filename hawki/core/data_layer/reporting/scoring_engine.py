# --------------------
# File: hawki/core/data_layer/reporting/scoring_engine.py
# --------------------
"""
Security Score Engine – calculates a 0–100 deterministic score based on findings and sandbox results.
The score is used in audit‑grade reports to quantify overall risk posture.
"""

import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class SecurityScoreEngine:
    """Computes security score from findings and optional sandbox results."""

    # Severity weights (deductions from base score 100)
    SEVERITY_WEIGHTS = {
        "Critical": 15,
        "High": 8,
        "Medium": 4,
        "Low": 1,
    }

    # Simulation penalty per successful exploit (additional deduction)
    SIMULATION_PENALTY = 5

    # Score classification bands
    CLASSIFICATION_BANDS = [
        (90, 100, "Secure"),
        (75, 89, "Minor Risk"),
        (50, 74, "Moderate Risk"),
        (25, 49, "High Risk"),
        (0, 24, "Critical Risk"),
    ]

    def calculate(
        self,
        findings: List[Dict[str, Any]],
        sandbox_results: Optional[List[Dict[str, Any]]] = None,
        ai_enabled: bool = False,
    ) -> Dict[str, Any]:
        """
        Compute security score and classification.

        Args:
            findings: List of finding dictionaries, each must have a "severity" field.
            sandbox_results: Optional list of sandbox results, each with "success" and "attack_name".
            ai_enabled: Whether AI was used (affects handling of AI findings).

        Returns:
            Dict with keys:
                score (int): 0–100 score
                classification (str): risk band
                deductions (Dict[str, int]): breakdown of deductions by severity and simulation
                simulation_used (bool)
                ai_used (bool)
        """
        if not findings:
            return {
                "score": 100,
                "classification": "Secure",
                "deductions": {},
                "simulation_used": bool(sandbox_results),
                "ai_used": ai_enabled,
            }

        base_score = 100
        deductions = {}

        # Severity deductions
        severity_counts = {}
        for finding in findings:
            severity = finding.get("severity", "Low")
            # Normalize severity strings (e.g., "HIGH" -> "High")
            severity = severity.capitalize()
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

        total_severity_deduction = 0
        for sev, count in severity_counts.items():
            weight = self.SEVERITY_WEIGHTS.get(sev, 1)  # default to Low if unknown
            deduction = weight * count
            total_severity_deduction += deduction
            deductions[f"{sev.lower()}_findings"] = count

        # Simulation penalty
        simulation_penalty = 0
        if sandbox_results:
            successful = [r for r in sandbox_results if r.get("success")]
            simulation_penalty = len(successful) * self.SIMULATION_PENALTY
            # Cap penalty to avoid negative score? Score floor is 0 anyway.
            deductions["simulation_penalty"] = len(successful)

        final_score = base_score - total_severity_deduction - simulation_penalty
        final_score = max(0, min(100, final_score))  # clamp to 0–100

        # Determine classification
        classification = "Unknown"
        for low, high, label in self.CLASSIFICATION_BANDS:
            if low <= final_score <= high:
                classification = label
                break

        return {
            "score": final_score,
            "classification": classification,
            "deductions": deductions,
            "simulation_used": bool(sandbox_results),
            "ai_used": ai_enabled,
        }

# EOF: hawki/core/data_layer/reporting/scoring_engine.py