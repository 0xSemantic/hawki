# --------------------
# File: hawki/core/static_rule_engine/rules/flash_loan_manipulation.py
# --------------------
"""
Flash loan manipulation: detect price calculations that can be manipulated via flash loans.
"""

import re
from . import BaseRule

class FlashLoanManipulationRule(BaseRule):
    severity = "Critical"
    explanation_template = (
        "Using spot prices derived from pool reserves in the same transaction allows an attacker to take a flash loan, "
        "manipulate the price, and profit before repaying the loan."
    )
    impact_template = (
        "An attacker can drain funds by artificially inflating/deflating prices and trading against the protocol."
    )
    fix_template = (
        "Use time‑weighted average prices (TWAP) or oracles like Chainlink. Avoid relying on instantaneous spot prices."
    )

    def run_check(self, contract_data):
        findings = []
        # Look for price calculations that depend on token balances or reserves
        patterns = [
            r'getReserves\(\)',
            r'balanceOf\(address\(this\)\)',
            r'reserve0',
            r'reserve1',
            r'price\s*=\s*\w+\.balanceOf\(address\(this\)\)\s*[/*]',
        ]
        for contract in contract_data:
            source = contract.get("source", "")
            for pattern in patterns:
                matches = re.finditer(pattern, source)
                for match in matches:
                    line = source[:match.start()].count('\n') + 1
                    snippet = source[match.start():match.end()]
                    findings.append(self._create_finding(
                        title="Potential flash loan manipulation",
                        file=contract.get("path", ""),
                        line=line,
                        vulnerable_snippet=snippet,
                    ))
        return findings
# EOF: hawki/core/static_rule_engine/rules/flash_loan_manipulation.py