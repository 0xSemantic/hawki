# --------------------
# File: hawki/core/static_rule_engine/rules/upgrade_admin.py
# --------------------
"""
UpgradeAdmin – Detects improper upgrade admin transfer mechanisms.
If the admin of an upgradeable proxy can be changed by anyone without access control,
an attacker could take over the contract.
"""

import re
from . import BaseRule

class UpgradeAdminRule(BaseRule):
    severity = "Medium"
    explanation_template = (
        "In upgradeable contracts, the admin address controls upgrades. If the function that changes the admin "
        "is unprotected (e.g., no `onlyOwner` modifier), any user can set themselves as admin and then upgrade "
        "to a malicious implementation, compromising the contract."
    )
    impact_template = (
        "An attacker can take permanent control of the contract, drain funds, or brick the contract by upgrading "
        "to a malicious implementation."
    )
    fix_template = (
        "Add access control to the admin change function, e.g., `onlyOwner` modifier. Ensure that only the current "
        "admin or a privileged role can change the admin address.\n"
        "```solidity\n"
        "function changeAdmin(address newAdmin) public onlyOwner {\n"
        "    require(newAdmin != address(0), \"Zero address\");\n"
        "    admin = newAdmin;\n"
        "}\n"
        "```"
    )

    def run_check(self, contract_data):
        findings = []
        # Look for functions that change an admin-like variable
        admin_keywords = ["admin", "owner", "governance", "implementation"]
        for contract in contract_data:
            source = contract.get("source", "")
            for func in contract.get("functions", []):
                func_name = func.get("name", "")
                body = func.get("body", "")
                # If function name suggests admin change and has no access control
                if any(k in func_name.lower() for k in ["changeadmin", "setadmin", "updateadmin", "transferownership"]):
                    # Check if it has modifiers like onlyOwner
                    modifiers = func.get("modifiers", [])
                    if not any(mod in ["onlyOwner", "onlyAdmin", "onlyGovernance"] for mod in modifiers):
                        line = func.get("line", 1)
                        snippet = f"function {func_name}(...)"
                        findings.append(self._create_finding(
                            title="Unprotected upgrade admin change",
                            file=contract.get("path", ""),
                            line=line,
                            vulnerable_snippet=snippet,
                        ))
                # Also look for assignments to admin variable without checks
                # This is simplified; we could check for `admin = ...` in public functions
                if "admin =" in body and "require" not in body and "modifier" not in body:
                    line = func.get("line", 1)
                    snippet = f"function {func_name}() ... // contains admin ="
                    findings.append(self._create_finding(
                        title="Admin variable assignment without access control",
                        file=contract.get("path", ""),
                        line=line,
                        vulnerable_snippet=snippet,
                    ))
        return findings
# EOF: hawki/core/static_rule_engine/rules/upgrade_admin.py