import os, subprocess
from datetime import datetime, timedelta
import psycopg2


# Get current timestamp
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
conn = psycopg2.connect(
    # host = "vhp-devtest.cjxtrsmbui3n.ap-southeast-1.rds.amazonaws.com",
    # database = "vhptools",
    # user = "vhpadmin",
    # password = "bFdq8QsQoxH1vAvO"
    # host = "localhost",
    # database = "vhptools",
    # user = "postgres",
    # password = "bali2000"
    host = "psql.staging.e1-vhp.com",
    database = "vhptools",
    user = "postgres",
    password = "DevPostgreSQL#2024",

)

# Create a cursor object
cursor = conn.cursor()

def get_content_file(file_path):
    """
    Reads the content of a file and returns it as a string.

    :param file_path: Path to the file to be read.
    :return: Content of the file as a string.
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return ""
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}")
        return ""
    
def get_file_extensions(root_folder):
    # Set to store unique extensions
    extensions = set()

    # Walk through the directory and get all file extensions
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            # Extract the file extension and add to the set
            _, ext = os.path.splitext(filename)
            if ext:  # Only consider files with extensions
                extensions.add(ext.lower())  # Convert to lowercase for consistency

    return extensions

def gen_folder_summary(root_folder):
    curdir = os.getcwd()
    root_folder_len = len(root_folder)
    os.chdir("/usr1/vhp_gittools/tmp_git_pull")
    extensions = get_file_extensions(root_folder)
    # print(f"Found extensions: {extensions}")
    
    content = ""
    # Append the generated timestamp and file counts to the content
    content += f"Generated on: {timestamp}\n"
    content += "---------------------------------------------\n"

    extension_counts = {}
    for ext in extensions:
        count = len([f for f in subprocess.check_output(["find", root_folder, "-type", "f", "-name", f"*{ext}"]).decode().splitlines()])
        extension_counts[ext] = count

    # Output results
    for ext, count in extension_counts.items():
        # print(f"Number of {ext} files: {count}")
        content += f"Number of  {ext} files: {count}\n"


    # Start directory structure section
    content += f"\nDirectory Structure and File Info for {root_folder}:\n"

    # List to hold directory name, file count, last updated file, and last updated timestamp
    directory_info = []

    # For directories, list their names with the number of files in them
    for dirpath, dirnames, filenames in os.walk(root_folder):
        # Exclude the base directory itself
        if dirpath == root_folder:
            continue
        # Count the number of files in the current directory
        file_count = len(filenames)

        # Get the most recently modified file and its timestamp
        if filenames:
            latest_file = max(filenames, key=lambda file: os.path.getmtime(os.path.join(dirpath, file)))
            latest_time = os.path.getmtime(os.path.join(dirpath, latest_file))
            latest_time_str = datetime.fromtimestamp(latest_time).strftime("%Y-%m-%d %H:%M:%S")
        else:
            latest_file = "N/A"
            latest_time_str = "N/A"

        # Remove './Master' prefix from the directory path
        dir_name = dirpath[root_folder_len:]  # Remove './Master' (8 characters)
        directory_info.append((dir_name, file_count, latest_file, latest_time_str))

    # Sort the directories by folder name (alphabetically)
    directory_info.sort(key=lambda x: x[0])  # Sort by directory name (first element)

    # Write the sorted directory info to the content
    for dir_name, file_count, latest_file, latest_time_str in directory_info:
        content += f"{dir_name} ({file_count} files, {latest_file}  {latest_time_str})\n"

    # Output the content to a text file
    # with open(f"summary_{root_folder}.txt", 'w') as f:
    #     f.write(content)

    os.chdir(curdir)
    return content

def gen_updated_files_summary(root_folder, nhari):
    curdir = os.getcwd()
    root_folder_len = len(root_folder)
    os.chdir("/usr1/vhp_gittools/tmp_git_pull")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Calculate the time for 7 days ago
    seven_days_ago = datetime.now() - timedelta(days=nhari)

    content = ""

    # Append the generated timestamp to the content
    content += f"Generated on: {timestamp}\n"
    content += "---------------------------------------------\n"
    content += f"Files updated in the last {nhari} days:\n"

    # List to hold directory name and the updated files in them
    directory_info = []

    # For directories, list their names and the files that have been updated in the last nHari days
    for dirpath, dirnames, filenames in os.walk(root_folder):
        # Exclude the base directory itself
        if dirpath == root_folder:
            continue

        # List to hold updated files in the current directory
        updated_files = []

        # Check each file in the current directory
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            last_modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))

            # If the file was updated in the last 7 days, add it to the list
            if last_modified_time >= seven_days_ago:
                updated_files.append((filename, last_modified_time))

        # If there are any updated files, add the directory info to the list
        if updated_files:
            # Remove './Master' prefix from the directory path
            dir_name = dirpath[root_folder_len:]  # Remove './Master' (8 characters)
            directory_info.append((dir_name, updated_files))

    # Sort the directories by folder name (alphabetically)
    directory_info.sort(key=lambda x: x[0])  # Sort by directory name (first element)

    # Append the sorted directory info and updated files to the content
    for dir_name, updated_files in directory_info:
        content += f"\n{dir_name}:\n"
        # Sort updated files by timestamp (latest first) for each directory
        updated_files.sort(key=lambda x: x[1], reverse=True)  # Sort by timestamp (latest first)
        for filename, last_modified_time in updated_files:
            content += f"  {filename} ({last_modified_time.strftime('%Y-%m-%d %H:%M:%S')})\n"

    # Output the content to a text file
    # with open(f"updated_file_{root_folder}.txt", 'w') as f:
    #     f.write(content)

    os.chdir(curdir)
    return content

def fetch_child_modules(cursor, parent_nr):
    query = """
    SELECT id, modul_name, p_nr
    FROM p_trees
    WHERE parent_nr = %s
    ORDER BY id;
    """
    cursor.execute(query, (parent_nr,))
    return cursor.fetchall()

def print_modules_to_string(cursor, parent_nr=0, level=0, result=""):
    # Fetch top-level or child modules based on parent_nr
    modules = fetch_child_modules(cursor, parent_nr)

    # Iterate through the modules and append to the result string
    for module in modules:
        id, modul_name, p_nr = module
        result += f"{'   ' * level}|-{modul_name} (ID: {p_nr})\n"

        # Recursively fetch and append the child modules to result
        result = print_modules_to_string(cursor, p_nr, level + 1, result)

    return result


# ----------------------------------------------------------
# generate tree .p
# ----------------------------------------------------------
page_name = "TREE_DOTP"
content = f"Modules Tree Structure ({timestamp}):\n"
content += "---------------------------------------------\n"
content += print_modules_to_string(cursor)
insert_query = """
    INSERT INTO page_summary (page_name, page_content)
    VALUES (%s, %s)
    ON CONFLICT (page_name) 
    DO UPDATE SET page_content = EXCLUDED.page_content;
    """
# Execute the insert query with the page_name and content
cursor.execute(insert_query, (page_name, content))
conn.commit()
print(page_name, "inserted into the database successfully.")


# # ----------------------------------------------------------
# # dotP insert the content into the page_summary table
# # ----------------------------------------------------------
# page_name = 'PAGE_SUMMARY_P'
# root_folder = "./Master"
# content = gen_folder_summary(root_folder)
# # SQL query to insert the summary
# insert_query = """
#     INSERT INTO page_summary (page_name, page_content)
#         VALUES (%s, %s)
#         ON CONFLICT (page_name) 
#         DO UPDATE SET page_content = EXCLUDED.page_content;
#     """
# # Execute the insert query with the page_name and content
# cursor.execute(insert_query, (page_name, content))
# conn.commit()
# print(page_name, "inserted into the database successfully.")

