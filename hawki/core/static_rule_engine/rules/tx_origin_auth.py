# --------------------
# File: hawki/core/static_rule_engine/rules/tx_origin_auth.py
# --------------------
"""
tx.origin used for authentication – critical risk.
"""

import re
from . import BaseRule

class TxOriginAuthRule(BaseRule):
    severity = "Critical"
    explanation_template = (
        "Using `tx.origin` for authentication is dangerous because it represents the original sender of the transaction. "
        "If a contract uses `tx.origin` to authorize critical actions, an attacker can trick a user into interacting with a malicious "
        "contract that then calls the vulnerable contract, appearing as if the user is calling directly."
    )
    impact_template = (
        "An attacker can perform privileged actions on behalf of the user, such as stealing funds or changing ownership."
    )
    fix_template = (
        "Use `msg.sender` instead of `tx.origin` for authentication. If you must know the original sender, consider using "
        "`tx.origin` only for specific use cases like preventing multi‑contract attacks, but never for authorization."
    )

    def run_check(self, contract_data):
        findings = []
        pattern = re.compile(r'tx\.origin')
        for contract in contract_data:
            source = contract.get("source", "")
            # Find occurrences of tx.origin, especially in require statements or if conditions
            matches = pattern.finditer(source)
            for match in matches:
                line = source[:match.start()].count('\n') + 1
                snippet = source[match.start():match.end()]
                # Check if it's used in a condition (likely for auth)
                surrounding = source[max(0, match.start()-30):min(len(source), match.end()+30)]
                if 'require' in surrounding or 'if' in surrounding:
                    findings.append(self._create_finding(
                        title="tx.origin used for authentication",
                        file=contract.get("path", ""),
                        line=line,
                        vulnerable_snippet=snippet,
                    ))
        return findings
# EOF: hawki/core/static_rule_engine/rules/tx_origin_auth.py