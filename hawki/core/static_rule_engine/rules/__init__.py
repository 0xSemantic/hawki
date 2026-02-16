# --------------------
# File: hawki/core/static_rule_engine/rules/__init__.py
# --------------------
"""
Base rule class and rule loader.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseRule(ABC):
    """Abstract base class for all static analysis rules."""

    @abstractmethod
    def run_check(self, contract_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Execute the rule on the provided contract data.
        Returns a list of findings (dictionaries with at least 'rule', 'severity', 'description', 'location').
        """
        pass

# EOF: hawki/core/static_rule_engine/rules/__init__.py