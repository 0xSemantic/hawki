# --------------------
# File: hawki/core/static_rule_engine/rules/front_running.py
# --------------------
"""
Front‑running vulnerability: detect transaction ordering dependency.
"""

from . import BaseRule

class FrontRunningRule(BaseRule):
    def run_check(self, contract_data):
        findings = []
        # Placeholder: real detection is complex. For Phase 1 we flag any function that uses block.timestamp or similar.
        for contract in contract_data:
            source = contract.get("source", "")
            if "block.timestamp" in source or "block.number" in source:
                findings.append({
                    "rule": "FrontRunning",
                    "severity": "LOW",
                    "description": "Potential front‑running vulnerability due to block.timestamp/number usage.",
                    "location": contract.get("path"),
                })
        return findings
# EOF: hawki/core/static_rule_engine/rules/front_running.py