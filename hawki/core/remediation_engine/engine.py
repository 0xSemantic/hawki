# --------------------
# File: hawki/core/remediation_engine/engine.py
# --------------------
"""
RemediationEngine class: loads templates and populates fix snippets using AST context.
"""

import json
import logging
import re
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class RemediationEngine:
    """Generates fix snippets from templates and AST context."""

    def __init__(self, templates_dir: Optional[Path] = None):
        self.templates_dir = templates_dir or Path(__file__).parent / "templates"
        self.templates: Dict[str, Dict[str, str]] = {}
        self._load_templates()

    def _load_templates(self):
        """Load all JSON templates from the templates directory."""
        if not self.templates_dir.exists():
            logger.warning(f"Templates directory not found: {self.templates_dir}")
            return
        for template_file in self.templates_dir.glob("*.json"):
            try:
                with open(template_file, "r") as f:
                    template_data = json.load(f)
                rule_name = template_file.stem  # e.g., "reentrancy"
                self.templates[rule_name] = template_data
                logger.debug(f"Loaded remediation template: {rule_name}")
            except Exception as e:
                logger.error(f"Failed to load template {template_file}: {e}")

    def get_fix(self, finding: Dict[str, Any], context: Dict[str, Any]) -> str:
        """
        Generate a fix snippet for a given finding using the appropriate template.

        Args:
            finding: The finding dictionary, must contain a rule identifier (e.g., rule class name).
            context: AST‑derived context (function names, variable names, etc.).

        Returns:
            A string with the populated fix snippet, or a generic message if no template.
        """
        # Determine rule identifier: use rule class name or title
        rule_name = finding.get("rule", "").lower()
        if not rule_name:
            # Try to extract from title
            title = finding.get("title", "")
            if "reentrancy" in title.lower():
                rule_name = "reentrancy"
            elif "access control" in title.lower():
                rule_name = "access_control"
            else:
                # fallback to first word
                rule_name = title.split()[0].lower() if title else "generic"

        template = self.templates.get(rule_name)
        if not template:
            logger.debug(f"No remediation template for rule '{rule_name}', using generic")
            return "No specific fix snippet available. Review the code and apply secure patterns."

        fix_template = template.get("fix_snippet", "")
        if not fix_template:
            return "No fix snippet defined in template."

        # Replace placeholders using context
        return self._populate_placeholders(fix_template, context)

    def _populate_placeholders(self, template: str, context: Dict[str, Any]) -> str:
        """
        Replace {{placeholder}} with values from context.
        """
        def replacer(match):
            key = match.group(1).strip()
            # Allow nested keys like "function.name"
            parts = key.split('.')
            value = context
            for part in parts:
                if isinstance(value, dict):
                    value = value.get(part, "")
                else:
                    return ""
            return str(value) if value is not None else ""

        return re.sub(r'\{\{\s*([^}]+)\s*\}\}', replacer, template)

# EOF: hawki/core/remediation_engine/engine.py