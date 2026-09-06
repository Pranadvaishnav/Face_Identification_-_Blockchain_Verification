# FaceChain

FaceChain is a CLI-based face identification and image verification system that combines face recognition, reverse image search, SHA-256 hashing, and blockchain verification.

The system takes an input image, searches for visually similar images, compares faces using face embeddings, identifies the best matching candidate, generates a cryptographic fingerprint for that image, and verifies the fingerprint against a record stored on the Polygon Amoy Testnet.

---

## Features

- Face detection using face_recognition
- 128-dimensional face embeddings
- Reverse image search using Google Lens through SerpApi
- Automatic candidate image downloading
- Face similarity comparison using cosine similarity
- Best-match candidate identification
- SHA-256 cryptographic fingerprint generation
- Blockchain fingerprint registration
- Blockchain-based image verification
- Tamper detection
- CLI-based workflow

---

## Architecture

                    +-----------------+
                    |   Input Image   |
                    +--------+--------+
                             |
                             v
                    +-----------------+
                    | Face Detection  |
                    +--------+--------+
                             |
                             v
                    +-----------------+
                    |  Google Lens    |
                    | Reverse Search  |
                    +--------+--------+
                             |
                             v
                    +-----------------+
                    | Candidate       |
                    | Images          |
                    +--------+--------+
                             |
                             v
                    +-----------------+
                    | Face Embeddings |
                    | + Similarity    |
                    +--------+--------+
                             |
                             v
                    +-----------------+
                    |   Best Match    |
                    +--------+--------+
                             |
                             v
                    +-----------------+
                    |    SHA-256      |
                    |   Fingerprint   |
                    +--------+--------+
                             |
                             v
                    +-----------------+
                    | Polygon Amoy    |
                    |    Testnet      |
                    +--------+--------+
                             |
                    +--------+--------+
                    |                 |
                    v                 v
               Same Hash         Different Hash
                    |                 |
                    v                 v
             VERIFIED          TAMPERED

---

## How It Works

### 1. Face Detection

The input image is processed using the face_recognition library.

The system detects faces and generates a 128-dimensional face encoding for the detected face.

### 2. Reverse Image Search

The input image is uploaded to Google Lens through SerpApi.

The system retrieves visually similar image results from the web.

### 3. Candidate Collection

The returned candidate images are downloaded into:

data/candidates/

### 4. Face Matching

Each candidate image is processed to detect a face and generate its face encoding.

The system calculates the cosine similarity between the input face encoding and candidate face encodings.

The candidate with the highest similarity score is selected as the best match.

Example:

candidate_1.jpg: 0.9914
candidate_2.jpg: 0.9647
candidate_3.jpg: 0.9641

Best Match:
candidate_1.jpg

Similarity:
0.9914

### 5. SHA-256 Fingerprinting

The selected candidate image is hashed using SHA-256.

Example:

221cb32c1c7d6a01dfa86dd5f4eeec3240ce9b5ec2eb67aad07a1174464a6650

This fingerprint represents the exact contents of the file.

### 6. Blockchain Verification

The SHA-256 fingerprint is stored on the Polygon Amoy Testnet through the FaceRegistry smart contract.

The contract stores:

- Image fingerprint
- Source URL
- Registration timestamp
- Registering wallet address

### 7. Tamper Detection

When an image is modified, its SHA-256 hash changes.

For example:

Original:

221cb32c...

Modified:

f8290e3e...

The modified hash no longer matches the blockchain record.

The system therefore reports:

TAMPERED

---

## Blockchain

FaceChain uses:

Blockchain: Polygon
Network: Polygon Amoy Testnet
Chain ID: 80002
Smart Contract: FaceRegistry

### Contract Address

0x17f8F72de8406dcd91D5760e3f710608B475967C

The smart contract provides functions to:

registerFingerprint()
getRecord()
isRegistered()

The contract prevents the same fingerprint from being registered more than once.

---

## Project Structure

faceChain/
|
+-- blockchain/
|   +-- contracts/
|   |   +-- FaceRegistry.sol
|   +-- scripts/
|   |   +-- deploy.ts
|   +-- artifacts/
|   +-- hardhat.config.ts
|   +-- package.json
|   +-- ...
|
+-- data/
|   +-- candidates/
|
+-- face/
|   +-- face_engine.py
|   +-- face_matcher.py
|
+-- hashing/
|   +-- hash_generator.py
|
+-- search/
|   +-- reverse_search.py
|   +-- image_downloader.py
|
+-- results/
|
+-- sample/
|   +-- test.jpg
|   +-- 8.jpg
|
+-- src/
|   +-- test_pipeline.py
|
+-- tests/
|
+-- blockchain_connector.py
+-- verify_image.py
+-- main.py
+-- config.py
+-- requirements.txt
+-- .env.example
+-- .gitignore
+-- README.md

---

## Requirements

- Python 3.13
- Node.js
- npm
- Git
- MetaMask wallet
- Polygon Amoy testnet account
- SerpApi API key
- Polygon RPC endpoint
- Wallet private key for blockchain transactions

Note:

The project was originally planned around Python 3.10 because of compatibility considerations with face_recognition. The current implementation has been tested with Python 3.13.

---

## Installation

### 1. Clone the repository

git clone <YOUR_GITHUB_REPOSITORY_URL>

cd faceChain

### 2. Create a virtual environment

Windows:

python -m venv venv

Activate it using Git Bash:

source venv/Scripts/activate

Or using Command Prompt:

venv\Scripts\activate

### 3. Install Python dependencies

pip install -r requirements.txt

---

