import os
import requests
import shutil

def download_image(url, output_path):
    try:
        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")

        if not content_type.startswith("image/"):
            print(f"Skipped (not an image): {url}")
            return False

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "wb") as file:
            file.write(response.content)

        print(f"Downloaded: {output_path}")
        return True

    except Exception as e:
        print(f"Failed: {url}")
        print(f"Reason: {e}")
        return False


def download_candidates(results, output_dir="data/candidates"):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    os.makedirs(output_dir, exist_ok=True)

    matches = results.get("visual_matches", [])
    downloaded = []

    for i, match in enumerate(matches, start=1):

        # SerpApi's image URL
        image_url = match.get("thumbnail")

        if not image_url:
            print(f"Candidate {i}: no thumbnail found")
            continue

        output_path = os.path.join(
            output_dir,
            f"candidate_{i}.jpg"
        )

        if download_image(image_url, output_path):
            downloaded.append(output_path)

    return downloaded