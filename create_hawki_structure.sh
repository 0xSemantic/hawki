#!/bin/bash
# --------------------
# File: create_hawki_structure.sh
# --------------------
# This script creates the full directory structure and empty files
# for the Hawk-i project as defined in the roadmap (Phases 1-6).
# Run this script in the directory where you want the Hawk-i root.
# It creates all necessary folders and placeholder files.

set -e  # Exit on error

echo "Creating Hawk-i project structure..."

# Create root directories
mkdir -p hawki/core/repo_intelligence
mkdir -p hawki/core/static_rule_engine/rules
mkdir -p hawki/core/ai_engine/prompt_templates
mkdir -p hawki/core/exploit_sandbox/attack_scripts
mkdir -p hawki/core/monitoring/watchers
mkdir -p hawki/core/data_layer
mkdir -p cli
mkdir -p tests/ai
mkdir -p tests/sandbox
mkdir -p tests/monitoring
mkdir -p scripts
mkdir -p docker

# Create __init__.py files for Python packages
touch hawki/__init__.py
touch hawki/core/__init__.py
touch hawki/core/repo_intelligence/__init__.py
touch hawki/core/static_rule_engine/__init__.py
touch hawki/core/static_rule_engine/rules/__init__.py
touch hawki/core/ai_engine/__init__.py
touch hawki/core/exploit_sandbox/__init__.py
touch hawki/core/exploit_sandbox/attack_scripts/__init__.py
touch hawki/core/monitoring/__init__.py
touch hawki/core/monitoring/watchers/__init__.py
touch hawki/core/data_layer/__init__.py
touch cli/__init__.py
touch tests/__init__.py

# Create repository intelligence files
touch hawki/core/repo_intelligence/parser.py
touch hawki/core/repo_intelligence/indexer.py

# Create static rule engine files (10 rules)
touch hawki/core/static_rule_engine/rules/reentrancy.py
touch hawki/core/static_rule_engine/rules/access_control.py
touch hawki/core/static_rule_engine/rules/integer_overflow.py
touch hawki/core/static_rule_engine/rules/unchecked_send.py
touch hawki/core/static_rule_engine/rules/tx_origin_dependency.py
touch hawki/core/static_rule_engine/rules/uninitialized_storage.py
touch hawki/core/static_rule_engine/rules/delegatecall_misuse.py
touch hawki/core/static_rule_engine/rules/front_running.py
touch hawki/core/static_rule_engine/rules/timestamp_dependency.py
touch hawki/core/static_rule_engine/rules/gas_limit_vulnerability.py

# Create AI engine files
touch hawki/core/ai_engine/lite_llm_adapter.py
touch hawki/core/ai_engine/prompt_manager.py
touch hawki/core/ai_engine/llm_orchestrator.py
touch hawki/core/ai_engine/reasoning_agent.py
touch hawki/core/ai_engine/prompt_templates/vuln_analysis_prompt.json
touch hawki/core/ai_engine/prompt_templates/risk_scoring_prompt.json
touch hawki/core/ai_engine/prompt_templates/general_contract_prompt.json

# Create exploit sandbox files
touch hawki/core/exploit_sandbox/sandbox_manager.py
touch hawki/core/exploit_sandbox/docker_config.py
touch hawki/core/exploit_sandbox/attack_scripts/reentrancy_test.py
touch hawki/core/exploit_sandbox/attack_scripts/access_control_test.py
touch hawki/core/exploit_sandbox/deploy.py

# Create monitoring files
touch hawki/core/monitoring/watcher_base.py
touch hawki/core/monitoring/alert_manager.py
touch hawki/core/monitoring/state_manager.py
touch hawki/core/monitoring/watchers/repo_commit_watcher.py
touch hawki/core/monitoring/watchers/deployed_contract_watcher.py
touch hawki/core/monitoring/watchers/ci_cd_watcher.py
touch hawki/core/monitoring/watchers/vulnerability_event_watcher.py

# Create data layer files
touch hawki/core/data_layer/report_manager.py

# Create CLI files
touch cli/hawki_cli.py

# Create test files
touch tests/test_parser.py
touch tests/test_rules.py
touch tests/ai/test_prompt_manager.py
touch tests/ai/test_reasoning_agent.py
touch tests/sandbox/test_sandbox_manager.py
touch tests/monitoring/test_watcher_base.py
touch tests/monitoring/test_state_manager.py
touch tests/monitoring/test_alert_manager.py

# Create script files
touch scripts/ci_pipeline.py
touch scripts/deploy_helpers.py
touch scripts/build_pypi.sh

# Create Docker files
touch docker/Dockerfile
touch docker/docker-compose.yml

# Create root-level files
touch pyproject.toml
touch requirements.txt
touch README.md
touch MANIFEST.in
touch LICENSE

echo "Hawk-i project structure created successfully."
echo "You can now populate the files with the code from the phases."