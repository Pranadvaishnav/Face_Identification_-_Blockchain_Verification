import { network } from "hardhat";

async function main() {
  const { ethers } = await network.create();

  console.log("Deploying FaceRegistry...");

  const faceRegistry = await ethers.deployContract("FaceRegistry");

  console.log("Waiting for deployment...");

  await faceRegistry.waitForDeployment();

  const address = await faceRegistry.getAddress();

  console.log("=================================");
  console.log("FaceRegistry deployed!");
  console.log("Contract address:", address);
  console.log("=================================");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});