# Hawk‑i Demo Suite: Intentionally Vulnerable Contracts

Welcome to the **Hawk‑i Demo Suite** – a comprehensive collection of Solidity smart contracts deliberately crafted with security flaws. This suite is designed to **test, demonstrate, and validate** every feature of Hawk‑i, especially the powerful new capabilities introduced in **v0.7.0**:

- 🔍 **Static Rule Engine** – Detects known vulnerability patterns (now expanded to **30+ rules**).
- 🧠 **AI Reasoning** – Uncovers subtle, logic‑based, or novel issues using LLMs (Gemini, OpenAI, Anthropic, local Ollama).
- 💣 **Exploit Simulation Sandbox** – Automatically attempts to exploit identified weaknesses, returning detailed metrics that influence the security score.
- 📊 **Audit‑Grade Reporting (ARS v2)** – Generates professional reports with executive summary, security score (0–100), vulnerability charts, and per‑finding remediation snippets.
- 🛡️ **Guided Remediation Engine** – Every finding includes a context‑aware fix snippet, auto‑populated with your code’s variable names.
- 📡 **Telemetry (Opt‑In)** – Anonymous usage metrics to measure ecosystem impact.

Whether you are a developer evaluating Hawk‑i, a security researcher honing your skills, an auditor preparing for a real engagement, or a grant reviewer verifying the tool’s capabilities, this demo provides a **repeatable, self‑contained, and deeply educational environment** to see Hawk‑i in action.

---

## 📚 Table of Contents

