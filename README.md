# 🦅 Hawk‑i

**Holistic Analysis for Web3 Kode & Infrastructure**

Hawk‑i is an open‑source smart contract security intelligence platform that combines static analysis, AI reasoning, and exploit simulation to detect vulnerabilities across your Solidity repositories. Designed for continuous auditing, it runs locally or in your CI/CD pipeline, preserving privacy while providing deep, actionable insights.

[![PyPI version](https://img.shields.io/pypi/v/hawki)](https://pypi.org/project/hawki/)
[![Docker Pulls](https://img.shields.io/docker/pulls/levichinecherem/hawki)](https://hub.docker.com/r/0xsemantic/hawki)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Contributors](https://img.shields.io/github/contributors/0xSemantic/hawki)](https://github.com/0xSemantic/hawki/graphs/contributors)
[![Discussions](https://img.shields.io/github/discussions/0xSemantic/hawki)](https://github.com/0xSemantic/hawki/discussions)

---

## 📖 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Advanced Usage](#-advanced-usage)
- [Troubleshooting](#-troubleshooting)
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

## 🔧 Troubleshooting

Here are solutions to common issues you might encounter while using Hawk‑i.

### `hawki: command not found` after pip install

**Problem:** The `hawki` command is not available in your terminal after installation.

**Solution:**  
- Ensure your `pip` is up‑to‑date:  
  ```bash
  pip install --upgrade pip
  ```
- Reinstall Hawk‑i with the `--force-reinstall` flag:  
  ```bash
  pip install --force-reinstall hawki
  ```
- If you're using a virtual environment, make sure it's activated (you should see `(venv)` in your prompt).  
- As a fallback, you can always run Hawk‑i using the module syntax:  
  ```bash
  python -m cli.hawki_cli scan ./demo
  ```

### Docker: Report files not saved on host

**Problem:** When running Hawk‑i in Docker, the report is generated but not visible on your host machine.

**Solution:**  
Mount a host directory to the container’s report location. By default, reports are saved to `/home/hawki/hawki_reports/` inside the container. Use the `-v` flag to bind‑mount a host directory:

```bash
docker run --rm \
  -v $(pwd)/demo:/repo \
  -v $(pwd)/hawki_reports:/home/hawki/hawki_reports \
  hawki:latest scan /repo
```

Now the report will appear in `./hawki_reports` on your host.

### Docker image build fails or cannot find image

**Problem:** The Docker image fails to build, or `hawki-sandbox:latest` is not found.

**Solution:**  
- Ensure Docker is installed and running (`docker info`).  
- Your user must have permission to run Docker. On Linux, you may need to add yourself to the `docker` group or use `sudo`.  
- If the image is missing, the sandbox will attempt to build it automatically. This may take a few minutes the first time. Let it complete without interrupting (Ctrl+C will abort the build).

### Web3.py middleware import errors

**Problem:** Errors like `cannot import name 'geth_poa_middleware' from 'web3.middleware'`.

**Solution:**  
This occurs because the import path for `geth_poa_middleware` changed in newer versions of web3.py. We've included a compatibility layer in Hawk‑i, but if you still encounter issues, try updating web3.py:

```bash
pip install --upgrade web3
```

If the problem persists, please open an issue on GitHub.

### AI analysis fails with "API key not valid"

**Problem:** When using `--ai`, you see an error about an invalid API key.

**Solution:**  
- Provide a valid API key via `--api-key`, environment variable, or `.env` file (see [AI Configuration](#ai-configuration)).  
- For Google Gemini, ensure you have enabled the Generative Language API in your Google Cloud console and that the key is correct.  
- LiteLLM expects the key to be set as `GEMINI_API_KEY`, `OPENAI_API_KEY`, or `ANTHROPIC_API_KEY` depending on the provider.

### `pkgutil` errors during rule discovery

**Problem:** Errors like `AttributeError: 'PosixPath' object has no attribute 'startswith'` when loading rules.

**Solution:**  
This was a bug in early versions and has been fixed. Update to the latest Hawk‑i:

```bash
pip install --upgrade hawki
```

### Monitor shows "Path is not a Git repository" repeatedly

**Problem:** The `repo_commit_watcher` logs a warning every few seconds because the target directory is not a Git repository.

**Solution:**  
This is normal – the watcher is designed to monitor Git repos. If you don't need commit monitoring, disable that watcher by removing it from your configuration, or simply ignore the messages. The warning is logged only once per check cycle, not continuously.

### Sandbox fails with "Image not found" but Docker is installed

**Problem:** The sandbox tries to build the image but fails with a "not found" error.

**Solution:**  
- Check that the Docker daemon is running: `systemctl status docker` (Linux) or check Docker Desktop (macOS/Windows).  
- Ensure your user has permission to access Docker. You can test with `docker run hello-world`.  
- If the build is interrupted (e.g., by Ctrl+C), remove any partially built images:  
  ```bash
  docker rmi hawki-sandbox:latest
  ```
  Then run the scan again – the image will be rebuilt.

### Report files are empty or missing findings

**Problem:** The scan completes but the JSON report contains no findings, even though you expect some.

**Solution:**  
- Check that your contracts are Solidity files (`.sol`) and are in the scanned directory.  
- If you're using the demo suite, ensure the Hardhat node is running and contracts are deployed.  
- Run without `--ai` and `--sandbox` first to verify static rules are working.  
- Increase logging verbosity with `--verbose` to see what Hawk‑i is doing.

### Still stuck?

If none of the above solves your problem, please [open an issue](https://github.com/0xSemantic/hawki/issues) with:
- The exact command you ran
- The full error output
- Your environment (OS, Python version, Hawk‑i version)

We'll help you get back on track!

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