# --------------------
# File: hawki/core/static_rule_engine/rules/tx_origin_dependency.py
# --------------------
"""
tx.origin authentication: detect use of tx.origin in authorization logic.
"""

from . import BaseRule

class TxOriginRule(BaseRule):
    def run_check(self, contract_data):
        findings = []
        for contract in contract_data:
            source = contract.get("source", "")
            if "tx.origin" in source:
                findings.append({
                    "rule": "TxOrigin",
                    "severity": "MEDIUM",
                    "description": "Use of tx.origin for authentication can lead to phishing attacks.",
                    "location": contract.get("path"),
                })
        return findings
# EOF: hawki/core/static_rule_engine/rules/tx_origin_dependency.py