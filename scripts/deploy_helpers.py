#!/usr/bin/env python3
# --------------------
# File: scripts/deploy_helpers.py
# --------------------
"""
Helper functions for integrating Hawk-i with development tools:
- Foundry (forge)
- Hardhat
- Remix
Provides functions to run scans on compiled contracts and generate audit reports.
"""

import json
import logging
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from hawki.core.repo_intelligence.indexer import RepositoryIndexer
from hawki.core.static_rule_engine import RuleEngine
from hawki.core.ai_engine.reasoning_agent import ReasoningAgent
from hawki.core.data_layer.report_manager import ReportManager

logger = logging.getLogger(__name__)

def run_scan_on_directory(
    directory: Path,
    use_ai: bool = False,
    ai_model: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Run a full Hawk-i scan on a directory containing Solidity source files.
    Returns a dictionary with findings and repository info.
    """
    indexer = RepositoryIndexer()
    engine = RuleEngine()
    ai_agent = None
    if use_ai:
        ai_agent = ReasoningAgent()
        if ai_model or api_key:
            from hawki.core.ai_engine.llm_orchestrator import LLMOrchestrator
            ai_agent.orchestrator = LLMOrchestrator(model=ai_model, api_key=api_key)

    try:
        repo_data = indexer.index(str(directory))
        static_findings = engine.run_all(repo_data["contracts"])
        ai_findings = []
        if ai_agent:
            ai_findings = ai_agent.analyse_contracts(repo_data["contracts"])
        all_findings = static_findings + ai_findings
        return {
            "repository": repo_data,
            "findings": all_findings,
            "summary": {
                "total": len(all_findings),
                "high": sum(1 for f in all_findings if f.get("severity") == "HIGH"),
                "medium": sum(1 for f in all_findings if f.get("severity") == "MEDIUM"),
                "low": sum(1 for f in all_findings if f.get("severity") == "LOW"),
            }
        }
    finally:
        indexer.cleanup()

def integrate_with_foundry(project_root: Path, use_ai: bool = False) -> Path:
    """
    Run Hawk-i on a Foundry project (assumes src/ contains contracts).
    Returns path to generated report.
    """
    src_dir = project_root / "src"
    if not src_dir.exists():
        raise ValueError(f"Foundry project must have src/ directory: {src_dir}")
    result = run_scan_on_directory(src_dir, use_ai=use_ai)
    report_mgr = ReportManager(output_dir=project_root / "hawki-reports")
    report_path = report_mgr.save_findings(result["findings"], result["repository"])
    logger.info(f"Foundry integration complete. Report: {report_path}")
    return report_path

def integrate_with_hardhat(project_root: Path, use_ai: bool = False) -> Path:
    """
    Run Hawk-i on a Hardhat project (assumes contracts/ directory).
    Returns path to generated report.
    """
    contracts_dir = project_root / "contracts"
    if not contracts_dir.exists():
        raise ValueError(f"Hardhat project must have contracts/ directory: {contracts_dir}")
    result = run_scan_on_directory(contracts_dir, use_ai=use_ai)
    report_mgr = ReportManager(output_dir=project_root / "hawki-reports")
    report_path = report_mgr.save_findings(result["findings"], result["repository"])
    logger.info(f"Hardhat integration complete. Report: {report_path}")
    return report_path

def integrate_with_remix(workspace_path: Path, use_ai: bool = False) -> Path:
    """
    Run Hawk-i on a Remix workspace (directory containing contracts).
    Returns path to generated report.
    """
    if not workspace_path.exists():
        raise ValueError(f"Remix workspace path does not exist: {workspace_path}")
    result = run_scan_on_directory(workspace_path, use_ai=use_ai)
    report_mgr = ReportManager(output_dir=workspace_path / "hawki-reports")
    report_path = report_mgr.save_findings(result["findings"], result["repository"])
    logger.info(f"Remix integration complete. Report: {report_path}")
    return report_path

def generate_audit_readme(report_path: Path, output_md: Path) -> None:
    """
    Generate a human-readable audit summary Markdown file from a JSON report.
    """
    with open(report_path, 'r') as f:
        report = json.load(f)
    findings = report.get("findings", [])
    summary = report.get("summary", {})
    with open(output_md, 'w') as f:
        f.write(f"# Hawk-i Security Audit Report\n\n")
        f.write(f"**Scan Time:** {report.get('scan_timestamp', 'unknown')}\n\n")
        f.write(f"## Summary\n")
        f.write(f"- Total Findings: {summary.get('total_findings', 0)}\n")
        f.write(f"- High: {summary.get('severity_counts', {}).get('HIGH', 0)}\n")
        f.write(f"- Medium: {summary.get('severity_counts', {}).get('MEDIUM', 0)}\n")
        f.write(f"- Low: {summary.get('severity_counts', {}).get('LOW', 0)}\n\n")
        f.write(f"## Findings\n\n")
        for idx, fnd in enumerate(findings, 1):
            f.write(f"### {idx}. {fnd.get('rule', 'Unknown')} - {fnd.get('severity', 'INFO')}\n")
            f.write(f"**Location:** {fnd.get('location', 'N/A')}\n\n")
            f.write(f"{fnd.get('description', 'No description')}\n\n")
    logger.info(f"Audit README generated: {output_md}")

# If run as script, provide a simple CLI
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Hawk-i Deployment Helpers")
    parser.add_argument("command", choices=["foundry", "hardhat", "remix", "readme"])
    parser.add_argument("path", help="Project root path")
    parser.add_argument("--ai", action="store_true", help="Enable AI analysis")
    parser.add_argument("--output", help="Output file for readme command")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    if args.command == "foundry":
        integrate_with_foundry(Path(args.path), use_ai=args.ai)
    elif args.command == "hardhat":
        integrate_with_hardhat(Path(args.path), use_ai=args.ai)
    elif args.command == "remix":
        integrate_with_remix(Path(args.path), use_ai=args.ai)
    elif args.command == "readme":
        if not args.output:
            print("Error: --output required for readme command")
            sys.exit(1)
        generate_audit_readme(Path(args.path), Path(args.output))

# EOF: scripts/deploy_helpers.py