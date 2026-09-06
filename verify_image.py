import sys

from hashing.hash_generator import generate_sha256
from blockchain_connector import contract


def verify_image(original_image, current_image):
    # Hash the original image
    original_hash = generate_sha256(original_image)

    # Hash the current image
    current_hash = generate_sha256(current_image)

    print("\n================================")
    print("BLOCKCHAIN VERIFICATION")
    print("================================")

    print("Original Hash:")
    print(original_hash)

    print("\nCurrent Hash:")
    print(current_hash)

    # Check whether the original hash exists on blockchain
    registered = contract.functions.isRegistered(original_hash).call()

    if not registered:
        print("\nStatus: NOT_REGISTERED ⚠️")
        print("The original image fingerprint is not on the blockchain.")
        print("================================")
        return "NOT_REGISTERED"

    # Get blockchain record
    record = contract.functions.getRecord(original_hash).call()

    stored_hash = record[0]
    source_url = record[1]
    timestamp = record[2]
    registered_by = record[3]

    print("\nBlockchain Hash:")
    print(stored_hash)

    print("\nSource URL:")
    print(source_url)

    print("\nRegistered By:")
    print(registered_by)

    print("\nTimestamp:")
    print(timestamp)

    # Compare original blockchain fingerprint with current image
    if current_hash == stored_hash:
        print("\nStatus: VERIFIED ✅")
        status = "VERIFIED"
    else:
        print("\nStatus: TAMPERED ❌")
        status = "TAMPERED"

    print("================================")

    return status


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage:")
        print("python verify_image.py <original_image> <current_image>")
        sys.exit(1)

    original_image = sys.argv[1]
    current_image = sys.argv[2]

    verify_image(original_image, current_image)