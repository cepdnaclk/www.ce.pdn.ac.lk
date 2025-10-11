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
