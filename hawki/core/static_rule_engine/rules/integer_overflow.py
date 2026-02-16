# --------------------
# File: hawki/core/static_rule_engine/rules/integer_overflow.py
# --------------------
"""
Integer overflow/underflow: detect usage of arithmetic operations without SafeMath (or solidity >=0.8.0).
For Phase 1, we simply check if contract uses <0.8.0 and has arithmetic.
"""

from . import BaseRule

class IntegerOverflowRule(BaseRule):
    def run_check(self, contract_data):
        findings = []
        # In a real implementation we'd need pragma parsing. Here we assume <0.8.0 and flag all arithmetic.
        # Placeholder: flag any contract that uses + - * / without checked math.
        for contract in contract_data:
            # simplistic: if source contains + - * / and no using SafeMath, flag
            source = contract.get("source", "")
            if ("+" in source or "-" in source or "*" in source or "/" in source) and "using SafeMath" not in source:
                findings.append({
                    "rule": "IntegerOverflow",
                    "severity": "MEDIUM",
                    "description": "Arithmetic operations may overflow/underflow without SafeMath or Solidity 0.8+.",
                    "location": contract.get("path"),
                })
        return findings
# EOF: hawki/core/static_rule_engine/rules/integer_overflow.py