# --------------------
# File: hawki/core/data_layer/reporting/chart_renderer.py
# --------------------
"""
Chart Renderer – generates severity pie chart and vulnerability type bar chart.
Uses matplotlib if available; otherwise logs a warning and returns empty list.
"""

import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    logger.warning("matplotlib not installed. Chart generation disabled.")


class ChartRenderer:
    """Generates visual charts from findings data."""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_charts(self, findings: List[Dict[str, Any]]) -> List[Path]:
        """
        Create severity pie chart and vulnerability type bar chart.
        Returns list of paths to generated PNG images (empty if matplotlib unavailable).
        """
        if not MATPLOTLIB_AVAILABLE:
            logger.debug("Skipping chart generation (matplotlib not installed)")
            return []

        if not findings:
            logger.debug("No findings to chart")
            return []

        chart_paths = []

        # 1. Severity pie chart
        severity_counts = {}
        for f in findings:
            sev = f.get("severity", "Low").capitalize()
            severity_counts[sev] = severity_counts.get(sev, 0) + 1

        if severity_counts:
            fig, ax = plt.subplots(figsize=(8, 6))
            colors = {"Critical": "#8B0000", "High": "#FF4500", "Medium": "#FFA500", "Low": "#32CD32"}
            wedges, texts, autotexts = ax.pie(
                severity_counts.values(),
                labels=severity_counts.keys(),
                autopct="%1.1f%%",
                colors=[colors.get(k, "#687F97") for k in severity_counts.keys()],
                textprops={"color": "white", "fontsize": 12},
            )
            ax.set_title("Findings by Severity", color="white", fontsize=16)
            plt.tight_layout()
            pie_path = self.output_dir / "severity_pie.png"
            plt.savefig(pie_path, facecolor="#0c0c0c", edgecolor="none")
            plt.close()
            chart_paths.append(pie_path)

        # 2. Vulnerability type bar chart (top 10)
        type_counts = {}
        for f in findings:
            vuln_type = f.get("title", "").split()[0] if f.get("title") else "Unknown"
            type_counts[vuln_type] = type_counts.get(vuln_type, 0) + 1

        if type_counts:
            sorted_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            types, counts = zip(*sorted_types) if sorted_types else ([], [])

            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(types, counts, color="#687F97")
            ax.set_xlabel("Vulnerability Type", color="white")
            ax.set_ylabel("Count", color="white")
            ax.set_title("Top Vulnerability Types", color="white", fontsize=16)
            ax.tick_params(axis="x", rotation=45, colors="white")
            ax.tick_params(axis="y", colors="white")
            for spine in ax.spines.values():
                spine.set_color("#77746C")
            plt.tight_layout()
            bar_path = self.output_dir / "type_bar.png"
            plt.savefig(bar_path, facecolor="#0c0c0c", edgecolor="none")
            plt.close()
            chart_paths.append(bar_path)

        return chart_paths

# EOF: hawki/core/data_layer/reporting/chart_renderer.py