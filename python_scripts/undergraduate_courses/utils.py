"""
Author: E/18/227 Dinuka Mudalige - e18227@eng.pdn.ac.lk

- This script will read the data files and create html files for each course.
- This will be a daily process, run as a Cron job

"""

import os
import shutil

import requests


def get_semesters_list(SEMESTERS_API_URL, curriculum_key):
    """
    Fetches the list of semesters for a given curriculum from the API.
    """
    url = SEMESTERS_API_URL.format(curriculum_key)

    response = requests.get(url, timeout=10)
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
        response = requests.get(url, timeout=10)
        api_data = response.json()

        print(f">> Page {page + 1}: {response.status_code}")

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
        print("Error: Courses Folder Not Found!")


def create_new_course_pages(course_data):
    # TODO Use yml library
    # Get the list of Semesters
    # semesters = json.load(open("../../_data/semesters.json"))
    # courses = json.load(open("../../_data/courses.json"))
    for semester in course_data.values():
        courses = semester["courses"]
        print("- " + semester["title"] + " -\n")

        for course in courses:
            # print(course)

            course_code = course["code"]
            # print(course_code)
            # course_title = course["name"]
            # course_credits = course["credits"]
            # type = course["type"]
            prerequisties = course.get("prerequisites", "NULL")

            # content = course["content"]
            # objectives = course["objectives"]
            # ilos_knowledge = course["ILOs"]["Knowledge"]
            # ilos_skill = course["ILOs"]["Skill"]
            # ilos_attitude = course["ILOs"]["Attitude"]

            modules = course["modules"]
            marks = course["marks_allocation"]
            # statistics = course["statistics"]

            pageURL = course["urls"]["view"]
            # gh_page = "https://github.com/cepdnaclk/ce.pdn.ac.lk/tree/main{0}".format(
            #     course["urls"]["edit"]
            # )
            last_edit = course["updated_at"]

            outputString = f"""---
layout: page_course
permalink: "{pageURL}"

title: {course["code"].upper()} {course["name"]}
semester: {semester["title"]}
course_code: {course["code"].upper()}
course_title: {course["name"]}

credits: {course["credits"]}
type: {course["type"]}

prerequisites: {prerequisties}
aims_and_objectives: "{course.get("objectives", "")}"

modules: {course["modules"]}
textbooks_references: {course["references"]}

marks: {marks}

last_edit: {last_edit}
gh_page: #
faq_page: {course["urls"].get("faq_page", "#")}

---"""

            # Write into a file
            file_url = f"../../pages/courses/undergraduate/{semester['url']}/{course_code.strip().upper()}.html"
            os.makedirs(os.path.dirname(file_url), exist_ok=True)
            htmlFile = open(file_url, "w")
            htmlFile.write(outputString)
            htmlFile.close()
            print("Generated: " + course_code.upper() + ".html")

        print("")

    print("Course page generation completed !")
    print("--------------------------------")


# ilos_general: "{course["ilos"]["general"]}"
# ilos_knowledge: "{course["ilos"]["knowledge"]}"
# ilos_skill: "{course["ilos"]["skills"]}"
# ilos_attitude: "{course["ilos"]["attitudes"]}"
