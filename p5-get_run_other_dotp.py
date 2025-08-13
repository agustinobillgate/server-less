

import os
import re
import psycopg2
from psycopg2 import sql

# Function to extract filenames from RUN statements
def extract_run_files(file_path):
    pattern = re.compile(r'RUN\s+([^\s]+\.p)', re.IGNORECASE)
    run_files = set()  # Use a set to avoid duplicate filenames
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()
            for line in lines:
                matches = pattern.findall(line)
                for match in matches:
                    run_files.add(match)  # Add filenames in lowercase
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    
    return run_files

# Function to update the next_p field in the database
def update_next_p(cursor, p_nr, next_p_content):
    try:
        cursor.execute("""
            UPDATE p_files
            SET next_p = %s
            WHERE p_nr = %s
        """, (next_p_content, p_nr))
    except Exception as e:
        print(f"Error updating p_nr {p_nr}: {e}")


def fill_mention_in():
    print("Update Mention in...")
    sql = "update p_files set mention_in = '';"
    cursor.execute(sql)
    sql = """
            WITH mentions AS (
                SELECT p1.p_filename AS mentioned_file,
                    p2.p_filename AS referencing_file
                FROM p_files p1
                JOIN p_files p2
                ON p2.next_p LIKE '%' || p1.p_filename || '%' -- Search for the p_filename in the next_p field
            )
            UPDATE p_files
            SET mention_in = (
                SELECT STRING_AGG(referencing_file, E',') 
                FROM mentions 
                WHERE mentioned_file = p_files.p_filename
            )
            WHERE p_files.p_filename IN (SELECT mentioned_file FROM mentions);
            """
    cursor.execute(sql)

    # remove myown name in mention_in, to avoid infinite loop tree
    sql = """UPDATE p_files
            SET next_p = REPLACE(next_p, p_filename, '')
            WHERE next_p LIKE '%' || p_filename || '%';
            """
    cursor.execute(sql) 
    sql = """UPDATE p_files
            SET mention_in = REPLACE(mention_in, p_filename, '')
            WHERE mention_in LIKE '%' || p_filename || '%';"""
    cursor.execute(sql) 
    

# Connect to the PostgreSQL database
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
cursor = conn.cursor()
folder_path = f"D:/VHP-Projects/vhp-master-source/Master"

# folder_p = f"D:/VHP-Projects/vhp-master-source/Master"
# folder_path = r"/usr1/vhp_gittools/tmp_git_pull/Master"

try:
    print("Reset next_p...")
    sql = "update p_files set mention_in='', next_p = '';"
    cursor.execute(sql)

    # Fetch all .p files from the database
    cursor.execute("SELECT p_nr, p_filename, p_path FROM p_files  ORDER BY p_nr")
    files = cursor.fetchall()
    
    print("Start Searching...")
    nfiles = 0
    for p_nr, p_filename, p_path in files:
        path_only = os.path.dirname(p_path)
        if path_only.lower().endswith('ui'):
            continue
        nfiles = nfiles + 1
        # Extract filenames from RUN statements
        run_files = extract_run_files(p_path)
        
        # Prepare the content for next_p field
        next_p_content = ','.join(run_files)
        print(nfiles, p_filename, next_p_content)
        
        # Update the next_p field in the database
        update_next_p(cursor, p_nr, next_p_content)
        conn.commit()
    
    # Commit the changes to the database
    conn.commit()

    try:
        fill_mention_in()
    except Exception as e:
        print(f"Error updating mention_in: {e}")
    finally:
        conn.commit()

finally:
    cursor.close()
    conn.close()


#------------------------
"""
WITH mentions AS (
    SELECT p1.p_filename AS mentioned_file,
           p2.p_filename AS referencing_file
    FROM p_files p1
    JOIN p_files p2
    ON p2.next_p ILIKE '%' || p1.p_filename || '%' 
)
UPDATE p_files
SET mention_in = (
    SELECT STRING_AGG(referencing_file, E',') 
    FROM mentions 
    WHERE mentioned_file = p_files.p_filename
)
WHERE p_files.p_filename IN (SELECT mentioned_file FROM mentions);
"""