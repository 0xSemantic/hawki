# --------------------
# File: hawki/core/static_rule_engine/rules/delegatecall_misuse.py
# --------------------
"""
delegatecall misuse: detect calls to untrusted addresses via delegatecall.
"""

from . import BaseRule

class DelegatecallMisuseRule(BaseRule):
    def run_check(self, contract_data):
        findings = []
        for contract in contract_data:
            source = contract.get("source", "")
            if "delegatecall" in source:
                findings.append({
                    "rule": "DelegatecallMisuse",
                    "severity": "HIGH",
                    "description": "delegatecall to untrusted address can lead to storage manipulation.",
                    "location": contract.get("path"),
                })
        return findings
# EOF: hawki/core/static_rule_engine/rules/delegatecall_misuse.py