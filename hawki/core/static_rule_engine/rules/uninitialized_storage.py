# --------------------
# File: hawki/core/static_rule_engine/rules/uninitialized_storage.py
# --------------------
"""
Uninitialized storage pointers: detect local storage variables that point to default slot 0.
"""

from . import BaseRule

class UninitializedStorageRule(BaseRule):
    def run_check(self, contract_data):
        findings = []
        # Placeholder: actual detection requires deeper AST analysis.
        # For Phase 1 we just warn about potential issue.
        for contract in contract_data:
            # Very naive: look for "storage" keyword without assignment
            source = contract.get("source", "")
            if " storage " in source and " = " not in source:
                findings.append({
                    "rule": "UninitializedStorage",
                    "severity": "HIGH",
                    "description": "Possible uninitialized storage pointer.",
                    "location": contract.get("path"),
                })
        return findings
# EOF: hawki/core/static_rule_engine/rules/uninitialized_storage.py