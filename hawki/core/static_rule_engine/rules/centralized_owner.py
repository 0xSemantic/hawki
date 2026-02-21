# --------------------
# File: hawki/core/static_rule_engine/rules/centralized_owner.py
# --------------------
"""
CentralizedOwner – Flags contracts with a single owner that has absolute power.
This is a systemic risk, not a direct vulnerability, but important for governance assessment.
"""

import re
from . import BaseRule

class CentralizedOwnerRule(BaseRule):
    severity = "Low"
    explanation_template = (
        "This contract has a single owner with absolute control over critical functions (e.g., withdrawal, upgrades, pausing). "
        "While not an immediate vulnerability, it introduces centralization risk: if the owner's private key is compromised, "
        "the entire contract is compromised."
    )
    impact_template = (
        "A compromised owner account can drain funds, pause the contract indefinitely, or upgrade to a malicious implementation."
    )
    fix_template = (
        "Consider using a multi‑signature wallet for the owner account, or implement a timelock and/or a DAO‑based governance "
        "mechanism to decentralize control."
    )

    def run_check(self, contract_data):
        findings = []
        for contract in contract_data:
            # Look for an owner variable and functions that use onlyOwner
            source = contract.get("source", "")
            has_owner = False
            if "owner" in source or "admin" in source:
                has_owner = True
            # Count how many functions use onlyOwner
            only_owner_count = 0
            for func in contract.get("functions", []):
                modifiers = func.get("modifiers", [])
                if "onlyOwner" in modifiers:
                    only_owner_count += 1
            if has_owner and only_owner_count > 0:
                # Determine line for owner declaration
                match = re.search(r'(address|address\s+public|address\s+internal)\s+owner\s*;', source)
                line = source[:match.start()].count('\n') + 1 if match else 1
                snippet = match.group(0) if match else "owner variable"
                findings.append(self._create_finding(
                    title="Centralized owner risk",
                    file=contract.get("path", ""),
                    line=line,
                    vulnerable_snippet=snippet,
                ))
        return findings
# EOF: hawki/core/static_rule_engine/rules/centralized_owner.py