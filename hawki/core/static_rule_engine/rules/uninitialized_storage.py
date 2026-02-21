# --------------------
# File: hawki/core/static_rule_engine/rules/uninitialized_storage.py
# --------------------
"""
Uninitialized storage pointers: detect local storage variables that point to default slot 0.
"""

from . import BaseRule

class UninitializedStorageRule(BaseRule):
    severity = "High"
    explanation_template = (
        "Local storage variables that are not initialized will point to storage slot 0 by default. "
        "This can accidentally overwrite important contract state if the variable is used without assignment."
    )
    impact_template = (
        "An attacker could exploit this to corrupt contract storage, leading to loss of funds or contract takeover."
    )
    fix_template = (
        "Always initialize local storage variables explicitly, or avoid using storage pointers when not needed. "
        "If you need a storage reference, ensure it points to a valid state variable."
    )

    def run_check(self, contract_data):
        findings = []
        # Look for " storage " keyword without " = "
        import re
        pattern = re.compile(r'(\w+)\s+storage\s+(\w+)\s*(?!=)')
        for contract in contract_data:
            source = contract.get("source", "")
            matches = pattern.finditer(source)
            for match in matches:
                line = source[:match.start()].count('\n') + 1
                snippet = source[match.start():match.end()]
                findings.append(self._create_finding(
                    title="Uninitialized storage pointer",
                    file=contract.get("path", ""),
                    line=line,
                    vulnerable_snippet=snippet,
                ))
        return findings
# EOF: hawki/core/static_rule_engine/rules/uninitialized_storage.py