# --------------------
# File: hawki/core/static_rule_engine/rules/front_running.py
# --------------------
"""
Front‑running vulnerability: detect transaction ordering dependency.
"""

from . import BaseRule

class FrontRunningRule(BaseRule):
    severity = "Low"
    explanation_template = (
        "Using `block.timestamp` or `block.number` for critical logic can allow miners or bots to "
        "front‑run transactions by manipulating the block parameters or ordering."
    )
    impact_template = (
        "Attackers can exploit front‑running to gain unfair advantage, e.g., by seeing a pending trade "
        "and inserting their own transaction first."
    )
    fix_template = (
        "Avoid relying on block.timestamp or block.number for critical decisions. "
        "Use commit‑reveal schemes or other mechanisms that are resistant to front‑running."
    )

    def run_check(self, contract_data):
        findings = []
        import re
        patterns = [r'block\.timestamp', r'block\.number']
        for contract in contract_data:
            source = contract.get("source", "")
            for pattern in patterns:
                matches = re.finditer(pattern, source)
                for match in matches:
                    line = source[:match.start()].count('\n') + 1
                    snippet = source[match.start():match.end()]
                    findings.append(self._create_finding(
                        title="Potential front‑running via block.timestamp/number",
                        file=contract.get("path", ""),
                        line=line,
                        vulnerable_snippet=snippet,
                    ))
        return findings
# EOF: hawki/core/static_rule_engine/rules/front_running.py