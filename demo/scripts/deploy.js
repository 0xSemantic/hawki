const hre = require("hardhat");

const CONTRACT_NAMES = [
  "ReentrancyDemo",
  "CrossFunctionReentrancy",
  "DelegatecallExample",
  "SelfdestructVulnerable",
  "Proxy",
  "MissingInitializer",
  "AccessControlBypass",
  "OracleManipulation",
  "FlashLoanVulnerable",
  "GovernanceVote",
  "PermitReplay",
  "IntegerOverflowUnchecked",
  "TxOriginAuth",
  "UnsafeExternalCall",
  "ApprovalRace",
  "TimestampDependency",
  "BlockhashRandomness",
  "DoS",
  "GasGriefing",
  "UnboundedLoop",
  "InputValidation",
  "SignatureMalleability",
  "ReusedNonce",
  "UninitializedStorage",
  "Visibility",
  "HardcodedAddress",
  "EventEmission",
  "ZeroAddress",
  "UpgradeAdmin",
  "CentralizedOwner",
  "VulnerableToken",
  "ReentrancyDemo",
  "AccessControlTest",
  "DelegateCallExample",
  "MysteryLogic"
];

async function main() {
  console.log("Deploying contracts...\n");
  const addresses = {};

  for (const name of CONTRACT_NAMES) {
    const Contract = await hre.ethers.getContractFactory(name);
    const contract = await Contract.deploy();
    await contract.waitForDeployment();
    addresses[name] = contract.target;
    console.log(`${name} deployed to: ${contract.target}`);
  }

  console.log("\n✅ All contracts deployed.");
  console.log("\nContract addresses:\n", JSON.stringify(addresses, null, 2));
}

main().catch(console.error);