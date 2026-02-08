import json
from pathlib import Path
import time

# -----------------------------
# Step 1: Generator to read JSONL file
# -----------------------------
def read_jsonl(path):
    print("read_jsonl")
    r=0
    """Yield one record (dict) at a time from a JSONL file."""
    with open(path, "r") as f:
        for line in f:
            print("inside read_jsonl loop")
            yield json.loads(line)   # deserialize each line
            r=r+1
            print(f"read_jsonl --> {r}")

# -----------------------------
# Step 2: Generator to transform records
# -----------------------------
def transform(records):
    """Apply transformations lazily to each record."""
    print("transform")
    t=0
    for r in records:
        print("inside transform loop")
        # Example transformation: normalize name and add pass/fail
        r["name"] = r["name"].title()
        r["status"] = "Pass" if r["marks"] >= 80 else "Fail"
        yield r
        t=t+1
        print(f"transform --> {t}")

# -----------------------------
# Step 3: Generator to filter records
# -----------------------------
def filter_records(records):
    print("filter_records")
    f=0
    """Filter only students who passed."""
    for r in records:
        print("inside filter loop")
        if r["status"] == "Pass":
            yield r
        f=f+1
        print(f"filter_records --> {f}")

# -----------------------------
# Step 4: Write results back to JSONL
# -----------------------------
def write_jsonl(path, filtered_records):
    """Write records back to JSONL file."""
    with open(path, "w") as f:
        for r in filtered_records:
            f.write(json.dumps(r) + "\n")
            print(f"Written record {r['id']} → pausing for 1 seconds...")
            time.sleep(1)   # pause execution for 60 seconds

# -----------------------------
# Step 5: Putting it all together
# -----------------------------
if __name__ == "__main__":
    parent_dir = Path(__file__).resolve().parent
    source_file = parent_dir / "stud.jsonl"
    target_file = parent_dir / "cleaned.jsonl"

    # Build pipeline: read → transform → filter → write
    records = read_jsonl(source_file)
    transformed = transform(records)
    filtered = filter_records(transformed)
    write_jsonl(target_file, filtered)

    print("ETL pipeline completed successfully!")