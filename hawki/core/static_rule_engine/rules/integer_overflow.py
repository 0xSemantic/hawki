# --------------------
# File: hawki/core/static_rule_engine/rules/integer_overflow.py
# --------------------
"""
Integer overflow/underflow: detect usage of arithmetic operations without SafeMath or Solidity >=0.8.0.
"""

from . import BaseRule

class IntegerOverflowRule(BaseRule):
    severity = "Medium"
    explanation_template = (
        "Arithmetic operations in Solidity versions prior to 0.8.0 can overflow/underflow silently, "
        "leading to incorrect balances or logic. Even in 0.8.x, `unchecked` blocks can reintroduce overflow."
    )
    impact_template = (
        "An attacker could manipulate arithmetic to gain unexpected tokens or break contract invariants."
    )
    fix_template = (
        "Use Solidity 0.8.0 or later (which includes built‑in overflow checks), or use SafeMath library. "
        "If `unchecked` is necessary, ensure values are bounded and cannot overflow."
    )

    def run_check(self, contract_data):
        findings = []
        # This is a simplified detection; in practice we'd need pragma parsing.
        # For Phase 2, we'll flag any contract with arithmetic operations.
        import re
        arith_ops = re.compile(r'[\+\-\*/]')
        for contract in contract_data:
            source = contract.get("source", "")
            # Check if contract uses arithmetic and is not using SafeMath
            if arith_ops.search(source) and "using SafeMath" not in source:
                # Crude line number for first occurrence
                match = arith_ops.search(source)
                line = source[:match.start()].count('\n') + 1
                snippet = source[match.start():match.start()+10] if match else ""
                findings.append(self._create_finding(
                    title="Potential integer overflow/underflow",
                    file=contract.get("path", ""),
                    line=line,
                    vulnerable_snippet=snippet,
                ))
        return findings
# EOF: hawki/core/static_rule_engine/rules/integer_overflow.py