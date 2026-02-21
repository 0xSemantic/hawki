# --------------------
# File: cli/hawki_cli.py (final ruff‑clean with noqa)
# --------------------
"""
Hawk-i command‑line interface – v0.7.0 with telemetry and rich output.
"""

import argparse
import importlib.util
import json
import logging
import sys
from pathlib import Path

# Rich imports for beautiful CLI
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.table import Table
from rich.traceback import install

# Install rich traceback handler for pretty errors
install()

# Ensure we can import hawkki modules (must be before local imports)
sys.path.insert(0, str(Path(__file__).parent.parent))

# Local imports – ruff E402 is ignored because of path manipulation above
from hawki.core.ai_engine.reasoning_agent import ReasoningAgent  # noqa: E402
from hawki.core.data_layer.report_manager import ReportManager  # noqa: E402
from hawki.core.exploit_sandbox.sandbox_manager import SandboxManager  # noqa: E402
from hawki.core.repo_intelligence.indexer import RepositoryIndexer  # noqa: E402
from hawki.core.static_rule_engine import RuleEngine  # noqa: E402
from hawki.core.telemetry import MetricsCollector, MetricsExporter, MetricsStore  # noqa: E402

# Check optional dependencies
JINJA2_AVAILABLE = importlib.util.find_spec("jinja2") is not None
MATPLOTLIB_AVAILABLE = importlib.util.find_spec("matplotlib") is not None
PDFKIT_AVAILABLE = importlib.util.find_spec("pdfkit") is not None

