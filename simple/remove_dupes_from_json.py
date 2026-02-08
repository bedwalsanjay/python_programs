# remove duplicate lines from the file and save it back
import json
import os

file_path = r"C:\Users\Sanjay Bedwal\Desktop\repos\python_programs\leetcode\stud.jsonl"

# Detect file type by extension
ext = os.path.splitext(file_path)[1].lower()

if ext == ".jsonl":
    # JSONL → process line by line
    seen = set()
    unique_lines = []
    with open(file_path, "r") as f:
        for line in f:
            if line not in seen:
                seen.add(line)
                unique_lines.append(line)

    with open(file_path, "w") as f:
        f.writelines(unique_lines)

    print("Duplicates removed from JSONL file successfully!")

elif ext == ".json":
    # JSON → load entire array and deduplicate objects
    with open(file_path, "r") as f:
        data = json.load(f)   # list of dicts

    # unique_data = [dict(t) for t in {tuple(d.items()) for d in data}]

    # Step 1: convert each dict into a tuple of items (so it's hashable)
    tuples = []
    for d in data:
        tuples.append(tuple(d.items()))

    # Step 2: put those tuples into a set to remove duplicates
    unique_tuples = set(tuples)

    # Step 3: convert each tuple back into a dict
    unique_data = []
    for t in unique_tuples:
        unique_data.append(dict(t))

    # Step 4: save back to JSON
    with open(file_path, "w") as f:
        json.dump(unique_data, f, indent=2)

    print("Duplicates removed successfully!")
    print(unique_data)

else:
    print("Unsupported file type:", ext)
#---------------
import json

file_path = r"C:\Users\Sanjay Bedwal\Desktop\repos\python_programs\leetcode\stud.jsonl"

# Read all lines
with open(file_path, "r") as f:
    lines = f.readlines()

# Remove duplicates while preserving order
unique_lines = list(dict.fromkeys(lines))

# Save back
with open(file_path, "w") as f:
    f.writelines(unique_lines)

print("Duplicates removed successfully!")
