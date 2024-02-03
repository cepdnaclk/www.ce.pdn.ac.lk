"""
Author: E/18/227 Dinuka Mudalige - e18227@eng.pdn.ac.lk

- This script will read the data files and create html files for each semester. 
- This will be a daily process, run as a Cron job

"""

from importlib.resources import contents
import os
import json
import shutil

# Delete the existing folder
dir_path = "../../pages/semesters/"
try:
    shutil.rmtree(dir_path)
except:
    print("Error: Semesters Folder Not Found!")


# Get the list of Semesters
semesters = json.load(open("../../_data/semesters.json"))

for semester in semesters:
    title = semesters[semester]["title"]
    description = semesters[semester]["description"]
    url = semesters[semester]["url"]

    outputString = f"""---
layout: semester
permalink: "/courses/undergraduate{ url }"

title: {title}
code: {semester}
description: {description}
---"""

    # Write into a file
    file_url = f"../../pages/courses/semesters/{semester}.html"
    os.makedirs(os.path.dirname(file_url), exist_ok=True)
    htmlFile = open(file_url, "w")
    htmlFile.write(outputString)
    htmlFile.close()
    print("Generated: " + semester + ".html")


print("Semester page generation completed !")
print("--------------------------------")
