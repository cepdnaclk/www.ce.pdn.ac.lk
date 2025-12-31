import os
import shutil
from datetime import datetime, timezone

import requests


def delete_folder(dir_path):
    """Delete the existing folder"""
    try:
        shutil.rmtree(dir_path)
    except FileNotFoundError:
        print(f"Error: Folder not found at path: {dir_path}")


def get_updated_at(datetime_str):
    """Convert a datetime string to a timezone-aware datetime object in UTC."""
    dt = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    dt_with_tz = dt.replace(tzinfo=timezone.utc)
    return dt_with_tz


def download_image(image_url, save_dir):
    """Download an image from a URL and save it to a local path."""
    try:
        if image_url and image_url != "#":
            image_filename = f"{save_dir}/{image_url.split('/')[-1]}"
            file_url = ".." + image_filename
            try:
                image_response = requests.get(image_url, timeout=30)
                if image_response.status_code == 200:
                    os.makedirs(os.path.dirname(file_url), exist_ok=True)
                    with open(file_url, "wb") as img_file:
                        img_file.write(image_response.content)
                    return image_filename
            except requests.RequestException as e:
                print(f"Failed to download image from {image_url}: {e}")

    except IOError as e:
        print(f"Failed to save image {image_url} to {save_dir}: {e}")

    return "#"


def prepare_gallery(details: dict, image_path_prefix: str):
    """Extract gallery data, download assets, and keep only selected fields."""
    slug = (details.get("url") or "").strip() or str(details.get("id", "events"))
    gallery_items = details.get("gallery") or []

    processed = []
    for item in sorted(gallery_items, key=lambda g: g.get("order") or 0):
        urls = item.get("urls") or {}
        original = download_image(
            urls.get("original"), f"/{image_path_prefix}/images/{slug}"
        )
        medium = download_image(
            urls.get("medium"), f"/{image_path_prefix}/images/{slug}"
        )
        thumb = download_image(urls.get("thumb"), f"/{image_path_prefix}/images/{slug}")

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
        # No gallery display if there is one or no images
        return False, []

    return True, processed
