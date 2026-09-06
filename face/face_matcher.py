import os
import numpy as np
import face_recognition


def get_face_encoding(image_path):
    """Detect the first face and return its 128D encoding."""
    image = face_recognition.load_image_file(image_path)

    locations = face_recognition.face_locations(image)

    if not locations:
        return None

    encodings = face_recognition.face_encodings(image, locations)

    if not encodings:
        return None

    return encodings[0]


def cosine_similarity(a, b):
    """Calculate cosine similarity between two face encodings."""
    a = np.array(a)
    b = np.array(b)

    denominator = np.linalg.norm(a) * np.linalg.norm(b)

    if denominator == 0:
        return 0.0

    return float(np.dot(a, b) / denominator)


def find_best_match(target_path, candidates_dir):
    """Compare target face against all candidate images."""
    
    target_encoding = get_face_encoding(target_path)

    if target_encoding is None:
        print("No face found in target image.")
        return None

    results = []

    for filename in os.listdir(candidates_dir):

        if not filename.lower().endswith(
            (".jpg", ".jpeg", ".png", ".webp")
        ):
            continue

        candidate_path = os.path.join(candidates_dir, filename)

        candidate_encoding = get_face_encoding(candidate_path)

        if candidate_encoding is None:
            print(f"Skipping {filename}: no face found")
            continue

        similarity = cosine_similarity(
            target_encoding,
            candidate_encoding
        )

        results.append({
            "filename": filename,
            "similarity": similarity
        })

        print(
            f"{filename}: "
            f"{similarity:.4f}"
        )

    if not results:
        print("No candidates with detectable faces.")
        return None

    best_match = max(
        results,
        key=lambda x: x["similarity"]
    )

    return best_match


if __name__ == "__main__":

    target = "sample/test.jpg"
    candidates = "data/candidates"

    print("Comparing faces...\n")

    best = find_best_match(target, candidates)

    if best:
        print("\n==============================")
        print("BEST MATCH")
        print("==============================")
        print(f"Image: {best['filename']}")
        print(f"Similarity: {best['similarity']:.4f}")