import os
import json
import pandas as pd

blocked_substrings = ["merged"]


def substring_check(s, subs): return not any(sub in s.lower() for sub in subs)


path_to_json = '././output/'
json_files = [json_file for json_file in os.listdir(
    path_to_json) if (json_file.endswith('.json') and  substring_check(json_file, blocked_substrings))]

json_array = []
total = 0

for file in json_files:
    print(file)
    with open(path_to_json+file) as f:
        data = json.load(f)
        if isinstance(data, list):
            json_array.extend(data)

with open(path_to_json+'merged.json', 'w') as f:
    json.dump(json_array, f, indent=4)
