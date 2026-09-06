import argparse

from face.face_engine import detect_and_encode
from search.reverse_search import reverse_search
from search.image_downloader import download_candidates
from face.face_matcher import find_best_match
from hashing.hash_generator import generate_sha256
from blockchain_connector import register_fingerprint, verify_fingerprint


def run_pipeline(image_path, register=False):
    print("\n========================================")
    print("              FACECHAIN")
    print("========================================")

    # -------------------------------
    # 1. Face Detection
    # -------------------------------
    print("\n[1] Detecting face...")

    encodings = detect_and_encode(image_path)

    if not encodings:
        print("❌ No face found. Exiting.")
        return

    # -------------------------------
    # 2. Reverse Image Search
    # -------------------------------
    print("\n[2] Searching Google Lens...")

    results = reverse_search(image_path)

    matches = results.get("visual_matches", [])

    print(f"Visual matches found: {len(matches)}")

    if not matches:
        print("❌ No visual matches found. Exiting.")
        return

    # -------------------------------
    # 3. Download Candidates
    # -------------------------------
    print("\n[3] Downloading candidates...")

    downloaded = download_candidates(results)

    if not downloaded:
        print("❌ No candidate images downloaded. Exiting.")
        return

    print(f"Downloaded {len(downloaded)} candidate(s).")

    # -------------------------------
    # 4. Face Matching
    # -------------------------------
    print("\n[4] Matching faces...")

    best_match = find_best_match(
        image_path,
        "data/candidates"
    )

    if not best_match:
        print("❌ No matching face found. Exiting.")
        return

    print("\nBest Match:")
    print(f"Image: {best_match['filename']}")
    print(f"Similarity: {best_match['similarity']:.4f}")

    # -------------------------------
    # 5. SHA-256
    # -------------------------------
    print("\n[5] Generating SHA-256...")

    candidate_path = f"data/candidates/{best_match['filename']}"

    file_hash = generate_sha256(candidate_path)

    print("SHA-256:")
    print(file_hash)

    # -------------------------------
    # Find Source URL
    # -------------------------------
    source_url = ""

    try:
        candidate_number = int(
            best_match["filename"]
            .split("_")[1]
            .split(".")[0]
        )

        if 1 <= candidate_number <= len(matches):
            source_url = matches[candidate_number - 1].get("link", "")

    except Exception:
        pass

    if not source_url:
        source_url = "Unknown"

    print("\nSource URL:")
    print(source_url)

    # -------------------------------
    # 6. Blockchain
    # -------------------------------

    if register:

        print("\n[6] Blockchain Registration...")

        from blockchain_connector import contract

        already_registered = contract.functions.isRegistered(
            file_hash
        ).call()

        if already_registered:

            print("Fingerprint is already registered.")
            print("Skipping new transaction.")

        else:

            tx_hash = register_fingerprint(
                file_hash,
                source_url
            )

            print("\nBlockchain registration successful!")
            print("Transaction:", tx_hash)

    else:

        print("\n[6] Blockchain Verification...")

    # Always verify after registration / normal run
    verify_fingerprint(file_hash)

    print("\n========================================")
    print("Pipeline completed.")
    print("========================================")


def main():

    parser = argparse.ArgumentParser(
        description="FaceChain - Face identification and blockchain verification"
    )

    parser.add_argument(
        "image",
        help="Path to input image"
    )

    parser.add_argument(
        "--register",
        action="store_true",
        help="Register the best-match fingerprint on Polygon Amoy"
    )

    args = parser.parse_args()

    run_pipeline(
        args.image,
        args.register
    )


if __name__ == "__main__":
    main()