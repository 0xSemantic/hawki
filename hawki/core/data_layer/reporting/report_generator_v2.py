# --------------------
# File: hawki/core/data_layer/reporting/report_generator_v2.py
# --------------------
"""
Audit‑Grade Report Generator v2 (ARS v2).
Produces reports in Markdown, JSON, HTML, and PDF formats.
Integrates scoring engine and chart renderer, and links sandbox results to findings.
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from .scoring_engine import SecurityScoreEngine
from .chart_renderer import ChartRenderer

try:
    import jinja2
    JINJA2_AVAILABLE = True
except ImportError:
    JINJA2_AVAILABLE = False
    logging.getLogger(__name__).warning("jinja2 not installed. HTML and Markdown reports will be disabled.")

# Optional PDF dependencies
try:
    import pdfkit
    PDFKIT_AVAILABLE = True
except ImportError:
    PDFKIT_AVAILABLE = False

logger = logging.getLogger(__name__)


class ReportGeneratorV2:
    """Generates professional audit‑grade reports in multiple formats."""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.scoring_engine = SecurityScoreEngine()
        self.chart_renderer = ChartRenderer(output_dir / "charts")
        self.template_dir = Path(__file__).parent / "templates"

    def generate(
        self,
        repo_data: Dict[str, Any],
        findings: List[Dict[str, Any]],
        scan_metadata: Dict[str, Any],
        output_format: str = "md",
    ) -> Path:
        """
        Generate a report.

        Args:
            repo_data: Repository metadata (path, type, contracts, etc.) including sandbox_results if any.
            findings: List of finding dictionaries.
            scan_metadata: Dict with ai_enabled, sandbox_enabled, docker_available,
                           total_scanned_contracts, total_files, simulation_success_rate, mode.
            output_format: One of "md", "json", "html", "pdf".

        Returns:
            Path to the generated report file.
        """
        # Compute score
        score_result = self.scoring_engine.calculate(
            findings=findings,
            sandbox_results=repo_data.get("sandbox_results"),
            ai_enabled=scan_metadata.get("ai_enabled", False),
        )

        # Generate charts if format supports images (md, html, pdf) and matplotlib available
        chart_paths = []
        if output_format in ("md", "html", "pdf"):
            chart_paths = self.chart_renderer.generate_charts(findings)

        # Build report data context
        report_context = self._build_context(
            repo_data, findings, scan_metadata, score_result, chart_paths
        )

        # Render according to format
        if output_format == "json":
            return self._render_json(report_context)
        elif output_format == "md":
            return self._render_markdown(report_context)
        elif output_format == "html":
            return self._render_html(report_context)
        elif output_format == "pdf":
            return self._render_pdf(report_context)
        else:
            raise ValueError(f"Unsupported format: {output_format}")

    def _build_context(
        self,
        repo_data: Dict[str, Any],
        findings: List[Dict[str, Any]],
        scan_metadata: Dict[str, Any],
        score_result: Dict[str, Any],
        chart_paths: List[Path],
    ) -> Dict[str, Any]:
        """Assemble all data needed for templates."""
        # Prepare per‑finding details with fallbacks
        detailed_findings = []
        for idx, f in enumerate(findings, 1):
            detailed_findings.append({
                "id": f.get("id", f"F{idx:03d}"),
                "title": f.get("title", "Unknown Issue"),
                "severity": f.get("severity", "Low").upper(),
                "file": f.get("file", "unknown.sol"),
                "line": f.get("line", "?"),
                "vulnerable_snippet": f.get("vulnerable_snippet", "N/A"),
                "fix_snippet": f.get("fix_snippet", "No fix provided."),
                "explanation": f.get("explanation", "No explanation."),
                "impact": f.get("impact", "No impact analysis."),
                "exploit_steps": f.get("exploit_steps", []),
                "ai_used": f.get("ai_used", False),
            })

        # Severity counts
        severity_counts = {}
        for f in findings:
            sev = f.get("severity", "Low").capitalize()
            severity_counts[sev] = severity_counts.get(sev, 0) + 1

        # Process sandbox results and link to findings
        sandbox_results = repo_data.get("sandbox_results", [])
        sim_success_rate = None
        if sandbox_results:
            total = len(sandbox_results)
            successful = sum(1 for r in sandbox_results if r.get("success"))
            sim_success_rate = f"{successful}/{total} ({successful/total*100:.1f}%)" if total else "N/A"

            # Link successful exploits to findings
            for res in sandbox_results:
                if res.get("success"):
                    attack_name = res.get("attack_name", "").lower().replace("_attack", "").replace(".py", "")
                    for f in detailed_findings:
                        if attack_name in f["title"].lower() or attack_name in f.get("id", "").lower():
                            steps = [
                                f"Exploit succeeded using script: {res.get('attack_name')}",
                                f"Before balance: {res.get('before_balance', 'N/A')}",
                                f"After balance: {res.get('after_balance', 'N/A')}",
                                f"Gas used: {res.get('gas_used', 'N/A')}",
                                f"Transaction hash: {res.get('transaction_hash', 'N/A')}",
                                f"Logs: {res.get('logs', 'N/A')}"
                            ]
                            f["exploit_steps"] = steps
                            break

        # Chart relative paths (for embedding)
        chart_rel_paths = [p.name for p in chart_paths]

        return {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "scan_metadata": scan_metadata,
            "repo_data": repo_data,
            "findings": detailed_findings,
            "score": score_result,
            "severity_counts": severity_counts,
            "simulation_success_rate": sim_success_rate,
            "chart_paths": chart_rel_paths,
            "total_findings": len(findings),
        }

    def _render_json(self, context: Dict[str, Any]) -> Path:
        """Save context as JSON."""
        output_file = self.output_dir / f"report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, "w") as f:
            json.dump(context, f, indent=2)
        logger.info(f"JSON report saved to {output_file}")
        return output_file

    def _render_markdown(self, context: Dict[str, Any]) -> Path:
        """Render Markdown using Jinja2."""
        if not JINJA2_AVAILABLE:
            raise RuntimeError("jinja2 is required for Markdown reports. Install with 'pip install hawki[reports]'")

        template_path = self.template_dir / "markdown_template.md"
        if not template_path.exists():
            raise FileNotFoundError(f"Markdown template not found: {template_path}")

        env = jinja2.Environment(loader=jinja2.FileSystemLoader(self.template_dir))
        template = env.get_template("markdown_template.md")
        rendered = template.render(context)

        output_file = self.output_dir / f"report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.md"
        with open(output_file, "w") as f:
            f.write(rendered)
        logger.info(f"Markdown report saved to {output_file}")
        return output_file

    def _render_html(self, context: Dict[str, Any]) -> Path:
        """Render HTML using Jinja2."""
        if not JINJA2_AVAILABLE:
            raise RuntimeError("jinja2 is required for HTML reports. Install with 'pip install hawki[reports]'")

        template_path = self.template_dir / "html_template.html"
        if not template_path.exists():
            raise FileNotFoundError(f"HTML template not found: {template_path}")

        env = jinja2.Environment(loader=jinja2.FileSystemLoader(self.template_dir))
        template = env.get_template("html_template.html")
        rendered = template.render(context)

        output_file = self.output_dir / f"report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.html"
        with open(output_file, "w") as f:
            f.write(rendered)
        logger.info(f"HTML report saved to {output_file}")
        return output_file

    def _render_pdf(self, context: Dict[str, Any]) -> Path:
        """Generate PDF by first rendering HTML then converting with pdfkit."""
        if not PDFKIT_AVAILABLE:
            raise RuntimeError("pdfkit is required for PDF reports. Install with 'pip install hawki[pdf]'")

        # Render HTML first
        html_file = self._render_html(context)
        pdf_file = html_file.with_suffix(".pdf")

        try:
            pdfkit.from_file(str(html_file), str(pdf_file))
            logger.info(f"PDF report saved to {pdf_file}")
        except Exception as e:
            raise RuntimeError(f"PDF generation failed: {e}")

        return pdf_file

# EOF: hawki/core/data_layer/reporting/report_generator_v2.py