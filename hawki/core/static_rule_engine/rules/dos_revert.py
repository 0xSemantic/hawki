# --------------------
# File: hawki/core/static_rule_engine/rules/dos_revert.py
# --------------------
"""
Denial of Service via unexpected revert: functions that can be forced to revert by an attacker.
"""

import re
from . import BaseRule

class DoSRevertRule(BaseRule):
    severity = "High"
    explanation_template = (
        "If a function can be forced to revert by an attacker (e.g., by making an external call that fails, "
        "or by manipulating state), it can lead to denial of service, locking funds or preventing legitimate use."
    )
    impact_template = (
        "An attacker could block critical contract functionality, such as withdrawals or governance votes, "
        "causing financial loss or governance paralysis."
    )
    fix_template = (
        "Avoid relying on external calls that can fail without alternatives. Use pull‑over‑push patterns, "
        "or handle failures gracefully (e.g., log and continue)."
    )

    def run_check(self, contract_data):
        findings = []
        # Look for patterns where an external call is not checked and could revert the whole function
        # For example: `address.call(...);` without `require` or `if`
        for contract in contract_data:
            source = contract.get("source", "")
            lines = source.split('\n')
            for i, line in enumerate(lines):
                if ".call" in line and "require" not in line and "if" not in line:
                    # Also check if it's the only thing after that
                    findings.append(self._create_finding(
                        title="Potential DoS via unchecked external call",
                        file=contract.get("path", ""),
                        line=i+1,
                        vulnerable_snippet=line.strip(),
                    ))
        return findings
# EOF: hawki/core/static_rule_engine/rules/dos_revert.py