## Environment Variables

Create a .env file in the project root.

Add:

SERPAPI_API_KEY=your_serpapi_api_key
POLYGON_AMOY_RPC_URL=your_polygon_amoy_rpc_url
PRIVATE_KEY=your_wallet_private_key

IMPORTANT:

Never commit the .env file to GitHub.

The repository should contain .env.example, but not your actual .env file.

---

## Smart Contract Setup

The project uses Hardhat for smart contract development.

Go to the blockchain directory:

cd blockchain

Install dependencies:

npm install

Compile the contract:

npx hardhat compile

Deploy to Polygon Amoy:

npx hardhat run scripts/deploy.ts --network polygonAmoy

After deployment, copy the deployed contract address into:

blockchain_connector.py

Then return to the project root:

cd ..

---

## Running FaceChain

### Normal Verification

Run:

python main.py sample/test.jpg

The pipeline performs:

Face Detection
        |
        v
Google Lens Search
        |
        v
Candidate Download
        |
        v
Face Matching
        |
        v
Best Match
        |
        v
SHA-256
        |
        v
Blockchain Verification

Example final output:

Best Match:
Image: candidate_1.jpg
Similarity: 0.9914

SHA-256:
221cb32c1c7d6a01dfa86dd5f4eeec3240ce9b5ec2eb67aad07a1174464a6650

[6] Blockchain Verification...

Status: VERIFIED

---

## Registering a Fingerprint

To register a new fingerprint on Polygon Amoy:

python main.py sample/test.jpg --register

The system first checks whether the fingerprint is already registered.

If it is not registered, a blockchain transaction is submitted.

The transaction hash is displayed after confirmation.

---

## Tamper Detection Demo

FaceChain can demonstrate that modifying an image changes its cryptographic fingerprint.

Create a copy:

cp data/candidates/candidate_1.jpg data/candidates/tampered.jpg

Modify the copy:

python -c "from PIL import Image; p='data/candidates/tampered.jpg'; im=Image.open(p); im.save(p, quality=50)"

Verify the modified image:

python verify_image.py data/candidates/candidate_1.jpg data/candidates/tampered.jpg

Expected result:

Original Hash:
221cb32c...

Current Hash:
f8290e3e...

Blockchain Hash:
221cb32c...

Status: TAMPERED

---

## Verification Logic

FaceChain uses the following verification principle:

Blockchain Hash
       |
       |
       v
    Compare
       ^
       |
       |
Current File Hash

If:

Current Hash == Blockchain Hash

the file is reported as:

VERIFIED

Otherwise:

TAMPERED

If the original fingerprint does not exist on the blockchain:

NOT_REGISTERED

---

## Known Limitations

### 1. Face recognition is not perfect

Face similarity scores depend on image quality, pose, lighting, resolution, and other factors.

A high similarity score should not be treated as absolute proof of identity.

### 2. Reverse image search depends on external services

Google Lens results are accessed through SerpApi.

Search results can change or fail depending on API availability, rate limits, network conditions, and indexed content.

### 3. Candidate image availability

Some images returned by reverse image search may not be downloadable because of:

- Hotlink protection
- Invalid URLs
- Network errors
- Access restrictions
- Non-image responses

### 4. Polygon Amoy is a testnet

The current deployment uses Polygon Amoy Testnet and is intended for demonstration/testing rather than production use.

### 5. SHA-256 verifies file integrity, not visual authenticity

SHA-256 proves whether the exact file contents match the registered fingerprint.

It does not determine whether the original image itself is truthful, authentic, or AI-generated.

### 6. CLI only

The current version is a command-line application and does not include a web frontend.

### 7. Private key security

The blockchain transaction requires a wallet private key.

The private key must be stored securely in environment variables and must NEVER be committed to the repository.

---

## Security

Before pushing the project to GitHub, make sure these files are ignored:

.env
venv/
node_modules/
__pycache__/

Check your Git status with:

git status

Make sure your private key is not present anywhere in the repository.

---

## Technologies Used

Python
    Main application

face_recognition
    Face detection and face embeddings

NumPy
    Similarity calculations

SerpApi
    Google Lens reverse image search

Requests
    Image downloading

SHA-256
    Cryptographic fingerprinting

Solidity
    Smart contract

Hardhat
    Smart contract development and deployment

Web3.py
    Python to blockchain communication

Polygon Amoy
    Blockchain testnet

MetaMask
    Testnet wallet

---

## Project Goal

FaceChain explores how AI-based face identification and blockchain-based integrity verification can be combined into a single pipeline.

The system does not attempt to prove that a person is the real-world identity represented by an image.

Instead, it:

1. Finds visually similar online images.
2. Uses face similarity to identify a likely matching image.
3. Generates a cryptographic fingerprint of that image.
4. Records the fingerprint on-chain.
5. Later checks whether the file still matches the registered fingerprint.

---

## Example Result

A successful verification:

FACECHAIN

Input Image
     |
     v
Face Detected: 1
     |
     v
Google Lens Matches: 59
     |
     v
Best Match: candidate_1.jpg
     |
     v
Face Similarity: 0.9914
     |
     v
SHA-256: 221cb32c...
     |
     v
Polygon Amoy
     |
     v
VERIFIED

After modifying the file:

Original Hash: 221cb32c...
Current Hash:  f8290e3e...

Blockchain Hash: 221cb32c...

Status: TAMPERED

---

## Author

Pranad Vaishnav

FaceChain - Face Identification & Blockchain-Based Image Integrity Verification

---

## License

This project is intended for educational, experimental, and hackathon purposes.