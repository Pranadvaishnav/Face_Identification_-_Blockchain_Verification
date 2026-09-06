import os
from dotenv import load_dotenv
import serpapi

load_dotenv()

API_KEY = os.getenv("SERPAPI_API_KEY")


def reverse_search(image_path):
    if not API_KEY:
        raise ValueError("SERPAPI_API_KEY not found in .env")

    client = serpapi.Client(api_key=API_KEY)

    # Upload local image to SerpApi
    upload = client.upload_image(image_path)

    print("Image uploaded successfully.")

    # Search the uploaded image with Google Lens
    results = client.search({
        "engine": "google_lens",
        "image_id": upload["image_id"],
        "type": "visual_matches"
    })

    return results


if __name__ == "__main__":
    image_path = "sample/test.jpg"

    results = reverse_search(image_path)

    print("\nGoogle Lens search successful!")

    matches = results.get("visual_matches", [])

    print(f"Visual matches found: {len(matches)}")

    for i, result in enumerate(matches[:5], start=1):
        print(f"\n--- Match {i} ---")
        print("Title:", result.get("title"))
        print("Source:", result.get("source"))
        print("URL:", result.get("link"))