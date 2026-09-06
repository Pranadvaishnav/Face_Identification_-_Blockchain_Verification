import face_recognition


def detect_and_encode(image_path):
    # Load image
    image = face_recognition.load_image_file(image_path)

    # Detect faces
    face_locations = face_recognition.face_locations(image)

    print(f"Faces detected: {len(face_locations)}")

    if not face_locations:
        return []

    # Generate face encodings
    face_encodings = face_recognition.face_encodings(
        image,
        face_locations
    )

    return face_encodings


if __name__ == "__main__":
    image_path = "sample/test.jpg"

    encodings = detect_and_encode(image_path)

    if encodings:
        print(f"Successfully generated {len(encodings)} face encoding(s)")
        print(f"Encoding length: {len(encodings[0])}")
    else:
        print("No face found.")