from search.reverse_search import reverse_search
from search.image_downloader import download_candidates


image_path = "sample/test.jpg"

print("Running Google Lens...")
results = reverse_search(image_path)

print("\nDownloading candidates...")
downloaded = download_candidates(results)

print(f"\nSuccessfully downloaded: {len(downloaded)} candidates")

for image in downloaded:
    print(image)