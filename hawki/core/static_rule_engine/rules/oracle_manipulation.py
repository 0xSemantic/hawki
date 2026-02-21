# --------------------
# File: hawki/core/static_rule_engine/rules/oracle_manipulation.py
# --------------------
"""
Oracle price manipulation: detect usage of spot prices from manipulatable sources.
"""

from . import BaseRule
import re

class OracleManipulationRule(BaseRule):
    severity = "Critical"
    explanation_template = (
        "Using a spot price from a single on‑chain source (e.g., a pool's reserve ratio) without manipulation resistance "
        "allows attackers to temporarily skew the price with a large trade or flash loan, then profit from the distorted price."
    )
    impact_template = (
        "An attacker can drain funds by manipulating the oracle and then trading against the protocol."
    )
    fix_template = (
        "Use a time‑weighted average price (TWAP) oracle like Uniswap V2's `price0CumulativeLast`, or a decentralized "
        "oracle network like Chainlink. Avoid using instantaneous spot prices."
    )

    def run_check(self, contract_data):
        findings = []
        # Look for simple price calculations based on balances
        patterns = [
            r'balance\s*[Aa]\.balanceOf\(.*\)\s*[/*]',
            r'getReserves\(\)',
            r'price\s*=\s*\w+\.balanceOf\(address\(this\)\)',
        ]
        for contract in contract_data:
            source = contract.get("source", "")
            for pattern in patterns:
                matches = re.finditer(pattern, source)
                for match in matches:
                    line = source[:match.start()].count('\n') + 1
                    snippet = source[match.start():match.end()]
                    findings.append(self._create_finding(
                        title="Potential oracle manipulation",
                        file=contract.get("path", ""),
                        line=line,
                        vulnerable_snippet=snippet,
                    ))
        return findings
# EOF: hawki/core/static_rule_engine/rules/oracle_manipulation.py