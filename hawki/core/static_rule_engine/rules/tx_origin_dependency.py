# --------------------
# File: hawki/core/static_rule_engine/rules/tx_origin_dependency.py
# --------------------
"""
tx.origin authentication: detect use of tx.origin in authorization logic.
"""

from . import BaseRule

class TxOriginRule(BaseRule):
    severity = "High"
    explanation_template = (
        "Using `tx.origin` for authentication is dangerous because it represents the original sender of "
        "the transaction, which can be different from `msg.sender` in a chain of calls. An attacker can "
        "trick a contract into using the caller's `tx.origin` to bypass checks."
    )
    impact_template = (
        "Phishing attacks can trick users into interacting with malicious contracts that then call the "
        "vulnerable contract, appearing as if the user is calling directly."
    )
    fix_template = (
        "Use `msg.sender` instead of `tx.origin` for authentication. If you need to know the original "
        "sender, consider other patterns or clearly document the risks."
    )

    def run_check(self, contract_data):
        findings = []
        import re
        pattern = re.compile(r'tx\.origin')
        for contract in contract_data:
            source = contract.get("source", "")
            matches = pattern.finditer(source)
            for match in matches:
                line = source[:match.start()].count('\n') + 1
                snippet = source[match.start():match.end()]
                findings.append(self._create_finding(
                    title="Use of tx.origin for authentication",
                    file=contract.get("path", ""),
                    line=line,
                    vulnerable_snippet=snippet,
                ))
        return findings
# EOF: hawki/core/static_rule_engine/rules/tx_origin_dependency.py