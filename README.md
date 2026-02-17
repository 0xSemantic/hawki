# 🦅 Hawk‑i

**Holistic Analysis for Web3 Kode & Infrastructure**

Hawk‑i is an open‑source smart contract security intelligence platform that combines static analysis, AI reasoning, and exploit simulation to detect vulnerabilities across your Solidity repositories. Designed for continuous auditing, it runs locally or in your CI/CD pipeline, preserving privacy while providing deep, actionable insights.

[![PyPI version](https://img.shields.io/pypi/v/hawki)](https://pypi.org/project/hawki/)
[![Docker Pulls](https://img.shields.io/docker/pulls/0xsemantic/hawki)](https://hub.docker.com/r/0xsemantic/hawki)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Contributors](https://img.shields.io/github/contributors/0xSemantic/hawki)](https://github.com/0xSemantic/hawki/graphs/contributors)
[![Discussions](https://img.shields.io/github/discussions/0xSemantic/hawki)](https://github.com/0xSemantic/hawki/discussions)

---

## 📖 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Advanced Usage](#-advanced-usage)
- [Demo Suite](#-demo-suite)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgements](#-acknowledgements)
- [Roadmap](#-roadmap)
- [Contact](#-contact)

---

## ✨ Features

- **🔍 Repository Intelligence** – Parse and index Solidity files from local folders or remote Git repos (GitHub, GitLab, etc.).
- **📦 Static Rule Engine** – Detect 10+ common vulnerabilities (reentrancy, access control, integer overflows, etc.) with an extensible rule system.
- **🧠 AI Reasoning** – Leverage LLMs (Gemini, OpenAI, Anthropic) to uncover logic flaws, economic exploits, and governance risks that static analysis misses.
- **💣 Exploit Simulation Sandbox** – Automatically deploy contracts in an isolated Docker environment and run attack scripts to validate vulnerabilities.
- **⏱️ Continuous Monitoring** – Watch repositories and deployed contracts for changes, and get alerts via file or console.
- **🔌 CI/CD Integration** – Plug into GitHub Actions or GitLab CI to fail builds on high‑severity issues.
- **🛠️ Ecosystem Friendly** – Works with Foundry, Hardhat, and Remix projects out of the box.
- **🔒 Privacy First** – Runs entirely on your machine; no code is sent to external servers unless you enable AI with your own API keys.

---

## 🚀 Quick Start

### Installation

#### Option 1: Install from PyPI (recommended)

```bash
pip install hawki
```

#### Option 2: Use Docker

```bash
docker pull 0xsemantic/hawki:latest
docker run --rm -v $(pwd):/repo hawki scan /repo
```

#### Option 3: Install from source

```bash
git clone https://github.com/0xSemantic/hawki.git
cd hawki
pip install -e .
```

### Basic Usage

Scan a local repository:

```bash
hawki scan /path/to/your/project
```

Scan a remote GitHub repository:

```bash
hawki scan https://github.com/owner/repo.git
```

Enable AI analysis (you need an API key):

```bash
hawki scan /path --ai --ai-model gemini/gemini-1.5-flash --api-key YOUR_KEY
```

Run exploit simulation:

```bash
hawki scan /path --sandbox
```

Monitor a repository for new commits:

```bash
hawki monitor /path/to/repo --interval 60 --alert-log alerts.jsonl
```

Monitor a deployed contract:

```bash
hawki monitor --contract-address 0x123... --rpc-url https://mainnet.infura.io/v3/...
```

---

## 🔧 Advanced Usage

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

The script exits with code `1` if any **HIGH** severity findings are detected, allowing you to fail the pipeline.

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

### AI Configuration

Hawk‑i uses [LiteLLM](https://docs.litellm.ai/) to support multiple LLM providers. You can set your API key in three ways (listed in order of precedence):

1. **Command‑line argument** `--api-key` – takes highest priority.
2. **Environment variable** – set the corresponding variable for your provider (see table below).
3. **`.env` file** – if you prefer to keep keys in a file, you can load it manually (see instructions).

| Provider   | Model example                     | Environment variable |
|------------|-----------------------------------|----------------------|
| Google Gemini | `gemini/gemini-1.5-flash`       | `GEMINI_API_KEY`     |
| OpenAI        | `openai/gpt-4`                   | `OPENAI_API_KEY`     |
| Anthropic     | `anthropic/claude-3-haiku-20240307` | `ANTHROPIC_API_KEY` |

#### Persistent API Key Setup

- **Using environment variables (recommended)**  
  Add the export line to your shell profile (`~/.bashrc`, `~/.zshrc`, or `~/.profile`):
  ```bash
  export GEMINI_API_KEY="your-key"
  ```
  Then reload: `source ~/.bashrc`. After this, you can run `hawki scan --ai` without the `--api-key` flag.

- **Using a `.env` file**  
  Hawk‑i does not load `.env` automatically, but you can use `python-dotenv` to load it before running:
  ```bash
  pip install python-dotenv
  echo "GEMINI_API_KEY=your-key" > .env
  python -c "from dotenv import load_dotenv; load_dotenv()" && hawki scan . --ai
  ```
  For convenience, you can create a small wrapper script that loads the `.env` file.

### Adding Custom Rules, Prompts, or Attack Scripts

All dynamic components are auto‑discovered – just drop a file in the corresponding directory.

- **Static rules**: `hawki/core/static_rule_engine/rules/` (Python classes inheriting from `BaseRule`)
- **Prompt templates**: `hawki/core/ai_engine/prompt_templates/` (JSON files with `system` and `user` fields)
- **Attack scripts**: `hawki/core/exploit_sandbox/attack_scripts/` (Python scripts that use `web3.py` and exit with code `0` on success)
- **Watchers**: `hawki/core/monitoring/watchers/` (Python classes inheriting from `Watcher`)

---

## 🧪 Demo Suite

To help you understand Hawk‑i’s capabilities and to test your own contributions, we’ve built a **dedicated demo suite** of intentionally vulnerable contracts. The suite includes:

- `VulnerableToken.sol` – integer overflow & unchecked send
- `ReentrancyDemo.sol` – classic reentrancy bug
- `AccessControlTest.sol` – missing access control
- `DelegateCallExample.sol` – unsafe delegatecall
- `MysteryLogic.sol` – subtle rounding error (AI‑only detection)

### Run the Demo

```bash
cd demo
npm install           # install Hardhat dependencies
npx hardhat node      # start local blockchain (keep open)
# In another terminal:
npx hardhat run scripts/deploy.js --network localhost
hawki scan . --ai --sandbox
```

For a fully containerized demo (no local setup required):

```bash
docker build -f demo/Dockerfile.demo -t hawki-demo .
docker run --rm hawki-demo
```

See the [demo README](demo/README.md) for detailed instructions and expected output.

---

## 📁 Project Structure

```
hawki/
├── core/
│   ├── repo_intelligence/      # Repo cloning & Solidity parsing
│   ├── static_rule_engine/     # Static analysis & dynamic rule loading
│   ├── ai_engine/               # LLM orchestration & prompt management
│   ├── exploit_sandbox/         # Docker‑based exploit simulation
│   ├── monitoring/              # Continuous monitoring & alerts
│   └── data_layer/              # Report generation & persistence
├── cli/                          # Command‑line interface
├── scripts/                      # CI/CD and integration helpers
├── docker/                       # Dockerfile and compose
├── demo/                         # Vulnerable contracts for testing
├── tests/                         # Unit tests
├── pyproject.toml                 # Package metadata
├── CONTRIBUTING.md                # Contribution guidelines
├── CONTRIBUTORS.md                # List of contributors
└── README.md                      # This file
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

Special thanks to all contributors and the Web3 security community.

---

## 🛣️ Roadmap

- [x] **Phase 1** – Repository intelligence + static rule engine
- [x] **Phase 2** – AI reasoning with LiteLLM
- [x] **Phase 3** – Exploit simulation sandbox
- [x] **Phase 4** – Continuous monitoring & alerts
- [x] **Phase 5** – CI/CD & ecosystem integrations
- [x] **Phase 6** – Deployment (PyPI, Docker, CLI)
- [ ] **Phase 7** – Dashboard & real‑time visualisation
- [ ] **Phase 8** – Intelligence network & community rules

---

## 📬 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/0xSemantic/hawki/issues)
- **Discussions**: [GitHub Discussions](https://github.com/0xSemantic/hawki/discussions)
- **LinkedIn**: [0xSemantic](https://linkedin.com/in/0xsemantic)
- **Medium**: [@0xSemantic](https://medium.com/@0xsemantic)
- **Twitter**: [@0xSemantic](https://twitter.com/0xSemantic)

**Happy auditing, and may your contracts be bug‑free!** 🦅