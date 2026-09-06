import { defineConfig } from "hardhat/config";
import hardhatEthers from "@nomicfoundation/hardhat-ethers";
import dotenv from "dotenv";

dotenv.config({ path: "../.env" });

export default defineConfig({
  plugins: [hardhatEthers],

  paths: {
    sources: "./contracts",
  },

  solidity: {
    version: "0.8.34",
  },

  networks: {
    polygonAmoy: {
      type: "http",
      chainType: "l1",
      url: process.env.POLYGON_AMOY_RPC_URL!,
      accounts: [process.env.PRIVATE_KEY!],
    },
  },
});