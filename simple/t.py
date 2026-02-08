from pathlib import Path
parent_dir = Path(__file__).resolve().parent
target_file=parent_dir/"t.txt"

with open(target_file , "w") as fw:
    fw.write("this is first line\n")
    fw.write("this is second line\n")