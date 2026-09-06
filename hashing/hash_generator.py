import hashlib


def generate_sha256(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while chunk := file.read(8192):
            sha256.update(chunk)

    return sha256.hexdigest()


if __name__ == "__main__":

    image_path = "data/candidates/candidate_1.jpg"

    file_hash = generate_sha256(image_path)

    print("SHA-256 Hash:")
    print(file_hash)