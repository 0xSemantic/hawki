const hre = require("hardhat");

async function main() {
  const contracts = [
    "VulnerableToken",
    "ReentrancyDemo",
    "AccessControlTest",
    "DelegateCallExample",
    "MysteryLogic"
  ];

  console.log("Deploying contracts...\n");
  const addresses = {};

  for (const name of contracts) {
    const Contract = await hre.ethers.getContractFactory(name);
    const contract = await Contract.deploy();
    await contract.deployed();
    addresses[name] = contract.address;
    console.log(`${name} deployed to: ${contract.address}`);
  }

  console.log("\n✅ All contracts deployed.");
  console.log("\nContract addresses for reference:\n", JSON.stringify(addresses, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});