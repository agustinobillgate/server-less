import os

# Define the directory to search
directory = f"D:/docker/pixcdk/image/src/functions/"

# Define the version threshold
threshold_version = [1, 0, 0, 27]

# File to save results
output_file = "./lower_version_files.txt"

# Function to compare versions
def is_version_lower(version_line, threshold):
    try:
        # Extract the version number from the line
        version_str = version_line.split("version:")[-1].strip()
        version_parts = list(map(int, version_str.split(".")))
        return version_parts < threshold
    except Exception as e:
        return False  # If parsing fails, consider it invalid

# List to store files with lower versions
files_with_lower_versions = []

# Walk through files in the directory
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.startswith("__"):
            continue
        file_path = os.path.join(root, file)
        try:
            # Check the first line of the file
            with open(file_path, "r") as f:
                first_line = f.readline().strip()
                if "#using conversion tools version:" in first_line:
                    if is_version_lower(first_line, threshold_version):
                        files_with_lower_versions.append(file_path)
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")

# Save results to a txt file
with open(output_file, "w") as output:
    output.write("\n".join(files_with_lower_versions))

print(f"Files with lower versions saved to {output_file}")
