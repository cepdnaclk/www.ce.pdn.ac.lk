"""
Author: Nuwan Jaliyagoda (nuwanjaliyagoda@eng.pdn.ac.lk)
"""

import json

from utils import (
    create_new_course_pages,
    delete_existing_course_pages,
    get_courses_list,
    get_semesters_list,
)

curriculums = {
    1: "rev-2013",
    2: "rev-2022",
}

course_color_codes = {
    "CO": "btn-outline-primary",
    "EE": "btn-outline-success",
    "EM": "btn-outline-danger",
    "GP": "btn-outline-warning",
}

COURSES_API_URL = "https://portal.ce.pdn.ac.lk/api/academic/v1/undergraduate/courses?curriculum={0}&page={1}"
SEMESTERS_API_URL = (
    "https://portal.ce.pdn.ac.lk/api/academic/v1/undergraduate/semesters?curriculum={0}"
)
DIRECTORY = "../../_data/courses_v{0}.json"

# Phase 0: Cleanup the pages
delete_existing_course_pages()


for curriculum_key, curriculum_name in curriculums.items():
    print(f"\nSyncing curriculum {curriculum_key}...")

    # Phase 1: Fetch semester data for the curriculum
    semesters = get_semesters_list(SEMESTERS_API_URL, curriculum_key)
    course_data = {
        semester["id"]: {**semester, "courses": []} for semester in semesters
    }

    # Phase 2: Fetch course data for the curriculum (using pagination)
    courses = get_courses_list(COURSES_API_URL, curriculum_key)

    # Phase 3: Aggregate course data under semesters while generating system data
    for item in courses:
        semester_id = item.get("semester_id")

        # Use relative URLs for course links
        item["urls"]["view"] = item["urls"]["view"].replace(
            "https://www.ce.pdn.ac.lk/", "/"
        )

        # Assign a custom color code based on the course code prefix
        item["color_code"] = course_color_codes.get(
            item["code"][0:2], "btn-outline-secondary"
        )
        course_data[semester_id]["courses"].append(item)

    # Phase 4: Save the aggregated data to a JSON file in the data directory
    output_file = DIRECTORY.format(curriculum_key)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(course_data, f, indent=2)

    print(f"Data for curriculum {curriculum_name} saved to {output_file}")

    # Phase 5: Generate Course Pages
    create_new_course_pages(course_data)
