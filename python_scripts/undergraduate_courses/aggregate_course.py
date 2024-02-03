"""
Author: Nuwan Jaliyagoda

- This script will collect all the JSON files in the directory '/courses', post-process and write into the
single JSON file, './_data/courses.json'. 
- Any validation to the JSON content can be done in this step.

"""

import json
import os
import subprocess
import hashlib
from datetime import datetime


def dict_hash(dictionary):
    dhash = hashlib.md5()
    encoded = json.dumps(dictionary, sort_keys=True).encode()
    dhash.update(encoded)
    return dhash.hexdigest()


# Get the list of semesters
semesterList = json.load(open("../../_data/semesters.json"))
courses = {}
courses_index = {}

base_path = "structured_data/undergraduate_courses"

courses_existing = json.load(open("../../_data/courses_index.json"))

for semester in semesterList:
    print(semester)
    semester_info = semesterList[semester]
    semester_dir = "../../{0}/{1}".format(base_path, semester)

    # Scan through each semester folder to get the courses under that semester
    if os.path.isdir(semester_dir):
        semester_courses = []
        for course in os.listdir(semester_dir):
            print("\t", course)

            # try:
            course_file = "../../{0}/{1}/{2}".format(base_path, semester, course)
            print(course_file)
            course_data = json.load(open(course_file))

            course_code = course.replace(".json", "")
            course_data["urls"] = {
                "edit": f"/{base_path}/{semester}/{course_code}.json",
                "view": f"/courses/undergraduate/{semester}/{course_code}/",
                "markdown": f"/pages/courses/undergraduate/{semester}/{course_code}",
                "faq_page": course_data["faq_page"],
            }

            # TODO: Post-process Lecturer and Instructor details with info available at api.ce.pdn.ac.lk

            # Changes and only update the `last_edit` if there any new difference
            current_course = courses_existing[course_code]

            # Remove the last edit info before compare
            if "last_edit" in current_course:
                last_edit_prev = current_course.pop("last_edit")
            else:
                last_edit_prev = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            hash_currentCourse = dict_hash(current_course)
            hash_newCourse = dict_hash(course_data)

            if hash_currentCourse != hash_newCourse:
                # The course details were changed
                course_data["last_edit"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            else:
                # There isn't any change happened
                course_data["last_edit"] = last_edit_prev

            semester_courses.append(course_data)
            courses_index[course_code] = course_data

            # except Exception as err:
            #     print("ERROR:", err)

        semester_courses.sort(key=lambda e: e["code"])

        courses[semester] = {
            "title": semester_info["title"],
            "description": semester_info["description"],
            "courses": semester_courses,
        }
    else:
        print("\t ERROR: {0} directory not exists".format(semester_dir))


# Write the courses.json file
filename = "../../_data/courses.json"
os.makedirs(os.path.dirname(filename), exist_ok=True)
with open(filename, "w") as f:
    f.write(json.dumps(courses, indent=4))

# Sort the course_index
sorted_course_index = {}
for key in sorted(courses_index):
    sorted_course_index[key] = courses_index[key]

# Write the courses_index.json file
filename = "../../_data/courses_index.json"
os.makedirs(os.path.dirname(filename), exist_ok=True)
with open(filename, "w") as f:
    f.write(json.dumps(sorted_course_index, indent=4))
