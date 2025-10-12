"""
Author : Hirushi Adikari

--------------------------------------------------------------------------------------------

"""

import json
import os

import requests

API_URL = "https://portal.ce.pdn.ac.lk/api/taxonomy/v1/intranet"
DIRECTORY = "../../_data/intranet.json"


def safe_index(item):
    """Extract integer index or push to end if not present or invalid."""
    index = item.get("metadata", {}).get("index")
    try:
        return int(index)
    except (ValueError, TypeError):
        return float("inf")


def sort_terms(terms):
    """Sort a list of terms by index and recursively sort inner terms."""
    sorted_terms = sorted(terms, key=safe_index)
    for term in sorted_terms:
        if "terms" in term:
            term["terms"] = sort_terms(term["terms"])
    return sorted_terms


def fetch_and_transform():
    response = requests.get(API_URL, timeout=30)
    response.raise_for_status()
    api_data = response.json()

    if api_data.get("status") != "success":
        raise ValueError("API did not return success status")

    top_level_terms = sort_terms(api_data["data"]["terms"])  # sort top-level

    result = []
    for category in top_level_terms:
        section_name = category.get("name")
        link_items = []

        sorted_inner = sort_terms(category.get("terms", []))  # sort children

        for term in sorted_inner:
            metadata = term.get("metadata", {})
            name = term.get("name") or metadata.get("title")
            url = metadata.get("link")
            if name and url:
                link_items.append({"name": name, "url": url})

        result.append({"name": section_name, "links": link_items})

    return result


def save_to_file(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"intranet.json updated at: {path}")


def main():
    try:
        intranet_data = fetch_and_transform()
        save_to_file(intranet_data, DIRECTORY)
    except (requests.RequestException, ValueError, OSError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
