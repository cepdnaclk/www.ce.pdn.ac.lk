"""
Author : Hirushi Adikari

--------------------------------------------------------------------------------------------

"""
import requests
import json
import os

API_URL = "https://portal.ce.pdn.ac.lk/api/taxonomy/v1/intranet"
DIRECTORY = "_data/intranet.json"

def fetch_and_transform():
    response = requests.get(API_URL)
    response.raise_for_status()
    api_data = response.json()

    if api_data.get("status") != "success":
        raise ValueError("API did not return success status")

    # Start building the output
    result = []

    for category in api_data["data"]["terms"]:
        section_name = category.get("name")
        link_items = []

        for term in category.get("terms", []):
            metadata = term.get("metadata", {})
            name = term.get("name") or metadata.get("title")
            url = metadata.get("link")
            if name and url:
                link_items.append({
                    "name": name,
                    "url": url
                })

        result.append({
            "name": section_name,
            "links": link_items
        })

    return result

def save_to_file(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"✅ intranet.json updated at: {path}")

def main():
    try:
        intranet_data = fetch_and_transform()
        save_to_file(intranet_data, DIRECTORY)
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()