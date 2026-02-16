# Hawk‑i Demo Suite: Intentionally Vulnerable Contracts

Welcome to the **Hawk‑i Demo Suite** – a collection of Solidity smart contracts deliberately crafted with security flaws. This suite is designed to **test, demonstrate, and validate** every feature of Hawk‑i:

- 🔍 **Static rule engine** – Detects known vulnerability patterns.
- 🧠 **AI reasoning** – Uncovers subtle, logic‑based, or novel issues.
- 💣 **Exploit simulation sandbox** – Automatically attempts to exploit identified weaknesses.
- ⏱️ **Continuous monitoring** – Watches repositories and deployed contracts for changes.

Whether you are a developer evaluating Hawk‑i, a security researcher honing your skills, or a grant reviewer verifying the tool’s capabilities, this demo provides a repeatable, self‑contained environment to see Hawk‑i in action.

---

## 📁 Repository Structure

The demo is located in the `demo/` directory of the Hawk‑i project:

```
demo/
├── contracts/               # Vulnerable Solidity contracts
│   ├── VulnerableToken.sol
│   ├── ReentrancyDemo.sol
│   ├── AccessControlTest.sol
│   ├── DelegateCallExample.sol
│   └── MysteryLogic.sol
├── scripts/                 # Deployment script
│   └── deploy.js
├── hardhat.config.js        # Hardhat configuration
├── package.json             # Node dependencies
└── README.md                # This file
```

---

## 🚀 Quick Start (TL;DR)

If you just want to see Hawk‑i scan the demo contracts immediately:

```bash
# 1. Clone the Hawk‑i repository (if not already done)
git clone https://github.com/0xSemantic/hawki.git
cd hawki

# 2. Install Hawk‑i (if not already installed)
pip install -e .

# 3. Enter the demo directory and install Hardhat dependencies
cd demo
npm install

# 4. Start a local Hardhat blockchain
npx hardhat node

# 5. In another terminal, deploy the contracts
npx hardhat run scripts/deploy.js --network localhost

# 6. In a third terminal, run Hawk‑i scan
hawki scan . --ai --sandbox
```

Watch the output – you’ll see static rules flag known vulnerabilities, AI reasoning attempt to uncover the subtle flaw in `MysteryLogic.sol`, and the sandbox trying to execute exploits (e.g., reentrancy).

---

## 📋 Prerequisites

- **Python 3.9+** with `pip`
- **Node.js 16+** and `npm`
- **Hawk‑i** installed (see [main README](../README.md) for options)
- **Git** (to clone the repository)

Optionally, **Docker** if you want to run the fully containerized demo (see below).

---

## 🛠️ Detailed Setup & Walkthrough

### 1. Install Hawk‑i

If you haven’t already, install Hawk‑i either from PyPI or in editable mode from source:

```bash
# From PyPI
pip install hawki

# OR from source (recommended for development)
git clone https://github.com/0xSemantic/hawki.git
cd hawki
pip install -e .
```

### 2. Prepare the Demo Contracts

Navigate to the `demo/` folder and install the required Node packages:

```bash
cd demo
npm install
```

This installs Hardhat, Ethers, and other dependencies needed to compile and deploy the contracts.

### 3. Start a Local Blockchain

Hardhat comes with a built‑in Ethereum simulator. Run:

```bash
npx hardhat node
```

You’ll see a list of accounts and private keys. Keep this terminal running – it will be our test network.

### 4. Deploy the Contracts

Open a **new terminal**, go to the `demo/` folder again, and execute:

```bash
npx hardhat run scripts/deploy.js --network localhost
```

The script will compile all contracts (if not already compiled) and deploy them to the local Hardhat node. It prints the address of each deployed contract. Make a note of these addresses if you plan to interact with them manually.

