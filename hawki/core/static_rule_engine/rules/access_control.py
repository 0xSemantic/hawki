# --------------------
# File: hawki/core/static_rule_engine/rules/access_control.py
# --------------------
"""
Access control: checks for missing onlyOwner or similar modifiers on sensitive functions.
"""

from . import BaseRule

class AccessControlRule(BaseRule):
    def run_check(self, contract_data):
        findings = []
        for contract in contract_data:
            # simplistic: flag any function named "withdraw", "transferOwnership", etc. without onlyOwner modifier
            sensitive_names = ["withdraw", "transferOwnership", "destroy", "kill"]
            for func in contract.get("functions", []):
                if any(name in func["name"] for name in sensitive_names):
                    if "onlyOwner" not in func.get("modifiers", []):
                        findings.append({
                            "rule": "AccessControl",
                            "severity": "HIGH",
                            "description": f"Sensitive function '{func['name']}' lacks access control modifier.",
                            "location": f"{contract.get('name')}.{func.get('name')}",
                        })
        return findings