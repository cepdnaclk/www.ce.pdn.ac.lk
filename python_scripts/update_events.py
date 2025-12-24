"""
------------------------------------------------------------------------------
Author: Ridma Jayasundara & Nuwan Jaliyagoda
------------------------------------------------------------------------------
"""

import os
from datetime import datetime

import requests
import yaml
from utils.helpers import delete_folder, download_image, get_updated_at

# API URL for events
api_url = "https://portal.ce.pdn.ac.lk/api/events/v1"

directory = "../events"
image_directory = f"{directory}/images/"
post_directory = f"{directory}/_posts/"


# -----------------------------------------------------------------------------------------
def get_events(url):
    """Fetch events from the given API URL and return a dictionary of events."""
    events_dict = {}
    current_page = 1

    while True:
        response = requests.get(f"{url}?page={current_page}", timeout=30)
        print(f"> Page {current_page}: {response.status_code}")

        if response.status_code != 200:
            print(f"Failed to fetch page {current_page}")
            break

        data = response.json()
        for item in data["data"]:
            try:
                events_dict[item["id"]] = item
            except Exception as e:  # noqa: BLE001
                print("Error \t:", str(e))

        if not data["links"]["next"]:
            break
        current_page += 1

    return events_dict


def prepare_gallery(details: dict):
    """Extract gallery data, download assets, and keep only selected fields."""
    slug = (details.get("url") or "").strip() or str(details.get("id", "events"))
    gallery_items = details.get("gallery") or []

    processed = []
    for item in sorted(gallery_items, key=lambda g: g.get("order") or 0):
        urls = item.get("urls") or {}
        original = download_image(urls.get("original"), f"/events/images/{slug}")
        medium = download_image(urls.get("medium"), f"/events/images/{slug}")
        thumb = download_image(urls.get("thumb"), f"/events/images/{slug}")

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


def format_date(datetime_str):
    """Format a datetime string to 'Month Day, Year' format."""
    if datetime_str:
        dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%B %d, %Y")
    return None


def save_event_page(details: dict, file_url: str):
    """Save event details to a markdown file with YAML front matter."""

    content = details.pop("description", "")
    gallery_enabled, gallery_images = prepare_gallery(details)
    start_date = format_date(details.get("start_at"))
    end_date = format_date(details.get("end_at"))
    data = {
        "layout": "page_events",
        "id": details.get("id", -1),
        "title": (details.get("title") or "").strip(),
        "parent": "Events",
        "image": download_image(details["image"].strip(), "/events/images"),
        "start_time": start_date,
        "end_time": end_date,
        "location": (details.get("location") or "").strip(),
        "event_types": details.get("event_type", []),
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
    except IOError as e:
        print(f"Failed to create page '{file_url}': {e}")


def main():
    print("Step 1: Clean-up...")
    delete_folder(image_directory)
    delete_folder(post_directory)
    os.makedirs(post_directory, exist_ok=True)

    print("Step 2: Fetching events...")
    events = get_events(api_url)

    print("Step 3: Updating events...")
    for _, event_details in events.items():
        print(f" - {event_details['title']}")
        file_name = f"{event_details['published_at']}-{event_details['url']}.md"
        file_path = os.path.join(post_directory, file_name)
        save_event_page(event_details, file_path)


if __name__ == "__main__":
    main()
