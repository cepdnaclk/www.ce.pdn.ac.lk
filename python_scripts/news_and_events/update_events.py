# based on news_update.py, this script was generated using claude.ai 
# by Ridma Jayasundara

import os
from datetime import datetime, timezone

import requests
import yaml

# API URL for events
api_url = "https://portal.ce.pdn.ac.lk/api/events/v1"

# Directory containing event markdown files
directory = "../../events/_posts"

# -----------------------------------------------------------------------------------------


class EventItem:
    def __init__(
        self,
        id,
        title,
        description,
        url,
        author,
        image,
        start_at,
        end_at,
        event_type,
        location,
        link_url,
        link_caption,
        published_at,
        created_at,
        updated_at,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.url = url
        self.author = author
        self.image = image
        self.start_at = self._format_datetime(start_at) if start_at else None
        self.end_at = self._format_datetime(end_at) if end_at else None
        self.event_type = event_type
        self.location = location
        self.link_url = link_url
        self.link_caption = link_caption
        self.published_at = published_at
        self.created_at = self._extract_date(created_at)
        self.updated_at = self._extract_date_for_updated_at(updated_at)

    def _format_datetime(self, datetime_str):
        dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%B %d, %Y")

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
        return f"EventItem(id={self.id}, title={self.title})"


def fetch_events(api_url):
    events_dict = {}
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
                event_item = EventItem(
                    id=item["id"],
                    title=item["title"],
                    description=item["description"],
                    url=item["url"],
                    author=item["author"],
                    image=item["image"],
                    start_at=item["start_at"],
                    end_at=item["end_at"],
                    event_type=item["event_type"],
                    location=item["location"],
                    link_url=item["link_url"],
                    link_caption=item["link_caption"],
                    published_at=item["published_at"],
                    created_at=item["created_at"],
                    updated_at=item["updated_at"],
                )
                events_dict[item["id"]] = event_item

            except Exception as e:
                print("Error \t:", str(e))

        if not data["links"]["next"]:
            break
        current_page += 1

    return events_dict


def update_markdown_files(directory, events_dict):
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                lines = file.readlines()

            metadata, _ = extract_metadata_and_content(lines)
            file_id = metadata.get("id")
            file_updated_at = metadata.get("updated_at")

            if file_id and file_id in events_dict:
                event_item = events_dict[file_id]

                if event_item.is_updated(file_updated_at):
                    rewrite_markdown_file(filepath, event_item)
                else:
                    print("No change \t:", filename)

                del events_dict[file_id]

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


def rewrite_markdown_file(filepath, event_item):
    new_filename = f"{event_item.published_at}-{event_item.url}.md"
    directory = os.path.dirname(filepath)
    new_filepath = os.path.join(directory, new_filename)
    
    try:
        os.rename(filepath, new_filepath)
        with open(new_filepath, "w", encoding="utf-8") as file:
            file.write(format_markdown(event_item))     
        print("Updated \t:", new_filename)   
        
    except Exception as e:
        print("Update Error\t:", new_filename, str(e))


def create_new_markdown_files(directory, events_dict):
    for event_item in events_dict.values():
        filename = f"{event_item.published_at}-{event_item.url}.md"

        try:
            filepath = os.path.join(directory, filename)
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(format_markdown(event_item))
            print("Created \t:", filename)

        except Exception as e:
            print("Create Error\t:", filename, str(e))


def format_markdown(event_item):
    # Format end time section based on whether it exists
    end_time_line = f'end_time: "{event_item.end_at}"' if event_item.end_at else 'end_time: #'
    
    # Join event types into a string for display
    event_type_str = ", ".join(event_item.event_type) if event_item.event_type else ""
    
    return f"""---
layout: page_events
id: {event_item.id}
title: "{event_item.title}"
parent: Events
image: {event_item.image}
start_time: "{event_item.start_at}"
{end_time_line}
location: "{event_item.location}"
event_type: "{event_type_str}"
link_url: {event_item.link_url or '#'}
link_caption: "{event_item.link_caption or ''}"
author: {event_item.author}
published_date: {event_item.published_at}
updated_at: {event_item.updated_at}
---

{event_item.description}

<!-- Automated Update by GitHub Actions -->
"""


def main():
    print()
    print("Step 1: Fetching events...")

    # Dictionary that holds all the events: key is the id from the API call
    events_items = fetch_events(api_url)

    print()
    print("Step 2: Updating events...")

    # Create directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    # Reads the existing event files in the directory and compare with the API event items
    # and if there are any changes, rewrite the file with new API data
    update_markdown_files(directory, events_items)

    # If there are new Event items, create new .md files for them
    create_new_markdown_files(directory, events_items)


if __name__ == "__main__":
    main()