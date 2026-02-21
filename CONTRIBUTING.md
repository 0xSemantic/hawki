# Contributing to Hawk‑i

First off, thank you for considering contributing to Hawk‑i! 🎉 Your help is essential for making this project better, whether it’s fixing a bug, adding a new rule, improving documentation, or suggesting features.

We welcome contributions from everyone – seasoned Web3 developers, security researchers, or first‑time open‑source contributors. This guide will help you get started.

---

## 📜 Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please be respectful, constructive, and considerate in all interactions.

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

If you plan to run the demo contracts or exploit sandbox, you’ll also need Node.js and Hardhat:

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
5. **Commit your changes** with a clear, descriptive message using [Conventional Commits](https://www.conventionalcommits.org/):
   ```
   feat(rule): add reentrancy guard detection
   fix(parser): handle nested contract declarations
   docs(readme): update installation instructions
   ```
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
- Comment intentional vulnerabilities clearly (e.g., `// VULNERABILITY: reentrancy`).

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

If you add a new module that should be auto‑discovered, simply place it in the corresponding directory – the system will load it automatically. No manual registration needed.

| Component               | Directory                                                |
|-------------------------|----------------------------------------------------------|
| Static rules            | `hawki/core/static_rule_engine/rules/`                   |
| Prompt templates        | `hawki/core/ai_engine/prompt_templates/`                 |
| Attack scripts          | `hawki/core/exploit_sandbox/attack_scripts/`             |
| Watchers                | `hawki/core/monitoring/watchers/`                        |
| Remediation templates   | `hawki/core/remediation_engine/templates/`               |
| Report templates        | `hawki/core/data_layer/reporting/templates/`             |

---

## 🧪 Testing

- All new features should include tests.
- Run the existing tests with:
  ```bash
  pytest tests/
  ```
- If you add a new rule, create a test in `tests/test_rules.py` or a dedicated file.
- Mock external services (like LLM calls) to avoid flaky tests.
- Aim for at least 85% test coverage overall.

---

## 🧩 Adding a New Static Rule

As of v0.7.0, every rule must provide not only detection logic but also explanation, impact, and fix templates. This ensures reports are complete even when AI is disabled.

1. Create a new `.py` file in `hawki/core/static_rule_engine/rules/`.
2. Define a class that inherits from `BaseRule` (imported from the `rules` package).
3. **Required class attributes**:
   - `severity` – one of `"Critical"`, `"High"`, `"Medium"`, `"Low"`.
   - `explanation_template` – a string describing why the issue is dangerous.
   - `impact_template` – a string describing potential consequences (fund loss, DoS, etc.).
   - `fix_template` – a string with placeholders (e.g., `{{function}}`) for the remediation engine.
4. Implement the `run_check(self, contract_data)` method. It should return a list of findings (dictionaries). Each finding must include at least:
   - `"title"`: short description
   - `"severity"`: same as class attribute (or override per finding)
   - `"file"`: relative path
   - `"line"`: line number
   - `"vulnerable_snippet"`: the exact code lines
   - (The `explanation`, `impact`, and `fix_snippet` fields will be populated automatically from the class attributes/remediation engine.)
5. Write a unit test in `tests/test_rules.py` that verifies detection on a purposely vulnerable contract.

Example skeleton:

```python
# --------------------
# File: hawki/core/static_rule_engine/rules/reentrancy.py
# --------------------
from . import BaseRule

class ReentrancyRule(BaseRule):
    severity = "Critical"
    explanation_template = "This function allows reentrant calls because it updates state after an external call."
    impact_template = "An attacker can drain funds by recursively calling back before state updates."
    fix_template = "Apply the checks‑effects‑interactions pattern and add a nonReentrant modifier."

    def run_check(self, contract_data):
        findings = []
        # ... detection logic ...
        for match in detected:
            findings.append({
                "title": "Reentrancy in withdraw()",
                "severity": self.severity,
                "file": match.file,
                "line": match.line,
                "vulnerable_snippet": match.code,
            })
        return findings
```

---

## 💣 Adding a New Attack Script

Attack scripts are used by the exploit sandbox to simulate vulnerabilities. In v0.7.0, they must return structured data to be included in reports and influence the security score.

1. Create a `.py` file in `hawki/core/exploit_sandbox/attack_scripts/`.
2. The script will be executed inside a Docker container with:
   - A local Ethereum testnet (Anvil/Ganache) at `http://localhost:8545`.
   - The vulnerable contract(s) already deployed.
   - Environment variable `CONTRACT_ADDRESSES` containing a JSON dict of contract names to addresses.
3. The script must output a JSON object (to stdout) with the following fields:
   ```python
   {
       "success": bool,
       "before_balance": int,      # e.g., attacker balance before
       "after_balance": int,       # after exploit
       "gas_used": int,
       "transaction_hash": str,    # optional
       "logs": str                  # optional, human‑readable details
   }
   ```
4. Exit with code 0 on success (exploit worked) or non‑zero on failure (exploit failed or script error).

You can use `web3.py` (pre‑installed in the sandbox image). Example skeleton:

```python
#!/usr/bin/env python3
import os, json, sys
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
contract_addresses = json.loads(os.environ["CONTRACT_ADDRESSES"])
vault = w3.eth.contract(address=contract_addresses["Vault"], abi=...)

attacker = w3.eth.accounts[1]
before = w3.eth.get_balance(attacker)

# perform exploit...
tx_hash = vault.functions.attack().transact({'from': attacker})
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

after = w3.eth.get_balance(attacker)

result = {
    "success": True,
    "before_balance": before,
    "after_balance": after,
    "gas_used": receipt.gasUsed,
    "transaction_hash": tx_hash.hex(),
    "logs": "Exploit succeeded"
}
print(json.dumps(result))
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

## 🛠️ Adding a New Remediation Template

Remediation templates provide context‑aware fix snippets for vulnerabilities. They are JSON files placed in `hawki/core/remediation_engine/templates/`, named after the vulnerability (e.g., `reentrancy.json`).

1. Create a `.json` file with the following structure:
   ```json
   {
       "fix_snippet": "function {{function_name}}() {{visibility}} {\n    // Checks‑Effects‑Interactions\n    require({{condition}});\n    {{state_updates}}\n    (bool success, ) = {{external_call}}.call{value: {{amount}}}(\"\");\n    require(success);\n}"
   }
   ```
2. Use double curly braces `{{placeholder}}` for variables that will be replaced by the remediation engine (using AST context).
3. The filename should match the rule’s identifier (e.g., rule class name) or a common vulnerability name.

---

## 📄 Adding a New Report Template

Report templates control the layout of generated reports. They are stored in `hawki/core/data_layer/reporting/templates/` and can be Markdown, HTML, or JSON.

1. Create a new template file (e.g., `custom_report.md`).
2. Use placeholders like `{{executive_summary}}`, `{{findings_table}}`, etc. Refer to existing templates for available variables.
3. To make the new format available, you may need to extend `ReportGeneratorV2` to handle it. For now, stick to the existing formats unless you’re willing to update the generator.

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
- For new features, add a section in the relevant part of the documentation (e.g., `docs/`).
- Keep docstrings up‑to‑date.
- If you add a new rule, mention it in the list of supported vulnerabilities (e.g., in the docs or a separate file).

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