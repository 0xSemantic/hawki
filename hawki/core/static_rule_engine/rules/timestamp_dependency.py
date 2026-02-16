# --------------------
# File: hawki/core/static_rule_engine/rules/timestamp_dependency.py
# --------------------
"""
Timestamp dependency: using block.timestamp for critical logic may be manipulated by miners.
"""

from . import BaseRule

class TimestampDependencyRule(BaseRule):
    def run_check(self, contract_data):
        findings = []
        for contract in contract_data:
            source = contract.get("source", "")
            if "block.timestamp" in source:
                findings.append({
                    "rule": "TimestampDependency",
                    "severity": "MEDIUM",
                    "description": "block.timestamp can be influenced by miners; avoid for critical logic.",
                    "location": contract.get("path"),
                })
        return findings
# EOF: hawki/core/static_rule_engine/rules/timestamp_dependency.py