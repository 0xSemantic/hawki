# --------------------
# File: cli/hawki_cli.py (updated for v0.7.0 with telemetry)
# --------------------
"""
Hawk-i command‑line interface – v0.7.0 with telemetry.
"""

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from hawki.core.repo_intelligence.indexer import RepositoryIndexer
from hawki.core.static_rule_engine import RuleEngine
from hawki.core.ai_engine.reasoning_agent import ReasoningAgent
from hawki.core.exploit_sandbox.sandbox_manager import SandboxManager
from hawki.core.data_layer.report_manager import ReportManager
from hawki.core.monitoring import Monitor
from hawki.core.telemetry import MetricsCollector, MetricsExporter, MetricsStore

# Try to import optional dependencies for reporting
try:
    import jinja2
    JINJA2_AVAILABLE = True
except ImportError:
    JINJA2_AVAILABLE = False

try:
    import matplotlib
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    import pdfkit
    PDFKIT_AVAILABLE = True
except ImportError:
    PDFKIT_AVAILABLE = False

def setup_logging(verbose: bool = False):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

def scan_command(args):
    """Handle 'scan' subcommand."""
    logger = logging.getLogger(__name__)
    indexer = RepositoryIndexer()
    engine = RuleEngine()
    report_mgr = ReportManager(output_dir=args.output_dir)

    ai_agent = None
    if args.ai:
        logger.info("AI analysis enabled")
        ai_agent = ReasoningAgent(orchestrator=None)
        if args.ai_model or args.api_key:
            from hawki.core.ai_engine.llm_orchestrator import LLMOrchestrator
            ai_agent.orchestrator = LLMOrchestrator(model=args.ai_model, api_key=args.api_key)

    # Check for optional dependencies if specific formats requested
    if args.format in ("html", "pdf") and not JINJA2_AVAILABLE:
        logger.error("HTML/PDF reports require jinja2. Install with 'pip install hawki[reports]'")
        sys.exit(1)
    if args.format == "pdf" and not PDFKIT_AVAILABLE:
        logger.error("PDF reports require pdfkit. Install with 'pip install hawki[pdf]'")
        sys.exit(1)
    if args.format in ("html", "pdf", "md") and not JINJA2_AVAILABLE:
        # Markdown also uses jinja2 now
        logger.error("Markdown/HTML/PDF reports require jinja2. Install with 'pip install hawki[reports]'")
        sys.exit(1)

    try:
        logger.info(f"Scanning target: {args.target}")
        repo_data = indexer.index(args.target)

        total_files = len([p for p in Path(repo_data["path"]).rglob("*.sol")])
        total_contracts = sum(len(c.get("contracts", [])) for c in repo_data.get("contracts", []))

        logger.info(f"Running {len(engine.rules)} static rules...")
        static_findings = engine.run_all(repo_data["contracts"])

        ai_findings = []
        if ai_agent:
            logger.info("Running AI reasoning...")
            ai_findings = ai_agent.analyse_contracts(repo_data["contracts"])
            logger.info(f"AI found {len(ai_findings)} potential issues")

        all_findings = static_findings + ai_findings

        sandbox_results = []
        docker_available = False
        if args.sandbox:
            logger.info("Starting exploit simulation sandbox...")
            repo_path = Path(repo_data["path"]) if repo_data["type"] == "remote" else Path(repo_data["path"])
            sandbox = SandboxManager(repo_path)
            sandbox_results = sandbox.run_all()
            logger.info(f"Sandbox completed with {len(sandbox_results)} attack script results")
            repo_data["sandbox_results"] = sandbox_results
            docker_available = True

        scan_metadata = {
            "ai_enabled": args.ai,
            "sandbox_enabled": args.sandbox,
            "docker_available": docker_available,
            "total_scanned_contracts": total_contracts,
            "total_files": total_files,
            "mode": "minimal",
            "version": "0.7.0",  # should come from package metadata
        }
        if args.ai and args.sandbox:
            scan_metadata["mode"] = "full"
        elif args.ai:
            scan_metadata["mode"] = "enhanced"
        else:
            scan_metadata["mode"] = "minimal"

        # Generate report
        if args.format:
            report_path = report_mgr.generate_report(
                findings=all_findings,
                repo_data=repo_data,
                scan_metadata=scan_metadata,
                output_format=args.format,
            )
        else:
            report_path = report_mgr.save_findings(all_findings, repo_data)

        logger.info(f"Scan complete. Total findings: {len(all_findings)}")
        print(f"\nReport saved to: {report_path}")

        # Telemetry (opt‑in)
        if args.telemetry:
            logger.info("Collecting anonymous usage metrics (opt‑in)")
            collector = MetricsCollector()
            metrics = collector.collect_from_scan(scan_metadata, repo_data, all_findings)
            # Attempt to export in background? For simplicity, we export now.
            exporter = MetricsExporter()
            exporter.export()
            print("Telemetry data recorded locally and sent anonymously (thank you!).")
        else:
            print("Telemetry not enabled. Use --telemetry to help us improve Hawk‑i.")

    except Exception as e:
        logger.error(f"Scan failed: {e}", exc_info=True)
        sys.exit(1)
    finally:
        indexer.cleanup()

