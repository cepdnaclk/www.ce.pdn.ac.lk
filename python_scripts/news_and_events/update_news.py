"""
------------------------------------------------------------------------------
Author: Ridma Jayasundara

first the API is read and all the news items are read
then they are stored in NewsItem objects
all the NewsItem objects are then added to a dictionary
key is "id" from API and value is the NewsItem object

then each existing news file is read one by one
its "id" and "updated_at" datetime is taken
based on the "id", the NewsItem object is taken from dictionary
if there is no "id" in the dictionary, that news file is deleted (because that news does not exist in API)
and compare "updated_at" datetime to find any updates
if there are updates, rewrite the file with NewsItem object data (modified news)
if no updates, ignore that item
either case(modified/not modified), that item is removed from dictionary
finally new newsfiles are created for the remaing NewsItem objects in the dictionary (new News that are not in the files)
------------------------------------------------------------------------------
"""

import os
from datetime import datetime, timezone

import requests
import yaml

# api_url = "http://localhost:8000/api/news/v1"
api_url = "https://portal.ce.pdn.ac.lk/api/news/v1"

directory = "../../news/_posts"

# -----------------------------------------------------------------------------------------


class NewsItem:
    def __init__(
        self,
        id,
        title,
        description,
        url,
        author,
        image,
        link_url,
        link_caption,
        created_at,
        published_at,
        updated_at,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.url = url
        self.author = author
        self.image = image
        self.link_url = link_url
        self.link_caption = link_caption
        self.created_at = self._extract_date(created_at)
        self.published_at = published_at
        self.updated_at = self._extract_date_for_updated_at(updated_at)

    def _extract_date(self, datetime_str):
        dt = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        return dt.strftime("%Y-%m-%d")

    def _extract_date_for_updated_at(self, datetime_str):
        # Parse the input datetime string
        dt = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")

        # Add UTC timezone information
        dt_with_tz = dt.replace(tzinfo=timezone.utc)
        return dt_with_tz

    def is_updated(self, given_datetime):
        return self.updated_at != given_datetime

    def __repr__(self):
        return f"NewsItem(id={self.id}, title={self.title})"


def fetch_news(api_url):
    news_dict = {}
    current_page = 1

    while True:
        response = requests.get(f"{api_url}?page={current_page}")
        print(f"> Page {current_page}: {response.status_code}")

        if response.status_code != 200:
            print(f"Failed to fetch page {current_page}")
            break

        data = response.json()
        for item in data["data"]:
            try:
                news_item = NewsItem(
                    id=item["id"],
                    title=item["title"],
                    description=item["description"],
                    url=item["url"],
                    author=item["author"],
                    image=item["image"],
                    link_url=item["link_url"],
                    link_caption=item["link_caption"],
                    created_at=item["created_at"],
                    published_at=item["published_at"],
                    updated_at=item["updated_at"],
                )
                news_dict[item["id"]] = news_item

            except Exception as e:
                print("Error \t:", str(e))

        if not data["links"]["next"]:
            break
        current_page += 1

    return news_dict


def update_markdown_files(directory, news_dict):
    os.makedirs(directory, exist_ok=True)
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                lines = file.readlines()

            metadata, _ = extract_metadata_and_content(lines)
            file_id = metadata.get("id")
            file_updated_at = metadata.get("updated_at")

            if file_id and file_id in news_dict:
                news_item = news_dict[file_id]

                if news_item.is_updated(file_updated_at):
                    rewrite_markdown_file(filepath, news_item)
                else:
                    print("No change \t:", filename)

                del news_dict[file_id]

            else:
                os.remove(filepath)
                print("Deleted \t:", filename, "(Reason: ID not found)")


def extract_metadata_and_content(lines):
    metadata_lines = []
    content_lines = []
    in_metadata = False

    for line in lines:
        if line.strip() == "---":
            in_metadata = not in_metadata
        elif in_metadata:
            metadata_lines.append(line)
        else:
            content_lines.append(line)

    metadata = yaml.safe_load("".join(metadata_lines))
    return metadata, "".join(content_lines)


def rewrite_markdown_file(filepath, news_item):
    new_filename = f"{news_item.published_at}-{news_item.url}.md"
    directory = os.path.dirname(filepath)
    new_filepath = os.path.join(directory, new_filename)

    try:
        os.rename(filepath, new_filepath)
        with open(new_filepath, "w", encoding="utf-8") as file:
            file.write(format_markdown(news_item))
        print("Updated \t:", new_filename)

    except Exception as e:
        print("Update Error\t:", new_filename, str(e))


def create_new_markdown_files(directory, news_dict):
    for news_item in news_dict.values():
        filename = f"{news_item.published_at}-{news_item.url}.md"

        try:
            filepath = os.path.join(directory, filename)
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(format_markdown(news_item))
            print("Created \t:", filename)

        except Exception as e:
            print("Create Error\t:", filename, str(e))


def format_markdown(news_item):
    return f"""---
layout: page_news
id: {news_item.id}
title: "{news_item.title}"

image: {news_item.image}
parent: News
link_url: {news_item.link_url or '#'}
link_caption: "{news_item.link_caption or ''}"

author: {news_item.author}

published_date: {news_item.published_at}
updated_at: {news_item.updated_at}
---

{news_item.description}

<!-- Automated Update by GitHub Actions -->
"""


def main():
    print()
    print("Step 1: Fetching news...")

    # dictionary that holds all the news : key is the id from the API call
    news_items = fetch_news(api_url)

    print()
    print("Step 2: Updating news...")

    # Reads the exiting news files in the directory and compare with the API news items
    # and if there are any changes, rewrite the file with new API data
    update_markdown_files(directory, news_items)

    # If there are new News items, create new .md files for them
    create_new_markdown_files(directory, news_items)


if __name__ == "__main__":
    main()
