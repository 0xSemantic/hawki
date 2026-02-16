# --------------------
# File: hawki/core/data_layer/report_manager.py (updated)
# --------------------
"""
Handles persistence of scan results, including sandbox outcomes.
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class ReportManager:
    """Manages report generation and storage."""

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or Path.cwd() / "hawki_reports"
        self.output_dir.mkdir(exist_ok=True)

    def save_findings(self, findings: List[Dict[str, Any]], repo_info: Dict[str, Any]) -> Path:
        """Save findings and optional sandbox results to a timestamped JSON file."""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        report_file = self.output_dir / f"report_{timestamp}.json"

        report_data = {
            "scan_timestamp": timestamp,
            "repository": {k: v for k, v in repo_info.items() if k != "contracts"},  # exclude large source
            "findings": findings,
            "summary": {
                "total_findings": len(findings),
                "severity_counts": self._count_severities(findings),
            }
        }

        # Include sandbox results if present
        if "sandbox_results" in repo_info:
            report_data["sandbox_results"] = repo_info["sandbox_results"]
            report_data["summary"]["sandbox_scripts_run"] = len(repo_info["sandbox_results"])
            report_data["summary"]["sandbox_successful"] = sum(
                1 for r in repo_info["sandbox_results"] if r.get("success")
            )

        with open(report_file, "w") as f:
            json.dump(report_data, f, indent=2)

        logger.info(f"Report saved to {report_file}")
        return report_file

    def _count_severities(self, findings: List[Dict]) -> Dict[str, int]:
        counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
        for f in findings:
            sev = f.get("severity", "INFO")
            counts[sev] = counts.get(sev, 0) + 1
        return counts

# EOF: hawki/core/data_layer/report_manager.py