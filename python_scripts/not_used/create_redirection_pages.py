## Author: E/18/098 Ishan Fernando - e18098@eng.pdn.ac.lk

# import csv

# # Read the CSV file
# csv_file_path = 'data.csv'  # Replace with your actual CSV file path
# with open(csv_file_path, 'r') as csv_file:
#     csv_reader = csv.reader(csv_file)
#     next(csv_reader)  # Skip header row
#     for row in csv_reader:
#         old_url, new_url = row

#         # Create a new file for each row
#         new_file_path = f'{old_url[1:].replace("/","-").replace("html","").replace(".","").lower()}.md'
#         with open(new_file_path, 'w') as new_file:
#             new_file.write(f'---\n')
#             new_file.write(f'layout: redirect\n')
#             new_file.write(f'permalink: {old_url}\n')
#             new_file.write(f'forward_url: {new_url}\n')
#             new_file.write(f'---\n')

# print("Conversion completed successfully.")

string1 = "redirections/academic-staff-asitha-bandaranayake-.md redirections/academic-staff-d-s-deegalla-.md redirections/academic-staff-damayanthi-herath-.md redirections/academic-staff-dhammika-elkaduwe-.md redirections/academic-staff-isuru-nawinne-.md redirections/academic-staff-janaka-alawatugoda-.md redirections/academic-staff-kamalanath-samarakoon-.md redirections/academic-staff-manjula-sandirigama-.md redirections/academic-staff-roshan-g-ragel-.md redirections/academic-staff-shirley-devapriya-dewasurendra-.md redirections/academic-staff-suneth-namal-karunarathna-.md redirections/academic-staff-swarnalatha-radhakrishnan-.md"

import os
for each in string1.split(" "):
    each = each.replace("redirections/","")
    os.system(f"mv {each} {each[0:-4]}.md")