"""
Author: E/18/227 Dinuka Mudalige - e18227@eng.pdn.ac.lk

- This script will read the data files and create html files for each course. 
- This will be a daily process, run as a Cron job

"""

from importlib.resources import contents
import os
import json
import shutil

# Delete the existing folder
dir_path = "../../pages/courses/undergraduate/"
try:
    shutil.rmtree(dir_path)
except:
    print("Error: Courses Folder Not Found!")


# Get the list of Semesters
semesters = json.load(open("../../_data/semesters.json"))
courses = json.load(open("../../_data/courses.json"))
for semester in semesters:
    dataInJSON = courses[semester]["courses"]
    print("- " + courses[semester]["title"] + " -\n")

    for thisCourse in dataInJSON:
        # print(thisCourse)

        course_code = thisCourse["code"]
        # print(course_code)
        # course_title = thisCourse["name"]
        # course_credits = thisCourse["credits"]
        # type = thisCourse["type"]
        prerequisties = (
            thisCourse["prerequisites"] if "prerequisites" in thisCourse else "NULL"
        )
        # content = thisCourse["content"]
        # objectives = thisCourse["objectives"]
        # ilos_knowledge = thisCourse["ILOs"]["Knowledge"]
        # ilos_skill = thisCourse["ILOs"]["Skill"]
        # ilos_attitude = thisCourse["ILOs"]["Attitude"]

        modules = thisCourse["modules"]
        marks = thisCourse["marks"]
        statistics = thisCourse["statistics"]

        pageURL = thisCourse["urls"]["view"]
        gh_page = "https://github.com/cepdnaclk/ce.pdn.ac.lk/tree/main{0}".format(
            thisCourse["urls"]["edit"]
        )
        last_edit = thisCourse["last_edit"].split(" ")[0]

        outputString = f"""---
layout: course
permalink: "{ pageURL }"

title: {thisCourse["code"].upper()} {thisCourse["name"]}
semester: {semester}
course_code : {thisCourse["code"].upper()} 
course_title : {thisCourse["name"]}

credits : {thisCourse["credits"]}
type : {thisCourse["type"]} 

prerequisites : {prerequisties}
aims_and_objectives: {thisCourse["objectives"]}
ilos_knowledge : {thisCourse["ILOs"]["Knowledge"]}
ilos_skill : {thisCourse["ILOs"]["Skill"]}
ilos_attitude : {thisCourse["ILOs"]["Attitude"]}

modules: {thisCourse["modules"]}
textbooks_references : {thisCourse["references"]}

marks: {marks}
statistics: {statistics}

last_edit: {last_edit}
gh_page: {gh_page}
faq_page: {thisCourse["urls"]["faq_page"]}

---"""

        # Write into a file
        file_url = (
            f"../../pages/courses/undergraduate/{semester}/{course_code.upper()}.html"
        )
        os.makedirs(os.path.dirname(file_url), exist_ok=True)
        htmlFile = open(file_url, "w")
        htmlFile.write(outputString)
        htmlFile.close()
        print("Generated: " + course_code.upper() + ".html")

    print("")


print("Course page generation completed !")
print("--------------------------------")
