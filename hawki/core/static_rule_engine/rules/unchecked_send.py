# --------------------
# File: hawki/core/static_rule_engine/rules/unchecked_send.py
# --------------------
"""
Unchecked send: detect send() or transfer() calls without checking return value.
"""

from . import BaseRule

class UncheckedSendRule(BaseRule):
    severity = "Medium"
    explanation_template = (
        "`send()` and `transfer()` return a boolean indicating success. If you don't check this return value, "
        "the function may silently fail, leading to incorrect contract state."
    )
    impact_template = (
        "Failed transfers could leave the contract in an inconsistent state, possibly locking funds or "
        "allowing users to withdraw more than they should."
    )
    fix_template = (
        "Always check the return value of `send()` or `transfer()` with `require`:\n"
        "```solidity\n"
        "bool success = address(...).send(amount);\n"
        "require(success, \"Transfer failed\");\n"
        "```"
    )

    def run_check(self, contract_data):
        findings = []
        import re
        # Look for send or transfer that is not inside an if or require
        # This is simplified: we'll flag any send/transfer that appears without "if" or "require" on the same line.
        pattern = re.compile(r'(send|transfer)\(')
        for contract in contract_data:
            source = contract.get("source", "")
            lines = source.split('\n')
            for i, line in enumerate(lines):
                if re.search(r'(send|transfer)\(', line) and not re.search(r'(if|require)\s*\(', line):
                    findings.append(self._create_finding(
                        title="Unchecked send/transfer",
                        file=contract.get("path", ""),
                        line=i+1,
                        vulnerable_snippet=line.strip(),
                    ))
        return findings
# EOF: hawki/core/static_rule_engine/rules/unchecked_send.py