console = Console()

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
        console.log("[cyan]AI analysis enabled[/cyan]")
        ai_agent = ReasoningAgent(orchestrator=None)
        if args.ai_model or args.api_key:
            from hawki.core.ai_engine.llm_orchestrator import LLMOrchestrator
            ai_agent.orchestrator = LLMOrchestrator(model=args.ai_model, api_key=args.api_key)

    # Check for optional dependencies if specific formats requested
    if args.format in ("html", "pdf") and not JINJA2_AVAILABLE:
        console.print("[red]HTML/PDF reports require jinja2. Install with 'pip install hawki[reports]'[/red]")
        sys.exit(1)
    if args.format == "pdf" and not PDFKIT_AVAILABLE:
        console.print("[red]PDF reports require pdfkit. Install with 'pip install hawki[pdf]'[/red]")
        sys.exit(1)
    if args.format in ("html", "pdf", "md") and not JINJA2_AVAILABLE:
        console.print("[red]Markdown/HTML/PDF reports require jinja2. Install with 'pip install hawki[reports]'[/red]")
        sys.exit(1)

    try:
        console.print(f"[bold green]Scanning target:[/bold green] {args.target}")
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("[cyan]Indexing repository...", total=1)
            repo_data = indexer.index(args.target)
            progress.update(task, advance=1)

            total_files = len([p for p in Path(repo_data["path"]).rglob("*.sol")])
            total_contracts = sum(len(c.get("contracts", [])) for c in repo_data.get("contracts", []))

            task = progress.add_task(f"[cyan]Running {len(engine.rules)} static rules...", total=1)
            static_findings = engine.run_all(repo_data["contracts"])
            progress.update(task, advance=1)

            ai_findings = []
            if ai_agent:
                task = progress.add_task("[cyan]Running AI reasoning...", total=1)
                ai_findings = ai_agent.analyse_contracts(repo_data["contracts"])
                progress.update(task, advance=1)

            all_findings = static_findings + ai_findings

            sandbox_results = []
            docker_available = False
            if args.sandbox:
                task = progress.add_task("[cyan]Starting exploit simulation sandbox...", total=1)
                repo_path = Path(repo_data["path"]) if repo_data["type"] == "remote" else Path(repo_data["path"])
                sandbox = SandboxManager(repo_path)
                sandbox_results = sandbox.run_all()
                progress.update(task, advance=1)
                repo_data["sandbox_results"] = sandbox_results
                docker_available = True

        scan_metadata = {
            "ai_enabled": args.ai,
            "sandbox_enabled": args.sandbox,
            "docker_available": docker_available,
            "total_scanned_contracts": total_contracts,
            "total_files": total_files,
            "mode": "minimal",
            "version": "0.7.0",
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

        console.print(f"[bold green]Scan complete.[/bold green] Total findings: {len(all_findings)}")
        console.print(f"[cyan]Report saved to:[/cyan] {report_path}")

        # Telemetry (opt‑in)
        if args.telemetry:
            console.log("[cyan]Collecting anonymous usage metrics (opt‑in)[/cyan]")
            collector = MetricsCollector()
            collector.collect_from_scan(scan_metadata, repo_data, all_findings)
            exporter = MetricsExporter()
            exporter.export()
            console.print("[green]Telemetry data recorded locally and sent anonymously (thank you!).[/green]")
        else:
            console.print("[dim]Telemetry not enabled. Use --telemetry to help us improve Hawk‑i.[/dim]")

    except Exception as e:
        logger.error(f"Scan failed: {e}", exc_info=True)
        console.print_exception()
        sys.exit(1)
    finally:
        indexer.cleanup()

def monitor_command(args):
    """Handle 'monitor' subcommand."""
    from hawki.core.monitoring import Monitor
    config = {}
    if args.config:
        with open(args.config, 'r') as f:
            config = json.load(f)
    else:
        if args.target:
            config = {
                "repocommitwatcher": {
                    "repo_path": args.target,
                    "branch": args.branch or "main"
                }
            }
        if args.contract_address:
            config["deployedcontractwatcher"] = {
                "rpc_url": args.rpc_url or "http://localhost:8545",
                "contract_address": args.contract_address
            }

    monitor = Monitor(
        watcher_configs=config,
        state_dir=args.state_dir,
        alert_log_file=args.alert_log
    )
    interval = args.interval or 60
    console.print("[cyan]Monitoring started. Press Ctrl+C to stop.[/cyan]")
    try:
        monitor.run_forever(interval_seconds=interval)
    except KeyboardInterrupt:
        console.print("\n[yellow]Monitoring stopped by user.[/yellow]")
        sys.exit(0)

def report_command(args):
    """Generate a report from an existing findings file."""
    logger = logging.getLogger(__name__)
    from hawki.core.data_layer.report_manager import ReportManager
    report_mgr = ReportManager(output_dir=args.output_dir)

    input_path = args.input
    if not input_path:
        report_files = sorted(Path(args.output_dir or ".").glob("report_*.json"))
        if not report_files:
            logger.error("No findings file specified and no previous scan found.")
            sys.exit(1)
        input_path = report_files[-1]

    try:
        with open(input_path, "r") as f:
            data = json.load(f)
    except Exception as e:
        logger.error(f"Failed to load findings file {input_path}: {e}")
        sys.exit(1)

    findings = data.get("findings", [])
    repo_data = data.get("repository", {"path": "unknown", "type": "unknown"})
    if "sandbox_results" in data:
        repo_data["sandbox_results"] = data["sandbox_results"]

    scan_metadata = {
        "ai_enabled": False,
        "sandbox_enabled": "sandbox_results" in data,
        "docker_available": False,
        "total_scanned_contracts": len(repo_data.get("contracts", [])),
        "total_files": 0,
        "mode": "unknown"
    }

    output_format = args.format or "md"
    report_path = report_mgr.generate_report(
        findings=findings,
        repo_data=repo_data,
        scan_metadata=scan_metadata,
        output_format=output_format,
    )
    console.print(f"[green]Report saved to:[/green] {report_path}")

def score_command(args):
    """Calculate and display security score from findings file."""
    logger = logging.getLogger(__name__)
    from hawki.core.data_layer.reporting.scoring_engine import SecurityScoreEngine

    input_path = args.input
    if not input_path:
        logger.error("No findings file specified.")
        sys.exit(1)

    try:
        with open(input_path, "r") as f:
            data = json.load(f)
    except Exception as e:
        logger.error(f"Failed to load findings file {input_path}: {e}")
        sys.exit(1)

    findings = data.get("findings", [])
    sandbox_results = data.get("sandbox_results")

    engine = SecurityScoreEngine()
    score_result = engine.calculate(
        findings=findings,
        sandbox_results=sandbox_results,
        ai_enabled=False,
    )

    # Display score in a nice table
    table = Table(title="Security Score", show_header=False)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="white")
    table.add_row("Score", f"{score_result['score']}/100")
    table.add_row("Classification", score_result['classification'])
    if args.verbose:
        for key, value in score_result['deductions'].items():
            table.add_row(key, str(value))
    console.print(table)

def metrics_command(args):
    """Display local telemetry stats."""
    store = MetricsStore()
    all_metrics = store.get_all()
    if not all_metrics:
        console.print("[yellow]No telemetry data recorded yet.[/yellow]")
        return

    total_scans = len(all_metrics)
    total_findings = sum(sum(m["findings"].values()) for m in all_metrics)
    critical = sum(m["findings"].get("Critical", 0) for m in all_metrics)
    high = sum(m["findings"].get("High", 0) for m in all_metrics)
    medium = sum(m["findings"].get("Medium", 0) for m in all_metrics)
    low = sum(m["findings"].get("Low", 0) for m in all_metrics)

    table = Table(title="Telemetry Summary")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="white")
    table.add_row("Total scans", str(total_scans))
    table.add_row("Total findings", str(total_findings))
    table.add_row("Critical", str(critical))
    table.add_row("High", str(high))
    table.add_row("Medium", str(medium))
    table.add_row("Low", str(low))
    console.print(table)

    if args.verbose:
        console.print("\n[bold]Detailed records:[/bold]")
        for m in all_metrics:
            console.print(f"  {m['timestamp']} - mode: {m['mode']}, findings: {m['findings']}")

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

    # Monitor command
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