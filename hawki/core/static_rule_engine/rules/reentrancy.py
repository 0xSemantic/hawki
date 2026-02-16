# --------------------
# File: hawki/core/static_rule_engine/rules/reentrancy.py
# --------------------
"""
Reentrancy detection: flags external calls after state changes without reentrancy guards.
"""

from typing import List, Dict, Any
from . import BaseRule

class ReentrancyRule(BaseRule):
    def run_check(self, contract_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        findings = []
        for contract in contract_data:
            for func in contract.get("functions", []):
                # simplistic: if function is not protected by nonReentrant and makes external calls
                # For Phase 1, we'll just flag all payable functions (placeholder)
                if func.get("state_mutability") == "payable" and "nonReentrant" not in func.get("modifiers", []):
                    findings.append({
                        "rule": "Reentrancy",
                        "severity": "HIGH",
                        "description": "Payable function without reentrancy guard may be vulnerable to reentrancy.",
                        "location": f"{contract.get('name')}.{func.get('name')}",
                    })
        return findings