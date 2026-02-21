# --------------------
# File: hawki/core/static_rule_engine/rules/visibility.py
# --------------------
"""
Improper visibility: functions that should be internal are marked public.
"""

import re
from . import BaseRule

class VisibilityRule(BaseRule):
    severity = "High"
    explanation_template = (
        "Functions that are only meant to be called internally should be marked `internal` or `private`. "
        "If they are `public`, they can be called by anyone, potentially exposing sensitive logic."
    )
    impact_template = (
        "An attacker could call internal functions directly, bypassing access controls or causing unexpected behavior."
    )
    fix_template = (
        "Change the visibility to `internal` or `private` if the function is not meant to be part of the public interface."
    )

    def run_check(self, contract_data):
        findings = []
        # Look for functions that look like internal helpers but are public
        # This is subjective; we'll flag functions with names like "_internal" or that are called only internally
        # For simplicity, flag any function that is public and not in an interface
        for contract in contract_data:
            for func in contract.get("functions", []):
                if func.get("visibility") == "public" and func.get("name", "").startswith("_"):
                    line = func.get("line", 1)
                    snippet = f"function {func['name']}() public ..."
                    findings.append(self._create_finding(
                        title="Public function that may be internal",
                        file=contract.get("path", ""),
                        line=line,
                        vulnerable_snippet=snippet,
                    ))
        return findings
# EOF: hawki/core/static_rule_engine/rules/visibility.py