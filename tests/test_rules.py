# --------------------
# File: tests/test_rules.py (updated)
# --------------------
"""
Unit tests for static rules.
"""

import unittest
from hawki.core.static_rule_engine import RuleEngine
from hawki.core.static_rule_engine.rules.reentrancy import ReentrancyRule

class TestRules(unittest.TestCase):
    def test_reentrancy_rule(self):
        rule = ReentrancyRule()
        contract_data = [{
            "name": "Vault",
            "functions": [
                {"name": "withdraw", "state_mutability": "payable", "modifiers": []}
            ]
        }]
        findings = rule.run_check(contract_data)
        self.assertEqual(len(findings), 1)
        # Check fields set by the rule itself
        self.assertEqual(findings[0]["title"], "Potential reentrancy vulnerability")
        self.assertEqual(findings[0]["severity"], "Critical")
        self.assertIn("function_name", findings[0])
        self.assertEqual(findings[0]["function_name"], "withdraw")

    def test_engine_discovery(self):
        engine = RuleEngine()
        # At least the 10 rules we defined should be loaded
        self.assertGreaterEqual(len(engine.rules), 10)

if __name__ == "__main__":
    unittest.main()