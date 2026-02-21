# --------------------
# File: hawki/core/static_rule_engine/rules/missing_initializer.py
# --------------------
"""
Missing initializer in UUPS upgradeable contracts.
Detects upgradeable contracts that lack an initializer function or are missing the initializer modifier.
"""

from . import BaseRule
import re

class MissingInitializerRule(BaseRule):
    severity = "Critical"
    explanation_template = (
        "Upgradeable contracts (UUPS or transparent proxies) must have an initializer function instead of a constructor. "
        "The initializer function should be protected by the `initializer` modifier to prevent re‑initialization."
    )
    impact_template = (
        "Without a proper initializer, the contract may be left uninitialized, allowing anyone to take ownership "
        "or set critical parameters, leading to complete compromise."
    )
    fix_template = (
        "Add an initializer function with the `initializer` modifier:\n"
        "```solidity\n"
        "function initialize() public initializer {\n"
        "    __Ownable_init();\n"
        "    // set initial state\n"
        "}\n"
        "```"
    )

    def run_check(self, contract_data):
        findings = []
        for contract in contract_data:
            source = contract.get("source", "")
            # Check if contract inherits from UUPSUpgradeable or similar
            if re.search(r'is\s+.*(UUPSUpgradeable|Initializable)', source):
                # Look for a function with the initializer modifier
                has_initializer = False
                for func in contract.get("functions", []):
                    if "initializer" in func.get("modifiers", []):
                        has_initializer = True
                        break
                if not has_initializer:
                    findings.append(self._create_finding(
                        title="Missing initializer in upgradeable contract",
                        file=contract.get("path", ""),
                        line=1,  # placeholder
                        vulnerable_snippet="Contract inherits from upgradeable base but has no initializer.",
                    ))
        return findings
# EOF: hawki/core/static_rule_engine/rules/missing_initializer.py