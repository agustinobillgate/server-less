import os

all_modules_file = "./all_modules.txt"
excl_lock_file = "./excl-lock.txt"
output_file = "./excl-lock-paired.txt"

# Load mappings from all_modules.txt
# Format: endpoint,function
module_map = {}
with open(all_modules_file, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or "," not in line:
            continue
        endpoint, func = line.split(",", 1)

        func_norm = func.lower().replace(".py", "")
        module_map[func_norm] = endpoint

# Load excl-lock filenames
excl_files = []
with open(excl_lock_file, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            excl_files.append(line)

# Produce output
output_lines = []
for pyfile in excl_files:
    norm = pyfile.lower().replace(".py", "")

    # direct match
    endpoint = module_map.get(norm)

    # fuzzy match if direct not found
    if not endpoint:
        for func_key, ep in module_map.items():
            if func_key.startswith(norm) or norm.startswith(func_key):
                endpoint = ep
                break

    # write result
    if endpoint:
        output_lines.append(f"{endpoint}, {pyfile.lower()} ")
    else:
        pass
        # output_lines.append(f"{pyfile}, NOT_FOUND")

# Save output
output_lines.sort()
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join([line for line in output_lines]))

print("Done! Output saved to:", output_file)