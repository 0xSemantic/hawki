# --------------------
# File: hawki/core/static_rule_engine/rules/unsafe_external_call.py
# --------------------
"""
Unsafe external call with state change after: detect external calls that are followed by state changes.
"""

from . import BaseRule

class UnsafeExternalCallRule(BaseRule):
    severity = "Critical"
    explanation_template = (
        "Making an external call (e.g., transferring ETH) before updating internal state allows the called contract to re‑enter "
        "and exploit the incomplete state, leading to reentrancy attacks."
    )
    impact_template = (
        "An attacker can drain funds by re‑entering the function before state updates."
    )
    fix_template = (
        "Apply the checks‑effects‑interactions pattern: update state before making external calls, or use a reentrancy guard."
    )

    def run_check(self, contract_data):
        findings = []
        # Look for patterns: .call{...}(...) followed by state updates (assignments)
        # This is complex; for demo we'll flag any function that does .call and then has state writes.
        for contract in contract_data:
            for func in contract.get("functions", []):
                func_body = func.get("body", "")
                if ".call" in func_body:
                    # Check if there are assignments after the call
                    lines = func_body.split('\n')
                    call_line = None
                    for i, line in enumerate(lines):
                        if ".call" in line:
                            call_line = i
                            break
                    if call_line is not None and call_line < len(lines) - 1:
                        # Look for '=' after call line (simplistic)
                        for j in range(call_line+1, len(lines)):
                            if '=' in lines[j] and not lines[j].strip().startswith('//'):
                                line_num = func.get("line", 0) + call_line + 1
                                snippet = lines[call_line].strip()
                                findings.append(self._create_finding(
                                    title="External call before state update (reentrancy risk)",
                                    file=contract.get("path", ""),
                                    line=line_num,
                                    vulnerable_snippet=snippet,
                                    function_name=func.get("name"),
                                ))
                                break
        return findings
# EOF