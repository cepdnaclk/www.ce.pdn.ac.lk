import json
import os

import requests

# Where the API is available
apiIndex = "https://api.ce.pdn.ac.lk/publications/v1"

r = requests.get("{0}/all".format(apiIndex), timeout=30)

# Fetch data from the api.ce.pdn.ac.lk
if r.status_code == 200:
    data = json.loads(r.text)

    publications_all = sorted(
        data,
        key=lambda k: "{}{}".format(5000 - int(k["year"]), k["title"]),
        reverse=False,
    )

    filename = "../_data/publications.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w") as f:
        f.write(json.dumps(publications_all, indent=2))
