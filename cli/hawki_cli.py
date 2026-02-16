# --------------------
# File: cli/hawki_cli.py (updated for Phase 4)
# --------------------
"""
Hawk-i command‑line interface – Phase 4 with monitoring.
"""

import argparse
import logging
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from hawki.core.repo_intelligence.indexer import RepositoryIndexer
from hawki.core.static_rule_engine import RuleEngine
from hawki.core.ai_engine.reasoning_agent import ReasoningAgent
from hawki.core.exploit_sandbox.sandbox_manager import SandboxManager
from hawki.core.data_layer.report_manager import ReportManager
from hawki.core.monitoring import Monitor

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

    try:
        logger.info(f"Scanning target: {args.target}")
        repo_data = indexer.index(args.target)

        logger.info(f"Running {len(engine.rules)} static rules...")
        static_findings = engine.run_all(repo_data["contracts"])

        ai_findings = []
        if ai_agent:
            logger.info("Running AI reasoning...")
            ai_findings = ai_agent.analyse_contracts(repo_data["contracts"])
            logger.info(f"AI found {len(ai_findings)} potential issues")

        all_findings = static_findings + ai_findings

        sandbox_results = []
        if args.sandbox:
            logger.info("Starting exploit simulation sandbox...")
            repo_path = Path(repo_data["path"]) if repo_data["type"] == "remote" else Path(repo_data["path"])
            sandbox = SandboxManager(repo_path)
            sandbox_results = sandbox.run_all()
            logger.info(f"Sandbox completed with {len(sandbox_results)} attack script results")
            repo_data["sandbox_results"] = sandbox_results

        report_path = report_mgr.save_findings(all_findings, repo_data)
        logger.info(f"Scan complete. Total findings: {len(all_findings)}")
        print(f"\nReport saved to: {report_path}")

    except Exception as e:
        logger.error(f"Scan failed: {e}", exc_info=True)
        sys.exit(1)
    finally:
        indexer.cleanup()

def monitor_command(args):
    """Handle 'monitor' subcommand."""
    logger = logging.getLogger(__name__)
    # Build watcher configs from arguments or config file
    config = {}
    if args.config:
        with open(args.config, 'r') as f:
            config = json.load(f)
    else:
        # If no config, we can create a simple default based on target
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
    monitor.run_forever(interval_seconds=interval)

def main():
    parser = argparse.ArgumentParser(description="Hawk-i Security Scanner")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Subcommands")

    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Perform a one-time scan")
    scan_parser.add_argument("target", help="Local directory path or Git repository URL")
    scan_parser.add_argument("-v", "--verbose", action="store_true", help="Enable debug logging")
    scan_parser.add_argument("-o", "--output-dir", type=Path, help="Directory to store reports (default: ./hawki_reports)")
    scan_parser.add_argument("--ai", action="store_true", help="Enable AI‑powered analysis")
    scan_parser.add_argument("--ai-model", help="LLM model (e.g., gemini/gemini-1.5-flash, openai/gpt-4)")
    scan_parser.add_argument("--api-key", help="API key for the chosen LLM (or set env var)")
    scan_parser.add_argument("--sandbox", action="store_true", help="Run exploit simulation sandbox")
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

    args = parser.parse_args()
    setup_logging(args.verbose)
    args.func(args)

if __name__ == "__main__":
    main()

# EOF: cli/hawki_cli.py