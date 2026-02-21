# --------------------
# File: hawki/core/static_rule_engine/rules/__init__.py
# --------------------
"""
Base rule class and rule loader.
Now includes explanation, impact, and fix templates for remediation.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class BaseRule(ABC):
    """Abstract base class for all static analysis rules."""

    # Rule metadata (should be overridden by subclasses)
    severity = "INFO"  # Default, override in subclass
    explanation_template = "No explanation provided."
    impact_template = "No impact analysis provided."
    fix_template = "No fix snippet available."

    @abstractmethod
    def run_check(self, contract_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Execute the rule on the provided contract data.
        Returns a list of findings (dictionaries). Each finding should contain at least:
            - 'title': short description
            - 'severity': string (Critical, High, Medium, Low)
            - 'file': relative path
            - 'line': int
            - 'vulnerable_snippet': the exact code lines
        Additional fields (explanation, impact, fix_snippet) will be merged by the RuleEngine.
        """
        pass

    def _create_finding(self, title: str, file: str, line: int, vulnerable_snippet: str,
                        severity: Optional[str] = None, **extra) -> Dict[str, Any]:
        """
        Helper to create a finding dictionary with consistent fields.
        The RuleEngine will later add explanation, impact, and fix_snippet.
        """
        finding = {
            "title": title,
            "severity": severity or self.severity,
            "file": file,
            "line": line,
            "vulnerable_snippet": vulnerable_snippet,
        }
        finding.update(extra)
        return finding

# EOF: hawki/core/static_rule_engine/rules/__init__.py