Example output:
```
Deploying contracts...

VulnerableToken deployed to: 0x5FbDB2315678afecb367f032d93F642f64180aa3
ReentrancyDemo deployed to: 0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512
AccessControlTest deployed to: 0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0
DelegateCallExample deployed to: 0xCf7Ed3AccA5a467e9e704C703E8D87F634fB0Fc9
MysteryLogic deployed to: 0xDc64a140Aa3E981100a9becA4E685f962f0cF6C9

✅ All contracts deployed.
```

### 5. Run Hawk‑i Scans

Now you can point Hawk‑i to the `demo/` folder and see what it finds.

#### Basic Static Analysis

```bash
hawki scan .
```

This runs only the static rule engine. Expected findings: reentrancy, integer overflow (unchecked block), missing access control, delegatecall misuse. The exact number depends on your rule set.

#### Include AI Reasoning

```bash
hawki scan . --ai
```

The AI will analyse `MysteryLogic.sol` (and possibly others) and may flag the fee‑calculation rounding error. If you have an API key for Gemini/OpenAI, you can specify it with `--api-key` or set the environment variable.

#### Add Exploit Simulation

```bash
hawki scan . --sandbox
```

The sandbox will attempt to run attack scripts (like `reentrancy_test.py` and `access_control_test.py`) against the deployed contracts. It will report which exploits succeeded.

#### Combine Everything

```bash
hawki scan . --ai --sandbox
```

### 6. Continuous Monitoring (Optional)

To see the monitoring subsystem in action, you can run:

```bash
hawki monitor . --interval 30 --alert-log alerts.jsonl
```

This will watch the local Git repository for new commits and the deployed contracts for bytecode changes. Try making a small change to one of the `.sol` files, commit it, and see an alert appear.

---

## 🔍 Contract Details & Vulnerabilities

Each contract in the suite contains one or more intentional flaws. Here’s what to expect from Hawk‑i:

### 1. `VulnerableToken.sol`

- **Vulnerability**: Integer overflow/underflow (simulated via `unchecked` block) and unchecked return value in `transfer`.
- **Hawk‑i Detection**:
  - Static rules: `integer_overflow`, `unchecked_send`
  - AI: May flag the overall lack of safety checks.
  - Sandbox: Could attempt to cause an underflow and drain tokens.

### 2. `ReentrancyDemo.sol`

- **Vulnerability**: Classic reentrancy in `withdraw` – state update after external call.
- **Hawk‑i Detection**:
  - Static rules: `reentrancy`
  - Sandbox: The included `reentrancy_test.py` attack script will try to drain the contract; should succeed.

### 3. `AccessControlTest.sol`

- **Vulnerability**: Public `addAllowed` and `removeAllowed` functions – no access control.
- **Hawk‑i Detection**:
  - Static rules: `access_control`
  - Sandbox: `access_control_test.py` will attempt to call `addAllowed` from a non‑owner account; should succeed.

### 4. `DelegateCallExample.sol`

- **Vulnerability**: `delegatecall` to an arbitrary address supplied by the caller.
- **Hawk‑i Detection**:
  - Static rules: `delegatecall_misuse`
  - Sandbox: Could be exploited to modify the contract’s storage (requires a malicious target contract).

### 5. `MysteryLogic.sol`

- **Vulnerability**: Fee calculation uses integer division, causing rounding errors and incorrect fee collection. Also, balances are updated before checking sufficient funds? Actually it checks, but the rounding flaw is subtle.
- **Hawk‑i Detection**:
  - Static rules: likely miss it – too complex.
  - AI reasoning: Should identify the rounding error and the potential for economic exploit.

---

## 📊 Expected Output & Interpretation

When you run `hawki scan . --ai --sandbox`, you’ll see output similar to:

