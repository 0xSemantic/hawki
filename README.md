# 🦅 Hawk‑i

**Holistic Analysis for Web3 Kode & Infrastructure**  
*Open‑source, privacy‑first security intelligence for smart contracts*

[![PyPI version](https://img.shields.io/pypi/v/hawki)](https://pypi.org/project/hawki/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/hawki)](https://pypi.org/project/hawki/)
[![PyPI - Downloads](https://img.shields.io/pypi/dw/hawki)](https://pypi.org/project/hawki/)
[![Docker Pulls](https://img.shields.io/docker/pulls/0xsemantic/hawki)](https://hub.docker.com/r/0xsemantic/hawki)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Contributors](https://img.shields.io/github/contributors/0xSemantic/hawki)](https://github.com/0xSemantic/hawki/graphs/contributors)
[![Discussions](https://img.shields.io/github/discussions/0xSemantic/hawki)](https://github.com/0xSemantic/hawki/discussions)

---

## 📖 Table of Contents

- [What is Hawk‑i?](#-what-is-hawk‑i)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Operational Modes](#-operational-modes)
- [Advanced Usage](#-advanced-usage)
  - [Audit‑Grade Reporting](#audit‑grade-reporting)
  - [Security Score](#security-score)
  - [Guided Remediation](#guided-remediation)
  - [Telemetry (Opt‑In)](#telemetry-opt‑in)
  - [CLI Reference](#cli-reference)
  - [CI/CD Integration](#cicd-integration)
  - [Ecosystem Integrations](#ecosystem-integrations)
- [Demo Suite](#-demo-suite)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgements](#-acknowledgements)
- [Roadmap](#-roadmap)
- [Contact](#-contact)

---

## 🦅 What is Hawk‑i?

Hawk‑i is an **open‑source security intelligence platform** for Web3 smart contracts. It evolves beyond a simple scanner into a complete audit‑grade system that **detects, simulates, scores, and helps fix vulnerabilities** – all while respecting your privacy.

Whether you're a solo developer, an auditor, or a protocol team, Hawk‑i integrates into your workflow to provide continuous, actionable security insights.

**Key differentiators:**
- **Hybrid analysis** – static rules + AI reasoning + live exploit simulation.
- **Professional reporting** – executive summaries, risk scores, charts, and per‑finding remediation.
- **Privacy by design** – runs locally; no code is ever sent to external servers (AI uses your own API keys).
- **Extensible** – drop‑in rules, attack scripts, and templates.

---

## ✨ Features

### Core Capabilities
- **🔍 Repository Intelligence** – Parse and index Solidity files from local folders or remote Git repos (GitHub, GitLab, etc.).
- **📦 Static Rule Engine** – Detect 30+ common vulnerabilities (reentrancy, access control, integer overflows, oracle manipulation, etc.) with an extensible rule system.
- **🧠 AI Reasoning** – Leverage LLMs (Gemini, OpenAI, Anthropic, local Ollama) to uncover logic flaws, economic exploits, and governance risks that static analysis misses.
- **💣 Exploit Simulation Sandbox** – Automatically deploy contracts in an isolated Docker environment and run attack scripts to validate vulnerabilities; results influence your risk score.
- **⏱️ Continuous Monitoring** – Watch repositories and deployed contracts for changes, and get alerts via file or console.

### v0.7.0 – Intelligence & Reporting Upgrade
- **📊 Audit‑Grade Reporting (ARS v2)** – Generate professional reports with executive summary, security score (0–100), severity charts, and per‑finding remediation.
- **🛡️ Guided Remediation Engine** – Every finding includes a context‑aware fix snippet, auto‑populated with your code’s variable names.
- **📈 Security Score** – A deterministic 0–100 score based on finding severity and exploit success, with clear risk bands.
- **📡 Telemetry (Opt‑In)** – Anonymous usage metrics to demonstrate ecosystem impact (no code, no repo names).
- **🧩 Expanded Vulnerability Library** – 30 fully documented vulnerabilities, each with detection, exploit script, and fix template.

---

## 🚀 Quick Start

### Installation

**Option 1: Install from PyPI (recommended)**
```bash
pip install hawki
```

**Option 2: Use Docker**
```bash
docker pull 0xsemantic/hawki:latest
docker run --rm -v $(pwd):/repo 0xsemantic/hawki scan /repo
```

**Option 3: Install from source**
```bash
git clone https://github.com/0xSemantic/hawki.git
cd hawki
pip install -e .
```

### Basic Scan
```bash
hawki scan /path/to/your/project
```
This runs static rules only (Minimal mode) and outputs a simple JSON report (legacy format). For the new audit‑grade report, use `--format`.

### Full Audit with AI + Sandbox
```bash
hawki scan /path --ai --ai-model openai/gpt-4 --api-key YOUR_KEY --sandbox --format pdf --telemetry
```
- `--ai` enables AI reasoning (requires an API key).
- `--sandbox` runs exploit simulations (requires Docker).
- `--format pdf` generates a professional PDF report.
- `--telemetry` opts in to anonymous usage stats.

### Generate a Report from Previous Scan
```bash
hawki report --input findings.json --format html --output report.html
```

### View Security Score
```bash
hawki score findings.json
```

### Show Local Telemetry
```bash
hawki metrics
```

### Monitor a Repository
```bash
hawki monitor /path/to/repo --interval 60 --alert-log alerts.txt
```

---

## ⚙️ Operational Modes

Hawk‑i adapts to your environment and privacy needs:

| Mode          | Static Rules | AI   | Sandbox | Docker Required |
|---------------|--------------|------|---------|-----------------|
| **Minimal**   | ✅           | ❌   | ❌      | ❌              |
| **Enhanced**  | ✅           | ✅   | ❌      | ❌              |
| **Full Audit**| ✅           | ✅   | ✅      | ✅              |

Reports indicate which mode was used and adapt content accordingly (e.g., omit exploit steps if sandbox disabled).

---

## 🔧 Advanced Usage

### Audit‑Grade Reporting

The `hawki scan` command with `--format` generates a report using the new **Audit‑Grade Report System (ARS v2)**. Reports include:

- **Executive Summary** – total contracts, severity counts, security score, risk classification, mode used.
- **Vulnerability Breakdown** – pie chart (severity) + bar chart (type) + fallback table.
- **Per‑Finding Details** – title, severity, file/line, vulnerable code, recommended fix, explanation, impact, exploit steps (if sandbox succeeded).
- **Simulation Metrics** – success rate, balance deltas, gas used.

Formats: Markdown (default), JSON, HTML, PDF (optional dependencies).

**Example Markdown snippet:**
```markdown
## 🔍 Detailed Findings
### F001: Reentrancy in withdraw() (CRITICAL)
- **File:** contracts/Vault.sol
- **Line:** 42

**Vulnerable Code:**
```solidity
function withdraw() external {
    uint bal = balances[msg.sender];
    (bool success,) = msg.sender.call{value: bal}("");
    require(success);
    balances[msg.sender] = 0;
}
```

**Recommended Fix:**
```solidity
function withdraw() external nonReentrant {
    uint bal = balances[msg.sender];
    balances[msg.sender] = 0;
    (bool success,) = msg.sender.call{value: bal}("");
    require(success);
}
```

**Explanation:** The function makes an external call before updating state, allowing reentrancy.
**Impact:** An attacker can drain all funds.
**Exploit Reproduction Steps:**
- Exploit succeeded using script: reentrancy_attack.py
- Before balance: 1000000000000000000
- After balance: 0
- Gas used: 120000
- Transaction hash: 0xabc...
```

### Security Score

The security score is a **deterministic 0–100** number computed as:

- Base: 100
- Deductions per finding:
  - Critical: -15
  - High: -8
  - Medium: -4
  - Low: -1
- If sandbox enabled: **-5** for each successfully reproduced exploit (capped).

**Risk Bands:**

| Score  | Classification |
|--------|----------------|
| 90–100 | Secure         |
| 75–89  | Minor Risk     |
| 50–74  | Moderate Risk  |
| 25–49  | High Risk      |
| 0–24   | Critical Risk  |

Use `hawki score findings.json` to see the score without generating a full report.

### Guided Remediation

Every finding now includes a `fix_snippet` populated by the **Remediation Engine**. The engine uses templates and AST context to generate accurate fixes. For example, a reentrancy finding might include:

```solidity
// Vulnerable code
function withdraw() external {
    uint amount = balances[msg.sender];
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success);
    balances[msg.sender] = 0;
}

// Recommended fix
function withdraw() external nonReentrant {
    uint amount = balances[msg.sender];
    balances[msg.sender] = 0;
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success);
}
```

### Telemetry (Opt‑In)

When you run `hawki scan --telemetry`, Hawk‑i collects **anonymous** data:

- Total scans performed
- Findings per severity
- Simulation success rate (if sandbox enabled)
- Hawk‑i version
- Execution mode

Data is stored locally in `~/.hawki/metrics.json` and can be viewed with `hawki metrics`. If you opt in, aggregated statistics may be sent to a public endpoint to power the community metrics badge. **No source code, repository names, or IPs are ever collected.**

**View your metrics:**
```bash
hawki metrics
```

**Example output:**
```
Total scans: 42
Total findings: 87 (Critical: 12, High: 23, Medium: 31, Low: 21)
```

### CLI Reference

The main command is `hawki`. Available subcommands:

| Subcommand | Description |
|------------|-------------|
| `scan`     | Perform a one‑time security scan. |
| `monitor`  | Continuously monitor a repository or contract. |
| `report`   | Generate a report from existing findings. |
| `score`    | Calculate the security score from a findings file. |
| `metrics`  | Display local telemetry statistics. |
| `simulate` | Run a specific exploit simulation (advanced). |

**`hawki scan` options:**
```
hawki scan <target> [options]
  -v, --verbose               Enable debug logging
  -o, --output-dir DIR         Report output directory (default: ./hawki_reports)
  --ai                         Enable AI reasoning
  --ai-model MODEL              LLM model (e.g., openai/gpt-4)
  --api-key KEY                 API key for LLM
  --sandbox                     Run exploit simulation (requires Docker)
  --format {md,json,html,pdf}   Output report format (if omitted, legacy JSON)
  --telemetry                   Opt in to anonymous usage metrics
```

**`hawki report` options:**
```
hawki report [options]
  -i, --input FILE    Findings JSON file (default: latest)
  -o, --output-dir DIR Output directory
  -f, --format FORMAT  Output format (md, json, html, pdf)
```

**`hawki score`**:
```
hawki score findings.json [-v]
```

**`hawki metrics`**:
```
hawki metrics [-v]
```

### CI/CD Integration

Hawk‑i provides a dedicated script `scripts/ci_pipeline.py` that auto‑detects GitHub Actions or GitLab CI and formats output accordingly.

**GitHub Actions example (`.github/workflows/hawki.yml`):**
```yaml
name: Hawk-i Security Scan
on: [push, pull_request]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install Hawk-i
        run: pip install hawki
      - name: Run Hawk-i CI
        run: python scripts/ci_pipeline.py .
```

The script exits with code `1` if any **HIGH** severity findings are detected, allowing you to fail the pipeline.

**GitLab CI example (`.gitlab-ci.yml`):**
```yaml
hawki-scan:
  image: python:3.11
  before_script:
    - pip install hawki
  script:
    - python scripts/ci_pipeline.py .
  artifacts:
    reports:
      codequality: gl-code-quality-report.json
```

### Ecosystem Integrations

Use the helper script `scripts/deploy_helpers.py` to integrate with popular development tools.

#### Foundry
```bash
python scripts/deploy_helpers.py foundry /path/to/forge-project --ai
```

#### Hardhat
```bash
python scripts/deploy_helpers.py hardhat /path/to/hardhat-project
```

#### Remix
```bash
python scripts/deploy_helpers.py remix /path/to/remix-workspace
```

#### Generate a human‑readable audit report
```bash
python scripts/deploy_helpers.py readme /path/to/report.json --output AUDIT.md
```

---

## 🧪 Demo Suite

We’ve built a **dedicated demo suite** of intentionally vulnerable contracts to help you understand Hawk‑i’s capabilities and to test your contributions.

The suite includes **30 vulnerable contracts**, one for each rule, covering:
- Reentrancy
- Access control bypass
- Delegatecall misuse
- Oracle manipulation
- Flash loan attacks
- Governance vote manipulation
- Signature replay
- Integer overflows
- And more…

### Quick Demo (with Docker)

```bash
docker build -f demo/Dockerfile.demo -t hawki-demo .
docker run --rm hawki-demo
```

### Manual Demo

```bash
cd demo
npm install           # install Hardhat dependencies
npx hardhat node      # start local blockchain (keep open)
# In another terminal:
npx hardhat run scripts/deploy.js --network localhost
hawki scan . --ai --sandbox --format html --telemetry
```

See the [demo README](demo/README.md) for detailed instructions and expected output.

---

## 📁 Project Structure

```
hawki/
├── core/
│   ├── repo_intelligence/          # Repo cloning & Solidity parsing
│   ├── static_rule_engine/         # Static analysis & dynamic rule loading (30+ rules)
│   ├── ai_engine/                   # LLM orchestration & prompt management
│   ├── exploit_sandbox/             # Docker‑based exploit simulation
│   ├── remediation_engine/          # Context‑aware fix snippet generation
│   ├── telemetry/                    # Opt‑in anonymous metrics
│   ├── monitoring/                   # Continuous monitoring & alerts
│   └── data_layer/                   # Report generation (ARS v2) & persistence
├── cli/                              # Command‑line interface
├── scripts/                          # CI/CD and integration helpers
├── docker/                           # Dockerfile and compose
├── demo/                             # Vulnerable contracts for testing
├── tests/                            # Unit tests
├── pyproject.toml                    # Package metadata
├── CONTRIBUTING.md                    # Contribution guidelines
├── CONTRIBUTORS.md                    # List of contributors
└── README.md                          # This file
```

---

## 🤝 Contributing

We welcome contributions from the community! Whether you're fixing a bug, adding a new rule, or improving documentation, your help makes Hawk‑i better for everyone.

Please read our [Contributing Guidelines](CONTRIBUTING.md) to get started. All contributors are recognised in [CONTRIBUTORS.md](CONTRIBUTORS.md) – we use the [All Contributors](https://allcontributors.org/) specification.

---

## 📄 License

Hawk‑i is released under the [MIT License](LICENSE).

---

## 🙏 Acknowledgements

Hawk‑i builds upon excellent open‑source projects:

- [tree‑sitter](https://tree-sitter.github.io/) and [tree‑sitter‑solidity](https://github.com/tree-sitter/tree-sitter-solidity) for parsing.
- [LiteLLM](https://github.com/BerriAI/litellm) for unified LLM access.
- [Docker](https://www.docker.com/) for sandboxing.
- [Web3.py](https://web3py.readthedocs.io/) for blockchain interaction.
- [GitPython](https://gitpython.readthedocs.io/) for repository handling.
- [matplotlib](https://matplotlib.org/) for chart generation (optional).
- [Jinja2](https://jinja.palletsprojects.com/) for templated reports.

Special thanks to all contributors and the Web3 security community.

---

## 🛣️ Roadmap

- [x] **Phase 1** – Repository intelligence + static rule engine
- [x] **Phase 2** – AI reasoning with LiteLLM
- [x] **Phase 3** – Exploit simulation sandbox
- [x] **Phase 4** – Continuous monitoring & alerts
- [x] **Phase 5** – CI/CD & ecosystem integrations
- [x] **Phase 6** – Deployment (PyPI, Docker, CLI)
- [x] **Phase 7 – v0.7.0 Intelligence & Reporting Upgrade**
  - Audit‑grade reporting (ARS v2)
  - 30 vulnerability rules
  - Security score
  - Guided remediation engine
  - Opt‑in telemetry
- [ ] **Phase 8** – Dashboard & real‑time visualisation
- [ ] **Phase 9** – Intelligence network & community rules marketplace

---

## 📬 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/0xSemantic/hawki/issues)
- **Discussions**: [GitHub Discussions](https://github.com/0xSemantic/hawki/discussions)
- **LinkedIn**: [0xSemantic](https://linkedin.com/in/0xsemantic)
- **Medium**: [@0xSemantic](https://medium.com/@0xsemantic)
- **Twitter**: [@0xSemantic](https://twitter.com/0xSemantic)

**Happy auditing, and may your contracts be bug‑free!** 🦅