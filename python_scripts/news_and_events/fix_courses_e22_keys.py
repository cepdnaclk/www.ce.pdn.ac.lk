import json
import os

# Paths
semesters_path = os.path.join('..', '..', '_data', 'Semesters_from_e22.json')
courses_e22_path = os.path.join('..', '..', '_data', 'courses_e22.json')
output_path = os.path.join('..', '..', '_data', 'courses_e22_fixed.json')

# Load semester keys
with open(semesters_path, encoding='utf-8') as f:
    semesters = json.load(f)

# Load courses_e22 data
with open(courses_e22_path, encoding='utf-8') as f:
    courses_e22 = json.load(f)

# Build new dict with correct keys
fixed = {}
for key in semesters.keys():
    lookup = key.lower()
    if lookup in courses_e22:
        fixed[key] = courses_e22[lookup]
    else:
        print(f'Warning: No data for key {key} (looked for {lookup})')

# Write output
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(fixed, f, indent=2, ensure_ascii=False)

print(f'Wrote fixed courses_e22 to {output_path}') 