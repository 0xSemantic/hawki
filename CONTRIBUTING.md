# Contributing to Hawk‑i

First off, thank you for considering contributing to Hawk‑i! 🎉 Your help is essential for making this project better, whether it’s fixing a bug, adding a new rule, improving documentation, or suggesting features.

We welcome contributions from everyone – seasoned Web3 developers, security researchers, or first‑time open‑source contributors. This guide will help you get started.

---

## 📜 Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md) (if available). Please be respectful, constructive, and considerate in all interactions.

---

## 🚀 Getting Started

### 1. Fork & Clone

1. Fork the repository on GitHub.
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/hawki.git
   cd hawki
   ```
3. Add the original repository as an upstream remote:
   ```bash
   git remote add upstream https://github.com/0xSemantic/hawki.git
   ```

### 2. Set Up Development Environment

Hawk‑i uses Python 3.9+ and relies on several dependencies. We recommend using a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -e .           # Install in editable mode
```

If you plan to run the demo contracts, you’ll also need Node.js and Hardhat:

```bash
cd demo
npm install
```

### 3. Run the Tests

Ensure everything is working by running the test suite:

```bash
pytest tests/
```

You should see all tests passing (or at least the ones that are not dependent on external APIs).

---

## 🧪 Development Workflow

We follow a simple GitHub flow:

1. **Create a branch** for your work:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. **Make your changes** – see the guidelines below.
3. **Write or update tests** to cover your changes.
4. **Run the tests** again to ensure they pass.
5. **Commit your changes** with a clear, descriptive message:
   ```
   feat(rule): add reentrancy guard detection
   fix(parser): handle nested contract declarations
   docs(readme): update installation instructions
   ```
   We use [Conventional Commits](https://www.conventionalcommits.org/) style.
6. **Push to your fork** and open a Pull Request against the `main` branch.

---

## 🧑‍💻 Coding Standards

### Python

- Follow [PEP 8](https://peps.python.org/pep-0008/) for code style.
- Use **type hints** for all function signatures.
- Write **docstrings** for modules, classes, and public methods (Google style preferred).
- Keep functions small and focused; follow the **Single Responsibility Principle**.
- Use **descriptive variable names**.

### Solidity (for demo contracts and attack scripts)

- Follow the [Solidity Style Guide](https://docs.soliditylang.org/en/latest/style-guide.html).
- Comment intentional vulnerabilities clearly (e.g., `// VULNERABILITY: ...`).

### Self‑Documenting Code

Every file must begin with a header comment describing its purpose, inputs, outputs, and dependencies. Example:

```python
# --------------------
# File: hawki/core/repo_intelligence/parser.py
# --------------------
"""
Solidity parser using tree‑sitter.
Extracts contracts, functions, state variables, modifiers, and inheritance.
Produces a structured representation for further analysis.
"""
```

### Dynamic Discovery

If you add a new module that should be auto‑discovered (e.g., a static rule, attack script, prompt template, or watcher), simply place it in the corresponding directory – the system will load it automatically. No need to register it manually.

- **Static rules**: `hawki/core/static_rule_engine/rules/`
- **Prompt templates**: `hawki/core/ai_engine/prompt_templates/`
- **Attack scripts**: `hawki/core/exploit_sandbox/attack_scripts/`
- **Watchers**: `hawki/core/monitoring/watchers/`

---

## 🧪 Testing

- All new features should include tests.
- Run the existing tests with:
  ```bash
  pytest tests/
  ```
- If you add a new rule, create a test in `tests/test_rules.py` or a dedicated file.
- Mock external services (like LLM calls) to avoid flaky tests.

---

## 🧩 Adding a New Static Rule

1. Create a new `.py` file in `hawki/core/static_rule_engine/rules/`.
2. Define a class that inherits from `BaseRule` (imported from the `rules` package).
3. Implement the `run_check(self, contract_data)` method. It should return a list of findings (dictionaries) with at least:
   - `"rule"`: short name (e.g., `"Reentrancy"`)
   - `"severity"`: `"HIGH"`, `"MEDIUM"`, `"LOW"`, or `"INFO"`
   - `"description"`: human‑readable explanation
   - `"location"`: string indicating where the issue was found (file/contract/function)
4. (Optional) Write a unit test in `tests/test_rules.py`.

Example:
```python
from . import BaseRule

class MyNewRule(BaseRule):
    def run_check(self, contract_data):
        findings = []
        # ... detection logic ...
        return findings
```

---

## 🤖 Adding a New Prompt Template

1. Create a `.json` file in `hawki/core/ai_engine/prompt_templates/`.
2. The JSON must contain `"system"` and `"user"` keys with string values.
3. Use placeholders like `{variable_name}`; they will be replaced at runtime.
4. Reference the template by its filename (without `.json`) in the code.

Example:
```json
{
  "system": "You are a Solidity expert...",
  "user": "Analyse this contract: {source_code}"
}
```

---

## 💣 Adding a New Attack Script

1. Create a `.py` file in `hawki/core/exploit_sandbox/attack_scripts/`.
2. The script will be executed inside the sandbox container. It should:
   - Connect to `http://localhost:8545` (the local blockchain).
   - Read deployed contract addresses from the environment variable `CONTRACT_ADDRESSES` (JSON dict).
   - Perform the exploit attempt.
   - Exit with code `0` if the exploit succeeded, non‑zero otherwise.
3. You can use `web3.py`; it is pre‑installed in the sandbox image.
4. Add a shebang (`#!/usr/bin/env python3`) and make the script executable if desired.

---

## 👁️ Adding a New Watcher

1. Create a `.py` file in `hawki/core/monitoring/watchers/`.
2. Define a class that inherits from `Watcher` (from `..watcher_base`).
3. Implement:
   - `__init__(self, name, config)`: call `super().__init__` and store any config.
   - `check(self)`: perform a single check. Return an event dictionary (with at least `"message"`) if something happened, else `None`.
   - Optionally override `load_state`/`save_state` if you need persistent state.
4. The watcher will be auto‑discovered and instantiated with config from the monitor’s configuration.

---

## 📚 Documentation

- Update the `README.md` if you change user‑facing functionality.
- For new features, add a section in the relevant part of the documentation.
- Keep docstrings up‑to‑date.

---

## 🐛 Reporting Bugs

- Use the [GitHub Issues](https://github.com/0xSemantic/hawki/issues) page.
- Search existing issues to avoid duplicates.
- Provide a clear title and description, steps to reproduce, expected vs. actual behaviour, and your environment (OS, Python version, Hawk‑i version).

---

## 💡 Suggesting Enhancements

- Open an issue with the label `enhancement`.
- Describe the feature, why it’s useful, and (if possible) a rough implementation idea.

---

## 🔄 Pull Request Process

1. Ensure your PR **describes the change** and links to any related issues.
2. Make sure all tests pass and the code is formatted.
3. Update documentation if needed.
4. The PR will be reviewed by maintainers. Be open to feedback and iterate.
5. Once approved, a maintainer will merge it.

---

## 🌍 Community

- Join the [Discussions](https://github.com/0xSemantic/hawki/discussions) for questions, ideas, and general chat.
- Follow [@0xSemantic](https://twitter.com/0xSemantic) on Twitter for updates.

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).

---

**Thank you for making Hawk‑i better!** 🦅