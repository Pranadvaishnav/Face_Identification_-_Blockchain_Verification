import os
import json
from dotenv import load_dotenv
from web3 import Web3

# Load .env from project root
load_dotenv()

RPC_URL = os.getenv("POLYGON_AMOY_RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

CONTRACT_ADDRESS = "0x17f8F72de8406dcd91D5760e3f710608B475967C"

ABI_PATH = "blockchain/artifacts/contracts/FaceRegistry.sol/FaceRegistry.json"

if not RPC_URL:
    raise ValueError("POLYGON_AMOY_RPC_URL not found in .env")

if not PRIVATE_KEY:
    raise ValueError("PRIVATE_KEY not found in .env")

# Connect to Polygon Amoy
w3 = Web3(Web3.HTTPProvider(RPC_URL))

if not w3.is_connected():
    raise ConnectionError("Could not connect to Polygon Amoy")

# Load contract ABI
with open(ABI_PATH, "r") as file:
    artifact = json.load(file)

abi = artifact["abi"]

contract = w3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS),
    abi=abi
)

# Wallet
account = w3.eth.account.from_key(PRIVATE_KEY)

print("Connected to Polygon Amoy")
print("Wallet:", account.address)
print("Contract:", CONTRACT_ADDRESS)
def register_fingerprint(fingerprint, source_url):
    nonce = w3.eth.get_transaction_count(account.address)

    transaction = contract.functions.registerFingerprint(
        fingerprint,
        source_url
    ).build_transaction({
        "from": account.address,
        "nonce": nonce,
        "gas": 300000,
        "gasPrice": w3.eth.gas_price,
        "chainId": 80002,
    })

    signed_transaction = w3.eth.account.sign_transaction(
        transaction,
        private_key=PRIVATE_KEY
    )

    tx_hash = w3.eth.send_raw_transaction(
        signed_transaction.raw_transaction
    )

    print("Transaction sent!")
    print("Transaction hash:", tx_hash.hex())

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print("Transaction confirmed!")
    print("Block number:", receipt.blockNumber)

    return tx_hash.hex()
def verify_fingerprint(file_hash):
    # Check whether this exact fingerprint exists
    if not contract.functions.isRegistered(file_hash).call():
        print("\n================================")
        print("BLOCKCHAIN VERIFICATION")
        print("================================")
        print("Current Hash: ", file_hash)
        print("Status:       NOT_REGISTERED ⚠️")
        print("================================")
        return "NOT_REGISTERED"

    # Fingerprint exists on blockchain
    record = contract.functions.getRecord(file_hash).call()

    stored_hash = record[0]
    source_url = record[1]
    timestamp = record[2]
    registered_by = record[3]

    print("\n================================")
    print("BLOCKCHAIN VERIFICATION")
    print("================================")
    print("Stored Hash:   ", stored_hash)
    print("Current Hash:  ", file_hash)
    print("Source URL:    ", source_url)
    print("Timestamp:     ", timestamp)
    print("Registered By: ", registered_by)

    if stored_hash == file_hash:
        print("Status:         VERIFIED ✅")
        status = "VERIFIED"
    else:
        print("Status:         TAMPERED ❌")
        status = "TAMPERED"

    print("================================")

    return status