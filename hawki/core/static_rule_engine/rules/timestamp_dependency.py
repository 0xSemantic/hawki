# --------------------
# File: hawki/core/static_rule_engine/rules/timestamp_dependency.py
# --------------------
"""
Timestamp dependency: using block.timestamp for critical logic may be manipulated by miners.
"""

from . import BaseRule

class TimestampDependencyRule(BaseRule):
    severity = "Medium"
    explanation_template = (
        "Miners have some influence over `block.timestamp`. Using it for critical logic (e.g., time‑based "
        "transitions, deadlines) can be manipulated within a range of about 15 seconds."
    )
    impact_template = (
        "An attacker could manipulate timestamps to gain unfair advantages, such as delaying or accelerating "
        "time‑sensitive operations."
    )
    fix_template = (
        "Avoid relying on `block.timestamp` for precise logic. If necessary, accept a small variance "
        "or use a trusted oracle like Chainlink VRF for randomness."
    )

    def run_check(self, contract_data):
        findings = []
        import re
        pattern = re.compile(r'block\.timestamp')
        for contract in contract_data:
            source = contract.get("source", "")
            matches = pattern.finditer(source)
            for match in matches:
                line = source[:match.start()].count('\n') + 1
                snippet = source[match.start():match.end()]
                findings.append(self._create_finding(
                    title="Timestamp dependency",
                    file=contract.get("path", ""),
                    line=line,
                    vulnerable_snippet=snippet,
                ))
        return findings
# EOF: hawki/core/static_rule_engine/rules/timestamp_dependency.py