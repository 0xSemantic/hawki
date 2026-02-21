# --------------------
# File: hawki/core/static_rule_engine/rules/blockhash_randomness.py
# --------------------
"""
Blockhash as randomness source: using blockhash for randomness is insecure because it can be manipulated by miners.
"""

import re
from . import BaseRule

class BlockhashRandomnessRule(BaseRule):
    severity = "High"
    explanation_template = (
        "Using `blockhash` or `block.blockhash` as a source of randomness is insecure because miners can influence it. "
        "They can choose to withhold blocks or manipulate the hash to their advantage."
    )
    impact_template = (
        "An attacker could predict or manipulate the randomness, leading to unfair outcomes in games, lotteries, "
        "or other mechanisms that rely on unpredictable values."
    )
    fix_template = (
        "Use a verifiable randomness source like Chainlink VRF, or a commit‑reveal scheme with a future blockhash "
        "that cannot be influenced by the caller."
    )

    def run_check(self, contract_data):
        findings = []
        patterns = [r'block\.blockhash', r'blockhash\(']
        for contract in contract_data:
            source = contract.get("source", "")
            for pattern in patterns:
                matches = re.finditer(pattern, source)
                for match in matches:
                    line = source[:match.start()].count('\n') + 1
                    snippet = source[match.start():match.end()]
                    findings.append(self._create_finding(
                        title="Insecure randomness via blockhash",
                        file=contract.get("path", ""),
                        line=line,
                        vulnerable_snippet=snippet,
                    ))
        return findings
# EOF