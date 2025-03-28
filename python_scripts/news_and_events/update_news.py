#Script by Ridma Jayasundara

#---------------Script Logic------------
# first the API is read and all the news items are read
# then they are stored in NewsItem objects
# all the NewsItem objects are then added to a dictionary
# key is "id" from API and value is the NewsItem object

# then each existing news file is read one by one
# its "id" and "updated_at" datetime is taken
# based on the "id", the NewsItem object is taken from dictionary
# if there is no "id" in the dictionary, that news file is deleted (because that news does not exist in API)
# and compare "updated_at" datetime to find any updates
# if there are updates, rewrite the file with NewsItem object data (modified news)
# if no updates, ignore that item
# either case(modified/not modified), that item is removed from dictionary
# finally new newsfiles are created for the remaing NewsItem objects in the dictionary (new News that are not in the files)
#---------------------------------------

import requests
import os
import yaml
from datetime import datetime, timezone

class NewsItem:
    def __init__(self, id, title, description, author, image, link_url, link_caption, published_at, updated_at):
        self._id = id
        self._title = title
        self._description = description
        self._author = author
        self._image = image
        self._link_url = link_url
        self._link_caption = link_caption
        self._published_at = published_at
        self._updated_at = self._extract_date_for_updated_at(updated_at)

    
    def _extract_date_for_updated_at(self, datetime_str):
        dt = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ") # Parse the input datetime string
        dt_with_tz = dt.replace(tzinfo=timezone.utc)# Add UTC timezone information
        return dt_with_tz
    
    def is_updated(self, given_datetime):
        return self._updated_at != given_datetime

    def __repr__(self):
        return f"NewsItem(id={self._id}, title={self._title})"


def fetch_news(api_url):
    news_dict = {}
    current_page = 1

    while True:
        response = requests.get(f"{api_url}?page={current_page}")
        if response.status_code != 200:
            print(f"Failed to fetch page {current_page}")
            break
        
        data = response.json()
        for item in data["data"]:
            news_item = NewsItem(
                id=item["id"],
                title=item["title"],
                description=item["description"],
                author=item["author"],
                image=item["image"],
                link_url=item["link_url"],
                link_caption=item["link_caption"],
                published_at=item["published_at"],
                updated_at=item["updated_at"]
            )
            news_dict[item["id"]] = news_item
        
        if not data["links"]["next"]:
            break
        current_page += 1
    
    return news_dict

def read_markdown_files(directory, news_dict):
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                lines = file.readlines()
                
            metadata, content = extract_metadata_and_content(lines)
            file_id = metadata.get("id")
            file_updated_at = metadata.get("updated_at")
            
            if file_id and file_id in news_dict:
                news_item = news_dict[file_id]
                
                if news_item.is_updated(file_updated_at):
                    rewrite_markdown_file(filepath, news_item)
                
                del news_dict[file_id]
                
            else:
                os.remove(filepath)
                print(f"Deleted file: {filename} - ID not found in news dictionary")
    
    create_new_markdown_files(directory, news_dict)

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
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(format_markdown(news_item))
    print("Modified News item : ", f"{news_item._published_at}-{news_item._title.replace(' ', '_')}.md")

def create_new_markdown_files(directory, news_dict):
    for news_item in news_dict.values():
        filename = f"{news_item._published_at}-{news_item._title.replace(' ', '_')}.md"
        filepath = os.path.join(directory, filename)
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(format_markdown(news_item))
        print("created new News Item : ",filename)

def format_markdown(news_item):
    return f"""---
layout: page_news
id: {news_item._id}
title: "{news_item._title}"

image: {news_item._image}
parent: News

link_url: {news_item._link_url or ''}
link_caption: "{news_item._link_caption or ''}"

author: {news_item._author}
published_date: {news_item._published_at}
updated_at: {news_item._updated_at}
---

{news_item._description}
"""

api_url = "https://portal.ce.pdn.ac.lk/api/news/v1"
news_items = fetch_news(api_url) # dictionary that holds all the news : key is the id from the API call

directory = "../../news/_posts"
read_markdown_files(directory, news_items) 
# reads the exiting news files in the directory and compare with the API news items
# and if there are any changes, rewrite the file with new API data
# and if there are new News items, create new .md files for them