```
2025-02-16 12:34:56 - hawki.cli - INFO - Scanning target: .
2025-02-16 12:34:57 - hawki.core.static_rule_engine - INFO - Running 10 static rules...
2025-02-16 12:34:58 - hawki.core.static_rule_engine - INFO - Found 5 findings.
2025-02-16 12:34:58 - hawki.core.ai_engine - INFO - Running AI reasoning...
2025-02-16 12:35:05 - hawki.core.ai_engine - INFO - AI found 1 potential issues.
2025-02-16 12:35:05 - hawki.core.exploit_sandbox - INFO - Starting exploit simulation...
...
```

At the end, a JSON report is saved in `./hawki_reports/`. You can open it to see detailed findings, including:

- **Rule name** (e.g., `Reentrancy`)
- **Severity** (HIGH, MEDIUM, LOW, INFO)
- **Description**
- **Location** (file/contract/function)
- **AI‑generated insights** (if any)
- **Sandbox results** (which exploits succeeded)

### Example Finding (from `MysteryLogic.sol` via AI)

```json
{
  "rule": "AI_Reasoning",
  "severity": "MEDIUM",
  "description": "Fee calculation uses integer division which truncates. This may lead to under‑collection of fees and economic imbalance.",
  "location": "MysteryLogic.transferWithFee",
  "source": "ai"
}
```

---

## 🐳 Dockerised Demo (One‑Command Showcase)

For grant reviews, conferences, or quick evaluations, you can run the entire demo inside a Docker container. This eliminates the need to install Node, Hardhat, or even Hawk‑i on your host machine.

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed

### Steps

1. **Build the Docker image** (from the Hawk‑i root directory):

   ```bash
   docker build -f demo/Dockerfile.demo -t hawki-demo .
   ```

2. **Run the container**:

   ```bash
   docker run --rm hawki-demo
   ```

The container will:
- Start a Hardhat node internally.
- Deploy all contracts.
- Execute `hawki scan . --ai --sandbox`.
- Print the results to the console.

You can mount a local directory to persist reports if needed.

---

## 🧪 Extending the Demo

The demo is meant to be a **living suite**. You are encouraged to:

- Add more vulnerable contracts (e.g., oracle manipulation, flash loan attacks).
- Write new **attack scripts** and place them in `hawki/core/exploit_sandbox/attack_scripts/` – they will be auto‑discovered.
- Create new **static rules** in `hawki/core/static_rule_engine/rules/`.
- Tweak the **AI prompt templates** in `hawki/core/ai_engine/prompt_templates/`.

To add a new contract:

1. Create a `.sol` file in `demo/contracts/`.
2. Add its name to the `contracts` array in `scripts/deploy.js`.
3. Redeploy and rescan.

---

## 🐛 Troubleshooting

### Common Issues

- **`ModuleNotFoundError: No module named 'hawki'`**  
  Make sure Hawk‑i is installed (`pip list | grep hawki`) or you are running from the project root with `python -m cli.hawki_cli`.

- **Hardhat node connection refused**  
  Ensure the node is running (`npx hardhat node`) and that you are using the `--network localhost` flag in deployment scripts.

- **Sandbox fails with Docker errors**  
  Verify Docker is installed and your user has permission to run containers. On Linux, you may need `sudo` or add your user to the `docker` group.

- **AI analysis returns nothing**  
  Check that you have set a valid API key either via `--api-key` or environment variable. Some free tiers have rate limits; try again later.

- **Attack scripts do not succeed**  
  The sandbox uses the default Hardhat accounts and private keys. If you modified the node or deployed to a different network, update the private keys in the attack scripts.

---

## 🤝 Contributing

We welcome contributions to the demo suite! If you have an interesting vulnerability pattern or a clever attack script, please open a pull request.

Before contributing, please read our [Contributing Guidelines](../CONTRIBUTING.md) (if available) and ensure your code follows the project’s style.

---

## 📄 License

This demo suite is part of the Hawk‑i project and is licensed under the [MIT License](../LICENSE).

---

**Happy hunting, and may your contracts be ever secure!** 🦅

---

*For questions, issues, or feedback, please [open an issue](https://github.com/0xSemantic/hawki/issues) on GitHub.*