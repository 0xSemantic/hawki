# --------------------
# File: hawki/core/static_rule_engine/rules/hardcoded_address.py
# --------------------
"""
Hardcoded privileged address: using a fixed address for critical roles reduces flexibility and trust.
"""

import re
from . import BaseRule

class HardcodedAddressRule(BaseRule):
    severity = "Medium"
    explanation_template = (
        "Hardcoding an address (e.g., owner, admin) in the contract code makes it immutable and reduces trust. "
        "If the private key is compromised, the contract cannot be updated."
    )
    impact_template = (
        "If the hardcoded address is compromised, the attacker gains permanent control over the contract. "
        "Also, the contract cannot be upgraded to change ownership."
    )
    fix_template = (
        "Use a constructor parameter to set the address at deployment, and include an upgrade mechanism if needed. "
        "Consider using OpenZeppelin's Ownable with a transferable owner."
    )

    def run_check(self, contract_data):
        findings = []
        # Look for addresses that look like Ethereum addresses (0x...) in the code
        address_pattern = re.compile(r'0x[a-fA-F0-9]{40}')
        for contract in contract_data:
            source = contract.get("source", "")
            matches = address_pattern.finditer(source)
            for match in matches:
                line = source[:match.start()].count('\n') + 1
                snippet = source[match.start():match.end()]
                findings.append(self._create_finding(
                    title="Hardcoded address",
                    file=contract.get("path", ""),
                    line=line,
                    vulnerable_snippet=snippet,
                ))
        return findings
# EOF: hawki/core/static_rule_engine/rules/hardcoded_address.py