- [What’s New in v0.7.0?](#-whats-new-in-v070)
- [Demo Suite Overview](#-demo-suite-overview)
- [Prerequisites](#-prerequisites)
- [Quick Start (TL;DR)](#-quick-start-tldr)
- [Detailed Walkthrough](#-detailed-walkthrough)
  - [Step 1: Set Up the Environment](#step-1-set-up-the-environment)
  - [Step 2: Deploy the Contracts](#step-2-deploy-the-contracts)
  - [Step 3: Run a Minimal Scan (Static Rules Only)](#step-3-run-a-minimal-scan-static-rules-only)
  - [Step 4: Run an Enhanced Scan (with AI)](#step-4-run-an-enhanced-scan-with-ai)
  - [Step 5: Run a Full Audit (AI + Sandbox)](#step-5-run-a-full-audit-ai--sandbox)
  - [Step 6: Generate Professional Reports](#step-6-generate-professional-reports)
  - [Step 7: Understand the Security Score](#step-7-understand-the-security-score)
  - [Step 8: Explore Guided Remediation](#step-8-explore-guided-remediation)
  - [Step 9: Opt‑In Telemetry and View Metrics](#step-9-opt-in-telemetry-and-view-metrics)
  - [Step 10: Continuous Monitoring (Optional)](#step-10-continuous-monitoring-optional)
- [Deep Dive: 30 Vulnerabilities Explained](#-deep-dive-30-vulnerabilities-explained)
  - [Critical Class](#critical-class)
  - [High Severity](#high-severity)
  - [Medium / Systemic](#medium--systemic)
- [How Hawk‑i Detects Each Vulnerability](#-how-hawk-i-detects-each-vulnerability)
- [Understanding the Security Score Formula](#-understanding-the-security-score-formula)
- [Guided Remediation Engine – Under the Hood](#-guided-remediation-engine--under-the-hood)
- [Telemetry – What’s Collected and Why](#-telemetry--whats-collected-and-why)
- [Extending the Demo: Add Your Own Contracts, Rules, or Attack Scripts](#-extending-the-demo-add-your-own-contracts-rules-or-attack-scripts)
- [Troubleshooting Common Issues](#-troubleshooting-common-issues)
- [Contributing to the Demo Suite](#-contributing-to-the-demo-suite)
- [License](#-license)

---

## ✨ What’s New in v0.7.0?

If you’re familiar with Hawk‑i’s earlier versions, here’s what v0.7.0 brings to the table:

| Feature | v0.6.x | v0.7.0 |
|---------|--------|--------|
| **Vulnerability Rules** | ~15–20 | **30+**, each with explanation, impact, and fix templates |
| **Reporting** | Basic markdown list | **Audit‑Grade Reports** (executive summary, score, charts, per‑finding details) |
| **Security Score** | ❌ | ✅ 0–100 deterministic score with risk bands |
| **Remediation** | Ad‑hoc | **Guided Remediation Engine** with context‑aware fix snippets |
| **Exploit Simulation** | Basic success flag | **Detailed metrics** (balances, gas, tx hash) integrated into score & report |
| **Telemetry** | ❌ | ✅ Opt‑in anonymous metrics |
| **Output Formats** | Markdown | Markdown, JSON, HTML, PDF |

The demo suite has been expanded to include **30 distinct vulnerabilities**, each mapped to a detection rule, an attack script (where applicable), and a remediation template.

---

## 📁 Demo Suite Overview

The demo is located in the `demo/` directory of the Hawk‑i project. Its structure reflects the new breadth:

```
demo/
├── contracts/                     # 30 vulnerable Solidity contracts
│   ├── 01_Reentrancy.sol
│   ├── 02_CrossFunctionReentrancy.sol
│   ├── 03_Delegatecall.sol
│   ├── 04_Selfdestruct.sol
│   ├── 05_ProxyStorageCollision.sol
│   ├── 06_MissingInitializer.sol
│   ├── 07_AccessControl.sol
│   ├── 08_OracleManipulation.sol
│   ├── 09_FlashLoan.sol
│   ├── 10_GovernanceVote.sol
│   ├── 11_PermitReplay.sol
│   ├── 12_IntegerOverflow.sol
│   ├── 13_TxOrigin.sol
│   ├── 14_UnsafeExternalCall.sol
│   ├── 15_ApprovalRace.sol
│   ├── 16_TimestampDependency.sol
│   ├── 17_BlockhashRandomness.sol
│   ├── 18_DoS.sol
│   ├── 19_GasGriefing.sol
│   ├── 20_UnboundedLoop.sol
│   ├── 21_InputValidation.sol
│   ├── 22_SignatureMalleability.sol
│   ├── 23_ReusedNonce.sol
│   ├── 24_UninitializedStorage.sol
│   ├── 25_Visibility.sol
│   ├── 26_HardcodedAddress.sol
│   ├── 27_EventEmission.sol
│   ├── 28_ZeroAddress.sol
│   ├── 29_UpgradeAdmin.sol
│   └── 30_CentralizedOwner.sol
├── attack_scripts/                # Exploit scripts (for sandbox)
│   ├── reentrancy.js
│   ├── delegatecall.js
│   ├── flashloan.js
│   └── ... (one per exploitable vulnerability)
├── scripts/                       # Deployment and helper scripts
│   ├── deploy.js
│   └── utils.js
├── hardhat.config.js              # Hardhat configuration
├── package.json                   # Node dependencies
└── README.md                      # This file (you are here!)
```

---

## 🔧 Prerequisites

- **Python 3.9+** with `pip`
- **Node.js 16+** and `npm`
- **Hawk‑i v0.7.0+** installed (see [main README](../README.md) for options)
- **Git** (to clone the repository)
- **Docker** (optional, for exploit simulation)

---

## 🚀 Quick Start (TL;DR)

If you just want to see Hawk‑i scan the demo contracts immediately:

```bash
# 1. Clone the Hawk‑i repository (if not already done)
git clone https://github.com/0xSemantic/hawki.git
cd hawki

# 2. Install Hawk‑i in editable mode (recommended for demos)
pip install -e .

# 3. Enter the demo directory and install Hardhat dependencies
cd demo
npm install

# 4. Start a local Hardhat blockchain
npx hardhat node

# 5. In another terminal, deploy the contracts
npx hardhat run scripts/deploy.js --network localhost

# 6. In a third terminal, run a full Hawk‑i audit
hawki scan . --ai --sandbox --format pdf --telemetry
```

Watch the output – you’ll see static rules flag known vulnerabilities, AI reasoning uncover subtle flaws, the sandbox attempt exploits, and a PDF report generated at the end. The report will include an **executive summary**, a **security score**, charts, and per‑finding remediation snippets.

---

## 🛠️ Detailed Walkthrough

This section takes you step‑by‑step through the entire Hawk‑i v0.7.0 experience, explaining what happens at each stage and how to interpret the results.

### Step 1: Set Up the Environment

First, ensure Hawk‑i is installed and the demo dependencies are ready.

```bash
# From the Hawk‑i root directory
pip install -e .            # or pip install hawki
cd demo
npm install
```

### Step 2: Deploy the Contracts

Open a terminal and start the Hardhat node:

```bash
npx hardhat node
```

This launches a local Ethereum network at `http://127.0.0.1:8545`. Keep it running.

Open a **second terminal**, navigate to `demo/`, and deploy the contracts:

```bash
npx hardhat run scripts/deploy.js --network localhost
```

The script will compile all 30 contracts (this may take a few seconds) and deploy them. It prints the address of each deployed contract. Example:

```
Deploying contracts...

01_Reentrancy deployed to: 0x5FbDB2315678afecb367f032d93F642f64180aa3
02_CrossFunctionReentrancy deployed to: 0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512
03_Delegatecall deployed to: 0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0
...
✅ All contracts deployed.
```

**Note:** The addresses will be different each time you restart the node.

### Step 3: Run a Minimal Scan (Static Rules Only)

Now open a **third terminal** and run a basic scan without AI or sandbox:

```bash
hawki scan .
```

Hawk‑i will:

1. Index all Solidity files in the current directory.
2. Dynamically load all static rules from `core/static_rule_engine/rules/` (30+ rules).
3. Run each rule against the contracts and collect findings.
4. Save a JSON report in `./hawki_reports/` (a timestamped folder).

**Expected output:** You’ll see log messages indicating how many rules were loaded and how many findings were detected. For the demo suite, you should see around 20–25 findings (some contracts have multiple issues). The report will list each finding with severity, file location, and a brief description.

**Example finding (from `01_Reentrancy.sol`):**

```json
{
  "id": "REENT-001",
  "title": "Reentrancy in withdraw()",
  "severity": "Critical",
  "file": "contracts/01_Reentrancy.sol",
  "line": 18,
  "vulnerable_snippet": "function withdraw() public {\n    uint bal = balances[msg.sender];\n    (bool success, ) = msg.sender.call{value: bal}(\"\");\n    require(success);\n    balances[msg.sender] = 0;\n}",
  "explanation": "This function makes an external call before updating state, allowing a malicious contract to re-enter and drain funds.",
  "impact": "An attacker can recursively call withdraw() to steal all funds from the contract."
}
```

**Key observation:** In minimal mode, the `fix_snippet` field is not yet populated (it will be added in enhanced/full mode by the Remediation Engine). The explanation comes from the rule’s built‑in template (since AI is disabled).

### Step 4: Run an Enhanced Scan (with AI)

Now enable AI reasoning. You’ll need an API key for one of the supported LLMs (Gemini, OpenAI, Anthropic). Set it as an environment variable or pass via `--api-key`.

```bash
export OPENAI_API_KEY=sk-...
hawki scan . --ai --ai-model openai/gpt-4
```

What happens:

- Hawk‑i performs the same static analysis as before.
- It also invokes the `ReasoningAgent`, which sends relevant contract code (or summaries) to the LLM.
- The AI may identify **additional issues** that static rules missed, especially in complex contracts like `MysteryLogic.sol` (fee rounding) or `GovernanceVote.sol` (vote manipulation).
- AI findings are merged with static findings. Each AI finding includes an `explanation` field from the LLM.

**Expected AI finding example:**

```json
{
  "id": "AI-001",
  "title": "Fee calculation rounding error",
  "severity": "Medium",
  "file": "contracts/16_MysteryLogic.sol",
  "line": 22,
  "vulnerable_snippet": "uint256 fee = (amount / 100) * 2;",
  "explanation": "The fee calculation uses integer division which truncates. This may lead to under‑collection of fees and economic imbalance.",
  "impact": "Over time, the contract will collect less fees than intended, potentially causing a deficit.",
  "ai_used": true
}
```

**Note:** If you don’t have an API key, you can skip this step or use a local model like Ollama (`--ai-model ollama/codellama`).

### Step 5: Run a Full Audit (AI + Sandbox)

Now add the `--sandbox` flag. This requires Docker to be installed and running.

```bash
hawki scan . --ai --sandbox
```

Hawk‑i will:

- Perform static analysis and AI reasoning as before.
- Start an ephemeral Docker container with a Hardhat node.
- Deploy the contracts **again** inside the sandbox (or use the already deployed ones if you provide addresses).
- For each critical/high vulnerability that has a corresponding attack script, run the script and capture results.
- The sandbox returns detailed metrics: `success`, `before_balance`, `after_balance`, `gas_used`, `transaction_hash`.
- These results are merged into the findings. Successful exploits add a **simulation penalty** to the security score (‑5 each) and appear in the report as `exploit_steps`.

**Example sandbox result for reentrancy:**

```json
"exploit_steps": [
  "1. Deploy ReentrancyDemo contract.",
  "2. Attacker deposits 1 ETH.",
  "3. Attacker deploys malicious contract and calls withdraw().",
  "4. Malicious contract's fallback function re-enters withdraw().",
  "5. State is updated only after multiple withdrawals."
],
"simulation": {
  "success": true,
  "before_balance": "1000000000000000000",
  "after_balance": "0",
  "gas_used": "120000",
  "transaction_hash": "0xabc...123"
}
```

### Step 6: Generate Professional Reports

After the scan, you can generate a report in various formats. If you used `--format pdf` during the scan, the report is generated automatically. Otherwise, use the `hawki report` command:

```bash
hawki report --input ./hawki_reports/latest/findings.json --format html --output audit.html
```

Open `audit.html` in a browser. You’ll see:

- **Executive Summary**: Number of contracts, severity counts, security score, risk classification, and execution mode.
- **Vulnerability Breakdown Chart**: Pie chart (severity distribution) and bar chart (top vulnerability types).
- **Per‑Finding Details**: For each finding, you get the vulnerable code snippet, recommended fix (from Remediation Engine), explanation, impact, and exploit steps (if any).
- **Simulation Metrics**: Success rate and per‑exploit details.

**Example Executive Summary:**

> **Mode:** Full Audit (AI + Sandbox enabled)  
> **Contracts Scanned:** 30  
> **Total Findings:** 28 (5 Critical, 12 High, 8 Medium, 3 Low)  
> **Simulation Success Rate:** 8/12 (66%)  
> **Security Score:** 42/100 – **High Risk**

### Step 7: Understand the Security Score

The security score is a **quantitative measure** of the overall risk posture. It’s calculated as:

**Base score = 100**  
**Deductions:**
- Critical: -15 each
- High: -8 each
- Medium: -4 each
- Low: -1 each

**If sandbox enabled:**  
- Successful exploit: **additional -5** per reproduction (capped at -15 per vulnerability to avoid over‑penalising the same issue).

The final score is mapped to a risk band:

| Score  | Classification |
|--------|----------------|
| 90–100 | Secure         |
| 75–89  | Minor Risk     |
| 50–74  | Moderate Risk  |
| 25–49  | High Risk      |
| 0–24   | Critical Risk  |

You can view the score without generating a full report:

```bash
hawki score ./hawki_reports/latest/findings.json
```

### Step 8: Explore Guided Remediation

Every finding in the report (and in the JSON) now includes a `fix_snippet` field. This snippet is generated by the **Remediation Engine**, which uses:
- A **template** stored in `core/remediation_engine/templates/` (e.g., `reentrancy.json`).
- **Context** from the AST (function names, variable names, etc.) to replace placeholders like `{{function_name}}`.

Example fix snippet for reentrancy:

```solidity
function withdraw() external nonReentrant {
    uint amount = balances[msg.sender];
    balances[msg.sender] = 0;
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success);
}
```

The remediation engine ensures fixes are consistent, secure, and adapted to your actual code.

### Step 9: Opt‑In Telemetry and View Metrics

If you used `--telemetry` during the scan, Hawk‑i collected **anonymous** data:
- Number of scans performed
- Findings per severity
- Simulation success rate (if sandbox used)
- Hawk‑i version
- Execution mode

Data is stored locally in `~/.hawki/metrics.json`. You can view it:

```bash
hawki metrics
```

Example output:
```
Total scans: 12
Findings: Critical=23, High=45, Medium=18, Low=7
Simulation success rate: 71%
Hawk-i version: 0.7.0
```

Telemetry helps the project demonstrate impact and secure funding. **No source code, repository names, or IPs are ever collected.** You can disable telemetry entirely by never using `--telemetry`.

### Step 10: Continuous Monitoring (Optional)

Hawk‑i can also **watch** the demo repository for changes. Try:

```bash
hawki monitor . --interval 30 --alert-log alerts.jsonl
```

Make a small change to one of the `.sol` files (e.g., add a comment), commit it, and you’ll see an alert logged in `alerts.jsonl`. This simulates how Hawk‑i could be used in a CI/CD pipeline or to monitor deployed contracts.

---

## 🔍 Deep Dive: 30 Vulnerabilities Explained

Below is a complete list of the 30 vulnerabilities covered in the demo suite. For each, we describe the issue, how Hawk‑i detects it, and what you’ll see in the report. (Note: Some vulnerabilities are only detectable via AI; static rules may miss them.)

### Critical Class

| #  | Contract / Vulnerability | Detection Method | Exploit Script? | Remediation Template |
|----|---------------------------|------------------|-----------------|----------------------|
| 1  | **Reentrancy** – `01_Reentrancy.sol` | Static rule (`reentrancy`) | ✅ `reentrancy.js` | `reentrancy.json` |
| 2  | **Cross‑Function Reentrancy** – `02_CrossFunctionReentrancy.sol` | Static rule (`cross_function_reentrancy`) | ✅ `cross_function_reentrancy.js` | `cross_function_reentrancy.json` |
| 3  | **Delegatecall to User‑Supplied Address** – `03_Delegatecall.sol` | Static rule (`delegatecall_misuse`) | ✅ `delegatecall.js` | `delegatecall.json` |
| 4  | **Unprotected Selfdestruct** – `04_Selfdestruct.sol` | Static rule (`unprotected_selfdestruct`) | ✅ `selfdestruct.js` | `selfdestruct.json` |
| 5  | **Upgradeable Proxy Storage Collision** – `05_ProxyStorageCollision.sol` | Static rule (`storage_collision`) | ❌ | `storage_collision.json` |
| 6  | **Missing Initializer (UUPS)** – `06_MissingInitializer.sol` | Static rule (`missing_initializer`) | ❌ | `missing_initializer.json` |
| 7  | **Access Control Bypass** – `07_AccessControl.sol` | Static rule (`access_control`) | ✅ `access_control.js` | `access_control.json` |
| 8  | **Oracle Price Manipulation** – `08_OracleManipulation.sol` | AI + Static (basic) | ✅ `oracle_manipulation.js` | `oracle_manipulation.json` |
| 9  | **Flash Loan Price Manipulation** – `09_FlashLoan.sol` | AI (complex logic) | ✅ `flashloan.js` | `flashloan.json` |
| 10 | **Governance Vote Manipulation** – `10_GovernanceVote.sol` | AI (economic) | ✅ `governance_vote.js` | `governance_vote.json` |
| 11 | **Permit Signature Replay** – `11_PermitReplay.sol` | Static rule (`permit_replay`) | ✅ `permit_replay.js` | `permit_replay.json` |
| 12 | **Integer Overflow in `unchecked`** – `12_IntegerOverflow.sol` | Static rule (`integer_overflow`) | ✅ `integer_overflow.js` | `integer_overflow.json` |
| 13 | **Authorization via tx.origin** – `13_TxOrigin.sol` | Static rule (`tx_origin`) | ✅ `tx_origin.js` | `tx_origin.json` |
| 14 | **Unsafe External Call with State Change After** – `14_UnsafeExternalCall.sol` | Static rule (`unsafe_external_call`) | ✅ `unsafe_external_call.js` | `unsafe_external_call.json` |
| 15 | **Improper ERC20 Approval Race Condition** – `15_ApprovalRace.sol` | Static rule (`approval_race`) | ✅ `approval_race.js` | `approval_race.json` |

### High Severity

| #  | Contract / Vulnerability | Detection Method | Exploit Script? | Remediation Template |
|----|---------------------------|------------------|-----------------|----------------------|
| 16 | **Timestamp Dependency** – `16_TimestampDependency.sol` | Static rule (`timestamp_dependency`) | ❌ | `timestamp_dependency.json` |
| 17 | **Blockhash as Randomness** – `17_BlockhashRandomness.sol` | Static rule (`blockhash_randomness`) | ❌ | `blockhash_randomness.json` |
| 18 | **Denial of Service via Unexpected Revert** – `18_DoS.sol` | Static rule (`dos_revert`) | ✅ `dos_revert.js` | `dos_revert.json` |
| 19 | **Gas Griefing** – `19_GasGriefing.sol` | Static rule (`gas_griefing`) | ✅ `gas_griefing.js` | `gas_griefing.json` |
| 20 | **Unbounded Loop (Gas Exhaustion)** – `20_UnboundedLoop.sol` | Static rule (`unbounded_loop`) | ✅ `unbounded_loop.js` | `unbounded_loop.json` |
| 21 | **Improper Input Validation** – `21_InputValidation.sol` | AI + Static (basic) | ❌ | `input_validation.json` |
| 22 | **Signature Malleability** – `22_SignatureMalleability.sol` | Static rule (`signature_malleability`) | ✅ `signature_malleability.js` | `signature_malleability.json` |
| 23 | **Reused Nonce in Signatures** – `23_ReusedNonce.sol` | Static rule (`reused_nonce`) | ✅ `reused_nonce.js` | `reused_nonce.json` |
| 24 | **Uninitialized Storage Pointer** – `24_UninitializedStorage.sol` | Static rule (`uninitialized_storage`) | ❌ | `uninitialized_storage.json` |
| 25 | **Improper Visibility (public instead of internal)** – `25_Visibility.sol` | Static rule (`visibility`) | ❌ | `visibility.json` |

### Medium / Systemic

| #  | Contract / Vulnerability | Detection Method | Exploit Script? | Remediation Template |
|----|---------------------------|------------------|-----------------|----------------------|
| 26 | **Hardcoded Privileged Address** – `26_HardcodedAddress.sol` | Static rule (`hardcoded_address`) | ❌ | `hardcoded_address.json` |
| 27 | **Lack of Event Emission** – `27_EventEmission.sol` | Static rule (`event_emission`) | ❌ | `event_emission.json` |
| 28 | **Missing Zero‑Address Check** – `28_ZeroAddress.sol` | Static rule (`zero_address`) | ❌ | `zero_address.json` |
| 29 | **Improper Upgrade Admin Transfer** – `29_UpgradeAdmin.sol` | Static rule (`upgrade_admin`) | ❌ | `upgrade_admin.json` |
| 30 | **Centralized Owner Risk** – `30_CentralizedOwner.sol` | Static rule (`centralized_owner`) | ❌ | `centralized_owner.json` |

---

## 🧠 How Hawk‑i Detects Each Vulnerability

Hawk‑i uses a **hybrid approach**:

1. **Static Rules** – Pattern‑based detection (e.g., looking for `delegatecall` with variable argument, state updates after external calls). Rules are written in Python and stored in `core/static_rule_engine/rules/`. Each rule produces findings with a predefined severity, explanation, and fix template.

2. **AI Reasoning** – For complex logic flaws (e.g., economic attacks, governance manipulation, rounding errors), Hawk‑i sends the contract source or a summary to an LLM. The AI may also be used to **validate** static findings or suggest additional test cases.

3. **Exploit Simulation** – For vulnerabilities marked as exploitable, the sandbox runs a dedicated attack script. The script’s success or failure is recorded and influences the security score.

4. **Remediation Engine** – After detection, the Remediation Engine uses the rule’s `fix_template` and the AST context to generate a context‑aware fix snippet.

---

## 📊 Understanding the Security Score Formula

The security score is designed to be **deterministic** and **transparent**. Here’s the exact formula used in `scoring_engine.py`:

```python
base_score = 100
deductions = {
    "Critical": 15,
    "High": 8,
    "Medium": 4,
    "Low": 1
}

score = base_score
for finding in findings:
    score -= deductions[finding.severity]

if sandbox_enabled:
    for exploit in successful_exploits:
        score -= 5  # per successful reproduction
        # Cap at -15 per vulnerability? In practice, we cap total penalty to avoid negative score.

score = max(0, min(100, score))
```

The classification is then applied.

**Why these numbers?** They were chosen based on common audit practices: Critical issues are the most severe, so they carry the largest weight. The simulation penalty reflects that a successfully exploited vulnerability is more dangerous than one that is only theoretical.

---

## 🛠️ Guided Remediation Engine – Under the Hood

The Remediation Engine (`core/remediation_engine/engine.py`) works as follows:

1. **Input**: A finding object and the AST of the contract.
2. **Template Lookup**: It looks for a JSON file in `templates/` named after the vulnerability (e.g., `reentrancy.json`).
3. **Placeholder Replacement**: The template contains placeholders like `{{function_name}}`, `{{condition}}`. The engine extracts these from the AST (e.g., the name of the function where the vulnerability occurred).
4. **Output**: A populated `fix_snippet` string, which is added to the finding.

Example template `reentrancy.json`:

```json
{
  "fix_snippet": "function {{function_name}}() {{visibility}} {\n    // Checks‑Effects‑Interactions\n    require({{condition}});\n    {{state_updates}}\n    (bool success, ) = {{external_call}}.call{value: {{amount}}}(\"\");\n    require(success);\n}"
}
```

The engine replaces `{{function_name}}` with `withdraw`, `{{condition}}` with `bal > 0`, etc., based on the actual code.

---

## 📡 Telemetry – What’s Collected and Why

Telemetry is **strictly opt‑in** and designed to be privacy‑preserving:

- **No source code**, repository names, file paths, or IP addresses are ever collected.
- Data collected: total scans, findings per severity, simulation success rate (if sandbox enabled), Hawk‑i version, execution mode, and timestamp (rounded to day).
- Data is stored locally in `~/.hawki/metrics.json`. If you opt in, Hawk‑i may send aggregated stats to a public endpoint to power the community metrics badge (e.g., “Hawk‑i has analyzed X repositories and identified Y critical vulnerabilities”).

To see your local metrics:

```bash
hawki metrics
```

To opt out, simply never use `--telemetry` or set `HAWKI_TELEMETRY=0` in your environment.

---

## 🧩 Extending the Demo: Add Your Own Contracts, Rules, or Attack Scripts

The demo is meant to be a **living suite**. You are encouraged to extend it:

### Adding a New Vulnerable Contract

1. Create a new `.sol` file in `demo/contracts/`.
2. Add the contract name (without `.sol`) to the `CONTRACTS` array in `scripts/deploy.js`.
3. If the vulnerability is exploitable, write an attack script in `demo/attack_scripts/` (JavaScript or Python) and ensure it outputs the required JSON format.
4. Optionally, add a remediation template in `core/remediation_engine/templates/` (if the vulnerability is new to the system).

### Adding a New Static Rule

1. Create a new `.py` file in `core/static_rule_engine/rules/`.
2. Define a class that inherits from `BaseRule` and implements `run_check`.
3. Provide class attributes: `severity`, `explanation_template`, `impact_template`, `fix_template`.
4. Write a unit test in `tests/test_rules.py`.
5. Run the demo to verify detection.

### Adding a New Attack Script

1. Create a new script (JavaScript or Python) in `core/exploit_sandbox/attack_scripts/`.
2. The script must output a JSON object with `success`, `before_balance`, `after_balance`, `gas_used`, `transaction_hash` (optional), and `logs`.
3. Ensure it can be run inside the sandbox container (it will have access to the deployed contract addresses via environment variable `CONTRACT_ADDRESSES`).

---

## 🐛 Troubleshooting Common Issues

- **`ModuleNotFoundError: No module named 'hawki'`**  
  Make sure Hawk‑i is installed (`pip list | grep hawki`) or run from the project root with `python -m cli.hawki_cli`.

- **Hardhat node connection refused**  
  Ensure the node is running (`npx hardhat node`) and that you are using the `--network localhost` flag in deployment scripts.

- **Sandbox fails with Docker errors**  
  Verify Docker is installed and your user has permission to run containers. On Linux, you may need `sudo` or add your user to the `docker` group.

- **AI analysis returns nothing**  
  Check that you have set a valid API key either via `--api-key` or environment variable. Some free tiers have rate limits; try again later.

- **Attack scripts do not succeed**  
  The sandbox uses the default Hardhat accounts and private keys. If you modified the node or deployed to a different network, update the private keys in the attack scripts.

- **Report PDF generation fails**  
  Install optional dependencies: `pip install weasyprint` or `pdfkit`. If not installed, Hawk‑i will fall back to HTML/Markdown.

---

## 🤝 Contributing to the Demo Suite

We welcome contributions! If you have an interesting vulnerability pattern, a clever attack script, or an improvement to the documentation, please open a pull request.

Before contributing, please read our [Contributing Guidelines](../CONTRIBUTING.md). Ensure your code follows the project’s style and includes appropriate tests.

---

## 📄 License

This demo suite is part of the Hawk‑i project and is licensed under the [MIT License](../LICENSE).

---

**Happy hunting, and may your contracts be ever secure!** 🦅

---

*For questions, issues, or feedback, please [open an issue](https://github.com/0xSemantic/hawki/issues) on GitHub.*