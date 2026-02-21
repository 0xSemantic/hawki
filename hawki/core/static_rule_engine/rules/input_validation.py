# --------------------
# File: hawki/core/static_rule_engine/rules/input_validation.py
# --------------------
"""
Improper input validation: missing bounds checks on user-supplied values.
"""

from . import BaseRule

class InputValidationRule(BaseRule):
    severity = "High"
    explanation_template = (
        "User‑supplied inputs should be validated to prevent out‑of‑bounds errors, integer overflows, "
        "or unexpected behavior. Missing checks can lead to vulnerabilities like underflows or access to invalid indices."
    )
    impact_template = (
        "An attacker could supply values that cause array index errors, arithmetic issues, or bypass logic."
    )
    fix_template = (
        "Add input validation using `require` statements: e.g., `require(amount > 0, \"amount must be >0\")`, "
        "`require(index < array.length, \"index out of bounds\")`."
    )

    def run_check(self, contract_data):
        findings = []
        # Look for array indexing without length check
        for contract in contract_data:
            source = contract.get("source", "")
            # Find array access like arr[x] where x is a variable
            # This is complex; we'll flag any function that uses array index without a require on length
            lines = source.split('\n')
            for i, line in enumerate(lines):
                if '[' in line and ']' in line and 'length' not in line and 'require' not in line:
                    # crude
                    findings.append(self._create_finding(
                        title="Possible missing input validation",
                        file=contract.get("path", ""),
                        line=i+1,
                        vulnerable_snippet=line.strip(),
                    ))
        return findings
# EOF: hawki/core/static_rule_engine/rules/input_validation.py