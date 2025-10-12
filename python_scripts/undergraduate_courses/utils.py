"""
Authors:
    Dinuka Mudalige (e18227@eng.pdn.ac.lk)
    Nuwan Jaliyagoda (nuwanjaliyagoda@eng.pdn.ac.lk)

- This script will read the data files and create html files for each course.
- This will be a daily process, run as a Cron job

"""

import os
import shutil
from datetime import datetime

import requests
import yaml


def get_semesters_list(SEMESTERS_API_URL, curriculum_key):
    """
    Fetches the list of semesters for a given curriculum from the API.
    """
    url = SEMESTERS_API_URL.format(curriculum_key)
    response = requests.get(url, timeout=30)
    api_data = response.json()
    return api_data.get("data", [])


def get_courses_list(COURSES_API_URL, curriculum_key):
    """
    Fetches the list of courses for a given curriculum from the API.
    Handles pagination to retrieve all courses.
    """
    page = 1
    courses = []
    url = COURSES_API_URL.format(curriculum_key, page)

    while url is not None:
        response = requests.get(url, timeout=30)
        api_data = response.json()

        print(f">> Page {page} | Response:{response.status_code}")

        courses.extend(api_data["data"])

        if api_data.get("links", {}).get("next") is None:
            # End of the pagination
            break

        page += 1
        url = COURSES_API_URL.format(curriculum_key, page)

    return courses


def delete_existing_course_pages():
    """Delete the existing folder"""

    dir_path = "../../pages/courses/undergraduate/"
    try:
        shutil.rmtree(dir_path)
    except FileNotFoundError:
        print(f"Error: Courses Folder Not Found at path: {dir_path}")


def create_new_course_pages(course_data):
    """Create new course pages from the course data"""

    for semester in course_data.values():
        courses = semester["courses"]
        print("- " + semester["title"] + " -\n")

        for course in courses:
            try:
                course_code = course["code"]
                page_url = course["urls"]["view"]
                title = " ".join(
                    [course["code"].strip().upper(), course["name"].strip()]
                )
                curriculum_name = (
                    course["academic_program"].get("curriculum_name", "-").strip()
                )
                marks_allocation = {
                    k: v for k, v in course["marks_allocation"].items() if v is not None
                }
                course_references = [
                    ref.strip() for ref in course.get("references", [])
                ]
                course_modules = [
                    {
                        "topic": module["topic"].strip(),
                        "description": module["description"].strip(),
                        "time_allocation": {
                            k: v
                            for k, v in module["time_allocation"].items()
                            if v is not None
                        },
                    }
                    for module in course["modules"]
                ]
                prerequisites = [
                    {
                        "id": p["id"],
                        "code": p["code"].strip(),
                        "name": p["name"].strip(),
                        "url": p["urls"]["view"]
                        .replace("https://www.ce.pdn.ac.lk", "")
                        .replace(" ", ""),
                    }
                    for p in course.get("prerequisites", [])
                ]

                try:
                    last_edit = datetime.fromisoformat(course["updated_at"]).strftime(
                        "%Y-%m-%d"
                    )
                except ValueError:
                    last_edit = ""
                    print(
                        f"Error: Invalid date format '{course['updated_at']}' for course {course['code']}"
                    )

                course_data = {
                    "layout": "page_course",
                    "permalink": page_url,
                    #
                    "title": title,
                    "course_code": course.get("code", "").upper(),
                    "course_title": course.get("name", "").strip(),
                    "curriculum": curriculum_name,
                    "semester": semester.get("title", "").strip(),
                    #
                    "course_content": course.get("content") or "",
                    #
                    "credits": course.get("credits"),
                    "type": course.get("type"),
                    "prerequisites": prerequisites,
                    "aims_and_objectives": course.get("objectives"),
                    "modules": course_modules,
                    "textbooks_references": course_references,
                    "marks": marks_allocation,
                    #
                    "ilos_general": course["ilos"].get("general", []),
                    "ilos_knowledge": course["ilos"].get("knowledge", []),
                    "ilos_skills": course["ilos"].get("skills", []),
                    "ilos_attitudes": course["ilos"].get("attitudes", []),
                    #
                    "last_edit": last_edit,
                    "edit_page": course["urls"].get("edit", "#"),
                    "faq_page": course["urls"].get("faq", "#"),
                    "color_code": course["color_code"],
                }

                # Write into a file
                file_url = f"../../pages/courses/undergraduate/{course_code.strip().upper()}.html"
                os.makedirs(os.path.dirname(file_url), exist_ok=True)
                try:
                    with open(file_url, "w", encoding="utf-8") as f:
                        f.write("---\n")
                        f.write(yaml.dump(course_data, sort_keys=False))
                        f.write("---\n\n")
                        f.write("")
                    print("Generated: " + course_code.upper() + ".html")
                except Exception as e:
                    print(
                        f"Error: generating file for course {course_code.upper()}: {e}"
                    )

            except KeyError as e:
                print(
                    f"Error: Missing key {e} in course data for {course_code.upper()}"
                )
            except Exception as e:
                print(f"Error: Unexpected error for course {course_code.upper()}: {e}")

        print("")

    print("Course page generation completed !")
    print("--------------------------------")
