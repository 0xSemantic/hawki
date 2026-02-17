# --------------------
# File: hawki/core/static_rule_engine/__init__.py
# --------------------
"""
Static rule engine that auto‑discovers rule classes from the rules/ directory.
"""

import importlib
import pkgutil
import logging
from pathlib import Path
from typing import List, Dict, Any

from .rules import BaseRule

logger = logging.getLogger(__name__)

class RuleEngine:
    """Discovers and executes all rules against contract data."""

    def __init__(self):
        self.rules: List[BaseRule] = []
        self._discover_rules()

    def _discover_rules(self):
        """Dynamically import all modules in the rules package and instantiate rule classes."""
        package = "hawki.core.static_rule_engine.rules"
        # Convert Path to string to avoid AttributeError in pkgutil
        rules_dir = str(Path(__file__).parent / "rules")
        for _, module_name, _ in pkgutil.iter_modules([rules_dir]):
            full_module = f"{package}.{module_name}"
            try:
                module = importlib.import_module(full_module)
                # Find all classes that subclass BaseRule (excluding BaseRule itself)
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and issubclass(attr, BaseRule) and attr is not BaseRule:
                        self.rules.append(attr())
                        logger.debug(f"Loaded rule: {attr_name}")
            except Exception as e:
                logger.error(f"Failed to load rule module {full_module}: {e}")

    def run_all(self, contract_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Run all rules on the given contract data and collect findings."""
        findings = []
        for rule in self.rules:
            try:
                rule_findings = rule.run_check(contract_data)
                if rule_findings:
                    findings.extend(rule_findings)
            except Exception as e:
                logger.error(f"Rule {rule.__class__.__name__} failed: {e}")
        return findings

# EOF: hawki/core/static_rule_engine/__init__.py