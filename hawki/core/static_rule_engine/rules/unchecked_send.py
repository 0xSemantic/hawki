# --------------------
# File: hawki/core/static_rule_engine/rules/unchecked_send.py
# --------------------
"""
Unchecked send: detect send() or transfer() calls without checking return value.
"""

from . import BaseRule

class UncheckedSendRule(BaseRule):
    def run_check(self, contract_data):
        findings = []
        for contract in contract_data:
            source = contract.get("source", "")
            # simplistic: if "send(" appears and not "if(" before it, flag
            if "send(" in source and "if(" not in source:
                findings.append({
                    "rule": "UncheckedSend",
                    "severity": "MEDIUM",
                    "description": "send() without checking return value may silently fail.",
                    "location": contract.get("path"),
                })
        return findings
# EOF: hawki/core/static_rule_engine/rules/unchecked_send.py