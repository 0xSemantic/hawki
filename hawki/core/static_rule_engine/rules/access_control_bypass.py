# --------------------
# File: hawki/core/static_rule_engine/rules/access_control_bypass.py
# --------------------
"""
Access control bypass: detect missing modifiers on sensitive functions.
"""

import re
from . import BaseRule

class AccessControlBypassRule(BaseRule):
    severity = "Critical"
    explanation_template = (
        "Sensitive functions (e.g., `withdraw`, `setOwner`, `pause`) must be protected by access control modifiers "
        "like `onlyOwner`. Without such protection, any user can call these functions and compromise the contract."
    )
    impact_template = (
        "An attacker can drain funds, change critical parameters, or take ownership of the contract."
    )
    fix_template = (
        "Add a modifier to restrict access:\n"
        "```solidity\n"
        "modifier onlyOwner() {\n"
        "    require(msg.sender == owner, \"Not owner\");\n"
        "    _;\n"
        "}\n"
        "function {{function_name}}() {{visibility}} onlyOwner {\n"
        "    // ...\n"
        "}\n"
        "```"
    )

    def run_check(self, contract_data):
        findings = []
        sensitive_names = ["withdraw", "transferOwnership", "destroy", "kill", "setOwner", "pause", "unpause", "setImplementation"]
        for contract in contract_data:
            for func in contract.get("functions", []):
                func_name = func.get("name", "")
                if any(s in func_name.lower() for s in sensitive_names):
                    modifiers = func.get("modifiers", [])
                    # Look for common access control modifiers
                    if not any(mod in ["onlyOwner", "onlyAdmin", "authorized", "hasRole"] for mod in modifiers):
                        # Try to extract line number (crude)
                        source = contract.get("source", "")
                        # Find function definition line (simplistic)
                        pattern = rf"function\s+{func_name}\s*\([^)]*\)"
                        match = re.search(pattern, source)
                        line = source[:match.start()].count('\n') + 1 if match else 1
                        snippet = func.get("body", "")[:100] if func.get("body") else ""
                        findings.append(self._create_finding(
                            title=f"Missing access control on {func_name}",
                            file=contract.get("path", ""),
                            line=line,
                            vulnerable_snippet=snippet,
                            function_name=func_name,
                            visibility=func.get("visibility", "public"),
                        ))
        return findings
# EOF: hawki/core/static_rule_engine/rules/access_control_bypass.py