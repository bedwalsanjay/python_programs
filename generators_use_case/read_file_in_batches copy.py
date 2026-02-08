# read records from a JSONL file, batch them into groups of N, and then write each batch out with a pause after writing.
import json
import time
from pathlib import Path

# -----------------------------
# Step 1: Generator to read JSONL file
# -----------------------------
def read_jsonl(path):
    """Yield one record (dict) at a time from a JSONL file."""
    with open(path, "r") as f:
        for line in f:
            yield json.loads(line)

# -----------------------------
# Step 2: Batcher generator
# -----------------------------
def batcher(iterable, size):
    """Yield records in batches of given size."""
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch

# -----------------------------
# Step 3: Writer with pause
# -----------------------------
def write_batches(path, batches, pause=60):
    """Write batches to file, pausing after each batch."""
    with open(path, "w") as f:
        for batch in batches:
            for r in batch:
                f.write(json.dumps(r) + "\n")
            print(f"Written batch of {len(batch)} records → pausing {pause} seconds...")
            time.sleep(pause)

# -----------------------------
# Step 4: Putting it all together
# -----------------------------
if __name__ == "__main__":
    parent_dir = Path(__file__).resolve().parent
    source_file = parent_dir / "stud.jsonl"
    target_file = parent_dir / "batched.jsonl"

    # Build pipeline: read → batch → write
    records = read_jsonl(source_file)
    batches = batcher(records, size=2)   # example: batches of 2 records
    write_batches(target_file, batches, pause=60)

    print("Batch ETL pipeline completed successfully!")