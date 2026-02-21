# --------------------
# File: hawki/core/data_layer/report_manager.py (updated for v0.7.0)
# --------------------
"""
Handles persistence of scan results, including sandbox outcomes.
Now supports audit‑grade reporting via ReportGeneratorV2.
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

from .reporting.report_generator_v2 import ReportGeneratorV2

logger = logging.getLogger(__name__)

class ReportManager:
    """Manages report generation and storage."""

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or Path.cwd() / "hawki_reports"
        self.output_dir.mkdir(exist_ok=True)
        self.v2_generator = ReportGeneratorV2(self.output_dir)

    def save_findings(self, findings: List[Dict[str, Any]], repo_info: Dict[str, Any]) -> Path:
        """Legacy method: save findings as JSON only."""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        report_file = self.output_dir / f"report_{timestamp}.json"

        report_data = {
            "scan_timestamp": timestamp,
            "repository": {k: v for k, v in repo_info.items() if k != "contracts"},
            "findings": findings,
            "summary": {
                "total_findings": len(findings),
                "severity_counts": self._count_severities(findings),
            }
        }

        if "sandbox_results" in repo_info:
            report_data["sandbox_results"] = repo_info["sandbox_results"]
            report_data["summary"]["sandbox_scripts_run"] = len(repo_info["sandbox_results"])
            report_data["summary"]["sandbox_successful"] = sum(
                1 for r in repo_info["sandbox_results"] if r.get("success")
            )

        with open(report_file, "w") as f:
            json.dump(report_data, f, indent=2)

        logger.info(f"Legacy report saved to {report_file}")
        return report_file

    def generate_report(
        self,
        findings: List[Dict[str, Any]],
        repo_data: Dict[str, Any],
        scan_metadata: Dict[str, Any],
        output_format: str = "md",
    ) -> Path:
        """
        Generate an audit‑grade report using ARS v2.
        This is the new method; it preserves backward compatibility.
        """
        return self.v2_generator.generate(
            repo_data=repo_data,
            findings=findings,
            scan_metadata=scan_metadata,
            output_format=output_format,
        )

    def _count_severities(self, findings: List[Dict]) -> Dict[str, int]:
        counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
        for f in findings:
            sev = f.get("severity", "INFO")
            counts[sev] = counts.get(sev, 0) + 1
        return counts

# EOF: hawki/core/data_layer/report_manager.py