# --------------------
# File: hawki/core/static_rule_engine/rules/reentrancy.py
# --------------------
"""
Reentrancy detection: flags external calls after state changes without reentrancy guards.
"""

from typing import List, Dict, Any
from . import BaseRule

class ReentrancyRule(BaseRule):
    severity = "Critical"
    explanation_template = (
        "Reentrancy occurs when a function makes an external call before updating its own state. "
        "The external call can invoke the same function again, leading to recursive calls and draining funds."
    )
    impact_template = (
        "An attacker can steal all funds from the contract by recursively calling the vulnerable function."
    )
    fix_template = (
        "Apply the checks‑effects‑interactions pattern: update state before making external calls, "
        "and consider using a reentrancy guard modifier like OpenZeppelin's `nonReentrant`."
    )

    def run_check(self, contract_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        findings = []
        for contract in contract_data:
            for func in contract.get("functions", []):
                # Simplified: check if function does an external call and doesn't have nonReentrant
                # In real implementation, we'd need to analyze function body.
                # For demo, we flag payable functions without nonReentrant.
                if func.get("state_mutability") == "payable" and "nonReentrant" not in func.get("modifiers", []):
                    line = func.get("line", 0)
                    snippet = f"function {func.get('name')}() payable ..."
                    findings.append(self._create_finding(
                        title="Potential reentrancy vulnerability",
                        file=contract.get("path", ""),
                        line=line,
                        vulnerable_snippet=snippet,
                        function_name=func.get('name'),
                        visibility=func.get('visibility', 'public'),
                    ))
        return findings
# EOF: hawki/core/static_rule_engine/rules/reentrancy.py