# # ----------------------------------------------------------
# # dotR insert the content into the page_summary table
# # ----------------------------------------------------------
# page_name = 'PAGE_SUMMARY_R'
# root_folder = "./Compiled"
# content = gen_folder_summary(root_folder)
# # SQL query to insert the summary
# insert_query = """
#     INSERT INTO page_summary (page_name, page_content)
#         VALUES (%s, %s)
#         ON CONFLICT (page_name) 
#         DO UPDATE SET page_content = EXCLUDED.page_content;
#     """
# # Execute the insert query with the page_name and content
# cursor.execute(insert_query, (page_name, content))
# conn.commit()
# print(page_name, "inserted into the database successfully.")

# # ----------------------------------------------------------
# # generate list updated file 7days
# # ----------------------------------------------------------
# page_name = "FILEUPDATE_7DAYS_P"
# root_folder = "./Master"
# content = gen_updated_files_summary(root_folder, 7)
# insert_query = """
#     INSERT INTO page_summary (page_name, page_content)
# VALUES (%s, %s)
# ON CONFLICT (page_name) 
# DO UPDATE SET page_content = EXCLUDED.page_content;
# """
# # Execute the insert query with the page_name and content
# cursor.execute(insert_query, (page_name, content))
# conn.commit()
# print(page_name, "inserted into the database successfully.")


# # ----------------------------------------------------------
# # dotR generate list updated file 7days
# # ----------------------------------------------------------
# page_name = "FILEUPDATE_7DAYS_R"
# root_folder = "./Compiled"
# content = gen_updated_files_summary(root_folder, 7)
# insert_query = """
#     INSERT INTO page_summary (page_name, page_content)
# VALUES (%s, %s)
# ON CONFLICT (page_name) 
# DO UPDATE SET page_content = EXCLUDED.page_content;
# """
# # Execute the insert query with the page_name and content
# cursor.execute(insert_query, (page_name, content))
# conn.commit()
# print(page_name, "inserted into the database successfully.")

# # ----------------------------------------------------------


# # ----------------------------------------------------------
# # update page Last_git_pull
# # ----------------------------------------------------------
# page_name = "LAST_GIT_PULL"
# file_git = "last_git_pull.txt"
# content = get_content_file(file_git).replace("<br>", "\n")
# insert_query = """
#     INSERT INTO page_summary (page_name, page_content)
# VALUES (%s, %s)
# ON CONFLICT (page_name) 
# DO UPDATE SET page_content = EXCLUDED.page_content;
# """
# # Execute the insert query with the page_name and content
# cursor.execute(insert_query, (page_name, content))
# conn.commit()
# print(page_name, content,  "inserted into the database successfully.")

# # ----------------------------------------------------------

cursor.close()
conn.close()