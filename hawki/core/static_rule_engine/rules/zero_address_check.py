# --------------------
# File: hawki/core/static_rule_engine/rules/zero_address_check.py
# --------------------
"""
Missing zero‑address check: functions that accept addresses should check for zero address to prevent burning tokens or locking funds.
"""

import re
from . import BaseRule

class ZeroAddressCheckRule(BaseRule):
    severity = "Medium"
    explanation_template = (
        "When setting an address (e.g., owner, token recipient), it's important to check for the zero address (0x0). "
        "Otherwise, tokens could be sent to a burn address or ownership could be lost."
    )
    impact_template = (
        "Tokens sent to zero address are permanently lost. Ownership could be transferred to zero address, locking the contract."
    )
    fix_template = (
        "Add a require statement: `require(to != address(0), \"Invalid address\");`"
    )

    def run_check(self, contract_data):
        findings = []
        # Look for functions that take an address parameter and don't have a zero‑address check
        for contract in contract_data:
            for func in contract.get("functions", []):
                params = func.get("parameters", [])
                for param in params:
                    if param.get("type") == "address":
                        # Check if function body contains require with zero address
                        body = func.get("body", "")
                        if "require" not in body or "address(0)" not in body:
                            line = func.get("line", 1)
                            snippet = f"function {func['name']}(address {param['name']}) ..."
                            findings.append(self._create_finding(
                                title="Missing zero‑address check",
                                file=contract.get("path", ""),
                                line=line,
                                vulnerable_snippet=snippet,
                            ))
        return findings
# EOF: hawki/core/static_rule_engine/rules/zero_address_check.py