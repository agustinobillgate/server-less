import os
import shutil
import Levenshtein

# Paths
source_folder = r"D:\docker\app_konversi\input\vhp-master-source\Master"
destination_folder = r"D:\docker\app_konversi\input\vhp-serverless\image\src\output\check-p-files2"
file_list_path = r".\lower_version_files.txt"

# Ensure destination folder exists
os.makedirs(destination_folder, exist_ok=True)

# Function to convert file names
def convert_file_name(file_name):
    # Replace underscores with hyphens and change extension to .p
    base_name = os.path.basename(file_name)
    return base_name.replace("_", "-").replace(".py", ".p")

# Function to find a file by similarity
def find_similar_file(source_root, target_file):
    threshold = 0.8  # Similarity threshold, higher means stricter match (1 = identical)
    similar_file = None
    for root, _, files in os.walk(source_root):
        for file in files:
            # Compare Levenshtein distance
            similarity = Levenshtein.ratio(file.lower(), target_file.lower())
            if similarity >= threshold:
                similar_file = os.path.join(root, file)
                print(f"Similar match found: {similar_file} with similarity {similarity:.2f}")
                break
        if similar_file:
            break
    return similar_file

# Read file paths from the text file
try:
    with open(file_list_path, "r") as f:
        files_to_process = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print(f"File not found: {file_list_path}")
    files_to_process = []

# Process each file
for file_path in files_to_process:
    # Convert file name
    new_file_name = convert_file_name(file_path)
    
    # Search for similar files in the source folder and its subfolders
    source_file = find_similar_file(source_folder, new_file_name)
    
    if source_file:
        destination_file = os.path.join(destination_folder, new_file_name)
        try:
            # Copy file to destination
            shutil.copy2(source_file, destination_file)
            print(f"Copied: {source_file} -> {destination_file}")
        except Exception as e:
            print(f"Error copying file {file_path}: {e}")
    else:
        print(f"File not found in source folder or subfolders: {new_file_name}")
