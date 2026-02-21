# --------------------
# File: hawki/core/static_rule_engine/rules/approval_race.py
# --------------------
"""
Improper ERC20 approval race condition: detect missing allowance checks that could lead to double spending.
"""

from . import BaseRule

class ApprovalRaceRule(BaseRule):
    severity = "Critical"
    explanation_template = (
        "The standard ERC20 `approve` function is vulnerable to a race condition: if an owner changes allowance from N to M, "
        "and the spender submits a transfer before the new approval, they can spend N and then M, exceeding the intended limit."
    )
    impact_template = (
        "An attacker can spend more tokens than allowed, leading to theft."
    )
    fix_template = (
        "Use OpenZeppelin's `safeApprove` or `increaseAllowance`/`decreaseAllowance` to mitigate the race condition. "
        "Alternatively, require the new allowance to be zero before changing it."
    )

    def run_check(self, contract_data):
        findings = []
        # Look for approve function without protection
        for contract in contract_data:
            for func in contract.get("functions", []):
                if func.get("name") == "approve":
                    # Check if it uses safe pattern (e.g., require allowance == 0)
                    body = func.get("body", "")
                    if "require" not in body or "allowance" not in body:
                        line = func.get("line", 1)
                        snippet = "function approve(address spender, uint256 amount) ..."
                        findings.append(self._create_finding(
                            title="ERC20 approval race condition",
                            file=contract.get("path", ""),
                            line=line,
                            vulnerable_snippet=snippet,
                        ))
        return findings
# EOF: hawki/core/static_rule_engine/rules/approval_race.py