def monitor_command(args):
    """Handle 'monitor' subcommand."""
    # ... (unchanged from previous) ...
    # We'll keep it as is; no telemetry for monitor.

def report_command(args):
    """Generate a report from an existing findings file."""
    # ... (unchanged) ...

def score_command(args):
    """Calculate and display security score from findings file."""
    # ... (unchanged) ...

def metrics_command(args):
    """Display local telemetry stats."""
    from hawki.core.telemetry import MetricsStore
    store = MetricsStore()
    all_metrics = store.get_all()
    if not all_metrics:
        print("No telemetry data recorded yet.")
        return

    total_scans = len(all_metrics)
    # Compute aggregated stats
    total_findings = sum(sum(m["findings"].values()) for m in all_metrics)
    critical = sum(m["findings"].get("Critical", 0) for m in all_metrics)
    high = sum(m["findings"].get("High", 0) for m in all_metrics)
    medium = sum(m["findings"].get("Medium", 0) for m in all_metrics)
    low = sum(m["findings"].get("Low", 0) for m in all_metrics)

    print(f"Total scans: {total_scans}")
    print(f"Total findings: {total_findings} (Critical: {critical}, High: {high}, Medium: {medium}, Low: {low})")
    if args.verbose:
        print("\nDetailed records:")
        for m in all_metrics:
            print(f"  {m['timestamp']} - mode: {m['mode']}, findings: {m['findings']}")

def main():
    parser = argparse.ArgumentParser(description="Hawk-i Security Scanner v0.7.0")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Subcommands")

    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Perform a one-time scan")
    scan_parser.add_argument("target", help="Local directory path or Git repository URL")
    scan_parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging")
    scan_parser.add_argument("-o", "--output-dir", type=Path, help="Directory to store reports (default: ./hawki_reports)")
    scan_parser.add_argument("--ai", action="store_true", help="Enable AI‑powered analysis")
    scan_parser.add_argument("--ai-model", help="LLM model (e.g., gemini/gemini-1.5-flash, openai/gpt-4)")
    scan_parser.add_argument("--api-key", help="API key for the chosen LLM (or set env var)")
    scan_parser.add_argument("--sandbox", action="store_true", help="Run exploit simulation sandbox (requires Docker)")
    scan_parser.add_argument("--format", choices=["md", "json", "html", "pdf"], default=None,
                             help="Output report format (if omitted, legacy JSON report is generated)")
    scan_parser.add_argument("--telemetry", action="store_true", help="Opt in to anonymous usage metrics")
    scan_parser.set_defaults(func=scan_command)

    # Monitor command (unchanged)
    monitor_parser = subparsers.add_parser("monitor", help="Continuously monitor targets")
    monitor_parser.add_argument("target", nargs="?", help="Local Git repository path (optional if config provided)")
    monitor_parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging")
    monitor_parser.add_argument("-c", "--config", type=Path, help="JSON configuration file for watchers")
    monitor_parser.add_argument("--state-dir", type=Path, help="Directory to store watcher state (default: ~/.hawki/monitor_state)")
    monitor_parser.add_argument("--alert-log", type=Path, help="File to append alerts to")
    monitor_parser.add_argument("--interval", type=int, default=60, help="Polling interval in seconds")
    monitor_parser.add_argument("--branch", help="Git branch to monitor (default: main)")
    monitor_parser.add_argument("--contract-address", help="Ethereum contract address to monitor")
    monitor_parser.add_argument("--rpc-url", help="RPC URL for contract monitoring (default: http://localhost:8545)")
    monitor_parser.set_defaults(func=monitor_command)

    # Report command
    report_parser = subparsers.add_parser("report", help="Generate a report from existing findings")
    report_parser.add_argument("-i", "--input", type=Path, help="Findings JSON file (default: latest in output dir)")
    report_parser.add_argument("-o", "--output-dir", type=Path, help="Output directory for report (default: ./hawki_reports)")
    report_parser.add_argument("-f", "--format", choices=["md", "json", "html", "pdf"], default="md",
                               help="Output format (default: md)")
    report_parser.set_defaults(func=report_command)

    # Score command
    score_parser = subparsers.add_parser("score", help="Calculate security score from findings file")
    score_parser.add_argument("input", type=Path, help="Findings JSON file")
    score_parser.add_argument("-v", "--verbose", action="store_true", help="Show deduction details")
    score_parser.set_defaults(func=score_command)

    # Metrics command
    metrics_parser = subparsers.add_parser("metrics", help="Display local telemetry stats")
    metrics_parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed records")
    metrics_parser.set_defaults(func=metrics_command)

    args = parser.parse_args()
    setup_logging(getattr(args, 'verbose', False))
    args.func(args)

if __name__ == "__main__":
    main()

# EOF: cli/hawki_cli.py