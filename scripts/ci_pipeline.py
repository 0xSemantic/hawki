#!/usr/bin/env python3
# --------------------
# File: scripts/ci_pipeline.py
# --------------------
"""
CI/CD integration script for Hawk-i.
Detects the CI environment (GitHub Actions, GitLab CI) and runs a scan,
outputting results in a format suitable for annotations or SARIF.
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path

# Add parent directory to path to allow importing hawk-i modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from hawki.core.repo_intelligence.indexer import RepositoryIndexer
from hawki.core.static_rule_engine import RuleEngine
from hawki.core.ai_engine.reasoning_agent import ReasoningAgent
from hawki.core.data_layer.report_manager import ReportManager

logger = logging.getLogger(__name__)

def setup_logging(verbose: bool = False):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

def detect_ci_environment() -> str:
    """Return the CI environment name: 'github', 'gitlab', or 'unknown'."""
    if os.getenv("GITHUB_ACTIONS") == "true":
        return "github"
    if os.getenv("GITLAB_CI") == "true":
        return "gitlab"
    return "unknown"

def format_github_annotation(findings: list) -> list:
    """Convert findings to GitHub Actions annotation commands."""
    annotations = []
    for f in findings:
        # GitHub workflow commands: https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions
        level = f.get("severity", "WARNING").lower()
        if level == "high":
            level = "error"
        elif level == "medium":
            level = "warning"
        else:
            level = "notice"
        # Try to extract file and line from location
        location = f.get("location", "")
        file = "unknown"
        line = 1
        if ":" in location:
            parts = location.split(":")
            file = parts[0]
            if len(parts) > 1 and parts[1].isdigit():
                line = parts[1]
        message = f.get("description", "No description")
        rule = f.get("rule", "unknown")
        annotation = f"::{level} file={file},line={line},title={rule}::{message}"
        annotations.append(annotation)
    return annotations

def format_gitlab_annotation(findings: list) -> list:
    """Convert findings to GitLab Code Quality report format (JSON)."""
    # GitLab Code Quality: https://docs.gitlab.com/ee/ci/testing/code_quality.html#implement-a-custom-tool
    issues = []
    for idx, f in enumerate(findings):
        location = f.get("location", "")
        file = location.split(":")[0] if ":" in location else "unknown"
        line = location.split(":")[1] if ":" in location and location.split(":")[1].isdigit() else 1
        severity = f.get("severity", "INFO").upper()
        # Map Hawk-i severity to GitLab severity
        gl_severity = {
            "HIGH": "critical",
            "MEDIUM": "major",
            "LOW": "minor",
            "INFO": "info"
        }.get(severity, "info")
        issue = {
            "type": "issue",
            "check_name": f.get("rule", "unknown"),
            "description": f.get("description", ""),
            "categories": ["Security"],
            "severity": gl_severity,
            "location": {
                "path": file,
                "lines": {
                    "begin": int(line)
                }
            }
        }
        issues.append(issue)
    return issues

def main():
    parser = argparse.ArgumentParser(description="Hawk-i CI Pipeline")
    parser.add_argument("target", nargs="?", default=".", help="Directory to scan (default: current directory)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging")
    parser.add_argument("--ai", action="store_true", help="Enable AI analysis (may be slow for CI)")
    parser.add_argument("--ai-model", help="LLM model")
    parser.add_argument("--api-key", help="API key for LLM")
    parser.add_argument("--output", choices=["annotations", "sarif", "json"], default="annotations",
                        help="Output format (default: annotations for CI)")
    parser.add_argument("--report-file", type=Path, help="Save full report to file (JSON)")
    args = parser.parse_args()

    setup_logging(args.verbose)

    ci_env = detect_ci_environment()
    logger.info(f"Detected CI environment: {ci_env}")

    indexer = RepositoryIndexer()
    engine = RuleEngine()
    report_mgr = ReportManager()  # not used directly

    ai_agent = None
    if args.ai:
        ai_agent = ReasoningAgent()
        if args.ai_model or args.api_key:
            from hawki.core.ai_engine.llm_orchestrator import LLMOrchestrator
            ai_agent.orchestrator = LLMOrchestrator(model=args.ai_model, api_key=args.api_key)

    try:
        # Index the target (local directory)
        repo_data = indexer.index(args.target)

        # Static analysis
        logger.info(f"Running {len(engine.rules)} static rules...")
        static_findings = engine.run_all(repo_data["contracts"])

        # AI analysis if enabled
        ai_findings = []
        if ai_agent:
            logger.info("Running AI reasoning...")
            ai_findings = ai_agent.analyse_contracts(repo_data["contracts"])
            logger.info(f"AI found {len(ai_findings)} potential issues")

        all_findings = static_findings + ai_findings

        # Output based on format
        if args.output == "json":
            print(json.dumps(all_findings, indent=2))
        elif args.output == "sarif":
            # For SARIF we'd need a converter; placeholder for now
            logger.warning("SARIF output not yet implemented, falling back to JSON")
            print(json.dumps(all_findings, indent=2))
        else:  # annotations
            if ci_env == "github":
                annotations = format_github_annotation(all_findings)
                for ann in annotations:
                    print(ann)
            elif ci_env == "gitlab":
                issues = format_gitlab_annotation(all_findings)
                # GitLab expects a JSON file named gl-code-quality-report.json
                output_file = Path("gl-code-quality-report.json")
                with open(output_file, "w") as f:
                    json.dump(issues, f)
                logger.info(f"GitLab Code Quality report written to {output_file}")
            else:
                # Unknown CI, print human-readable
                for f in all_findings:
                    print(f"[{f.get('severity','INFO')}] {f.get('rule','')}: {f.get('description','')} at {f.get('location','')}")

        # Optionally save full report
        if args.report_file:
            report_mgr.output_dir = args.report_file.parent
            report_mgr.save_findings(all_findings, repo_data)  # will generate timestamped file
            logger.info(f"Full report saved to {args.report_file}")

        # Exit with code 1 if any HIGH severity findings
        high_count = sum(1 for f in all_findings if f.get("severity") == "HIGH")
        if high_count > 0:
            logger.error(f"Found {high_count} HIGH severity issues")
            sys.exit(1)

    except Exception as e:
        logger.error(f"CI pipeline failed: {e}", exc_info=True)
        sys.exit(2)
    finally:
        indexer.cleanup()

if __name__ == "__main__":
    main()

# EOF: scripts/ci_pipeline.py