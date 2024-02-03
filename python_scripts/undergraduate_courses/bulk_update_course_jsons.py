'''
Author: Nuwan Jaliyagoda

- This script can be used to bulk update the JSON files under './courses/' directory.
- Can be used to post-process the JSON files manually

'''

import json 
import os

# Get the list of semesters 
semesterList = json.load(open("../_data/semesters.json"))

for semester in semesterList:
    print(semester)
    semester_info = semesterList[semester]
    semester_dir = "../courses/{0}".format(semester)

    # Scan through each semester folder to get the courses under that semester
    if os.path.isdir(semester_dir):
        semester_courses = []
        for course in os.listdir(semester_dir):
            print('\t', course)

            # Read the file
            course_file = "../courses/{0}/{1}".format(semester, course)
            course_data = json.load(open(course_file))
            
            # TODO: Changes --------------






            # ----------------------------

            # Save the file
            with open(course_file, "w") as f:
                f.write(json.dumps(course_data, indent = 4))

    else:
        print("\t ERROR: {0} directory not exists".format(semester_dir))
