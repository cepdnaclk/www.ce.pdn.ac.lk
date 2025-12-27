"""
------------------------------------------------------------------------------
Author: Ridma Jayasundara & Nuwan Jaliyagoda
------------------------------------------------------------------------------
"""

import os

import requests
import yaml
from utils.helpers import delete_folder, download_image, get_updated_at

api_url = "https://portal.ce.pdn.ac.lk/api/news/v1"

directory = "../news"
image_directory = f"{directory}/images/"
post_directory = f"{directory}/_posts/"


# -----------------------------------------------------------------------------------------
def get_news(url: str):
    """Fetch news items from the API with pagination."""
    news_dict = {}
    current_page = 1

    while True:
        response = requests.get(f"{url}?page={current_page}", timeout=30)
        print(f"> Page {current_page}: {response.status_code}")

        if response.status_code != 200:
            print(f"Failed to fetch page {current_page}")
            break

        data = response.json()
        for item in data.get("data", []):
            try:
                news_dict[item["id"]] = item
            except Exception as error:  # noqa: BLE001
                print("Error \t:", str(error))

        if not data.get("links", {}).get("next"):
            break
        current_page += 1

    return news_dict


def prepare_gallery(details: dict):
    """Extract gallery data, download assets, and keep only selected fields."""
    slug = (details.get("url") or "").strip() or str(details.get("id", "news"))
    gallery_items = details.get("gallery") or []

    processed = []
    for item in sorted(gallery_items, key=lambda g: g.get("order") or 0):
        urls = item.get("urls") or {}
        original = download_image(urls.get("original"), f"/news/images/{slug}")
        medium = download_image(urls.get("medium"), f"/news/images/{slug}")
        thumb = download_image(urls.get("thumb"), f"/news/images/{slug}")

        # Skip entries without any downloadable image
        if all(path == "#" for path in (original, medium, thumb)):
            continue

        processed.append(
            {
                "original": original,
                "medium": medium if medium != "#" else original,
                "thumb": thumb
                if thumb != "#"
                else (medium if medium != "#" else original),
                "caption": (item.get("caption") or "").strip(),
                "alt_text": (item.get("alt_text") or "").strip(),
            }
        )

    if len(processed) <= 1:
        return False, []

    return True, processed


def save_news_page(details: dict, file_url: str):
    """Persist a single news item as a markdown file with front matter."""

    content = (details.get("description") or "").strip()
    gallery_enabled, gallery_images = prepare_gallery(details)
    data = {
        "layout": "page_news",
        "id": details.get("id", -1),
        "title": (details.get("title") or "").strip(),
        "image": download_image(details.get("image"), "/news/images"),
        "parent": "News",
        "link_url": (details.get("link_url") or "#").strip() or "#",
        "link_caption": (details.get("link_caption") or "").strip(),
        "author": (details.get("author") or "").strip(),
        "published_date": (details.get("published_at") or "").strip(),
        "updated_at": get_updated_at((details.get("updated_at") or "").strip()),
        "gallery": gallery_enabled,
        "gallery_images": gallery_images,
    }

    try:
        os.makedirs(os.path.dirname(file_url), exist_ok=True)
        with open(file_url, "w", encoding="utf-8") as f:
            f.write("---\n")
            f.write(yaml.dump(data, sort_keys=False))
            f.write("---\n")
            f.write("\n")
            f.write("<!-- Automated Update by GitHub Actions -->\n")
            f.write("\n")
            f.write(content)
            f.write("\n")
    except IOError as error:
        print(f"Failed to create page '{file_url}': {error}")


def main():
    print("Step 1: Clean-up...")
    delete_folder(image_directory)
    delete_folder(post_directory)
    os.makedirs(post_directory, exist_ok=True)

    print("Step 2: Fetching news...")
    news_items = get_news(api_url)

    print("Step 3: Updating news...")
    for _, news_details in news_items.items():
        print(f" - {news_details['title']}")
        file_name = f"{news_details['published_at']}-{news_details['url']}.md"
        file_path = os.path.join(post_directory, file_name)
        save_news_page(news_details, file_path)


if __name__ == "__main__":
    main()
