import requests
import psycopg2
from psycopg2.extras import execute_values, execute_batch
import time, json, os
from dotenv import load_dotenv

global n_dotp, n_dotr
load_dotenv()

n_dotp = n_dotr = n_xml = 0
def create_tables(connection):
    """
    Create the necessary tables for storing GitLab commit and file data.
    """
    with connection.cursor() as cursor:
        # Create gitlab_commits table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gitlab_commits (
                recid  SERIAL PRIMARY KEY,
                id CHAR(40) ,             -- Commit ID (SHA-1 hash)
                filename VARCHAR(255),
                title TEXT,                          -- Title of the commit
                message TEXT,                        -- Commit message
                author_name VARCHAR(255),            -- Name of the author
                author_email VARCHAR(255),           -- Email of the author
                authored_date TIMESTAMP,             -- Date and time the commit was authored
                committer_name VARCHAR(255),         -- Name of the committer
                committer_email VARCHAR(255),        -- Email of the committer
                committed_date TIMESTAMP,            -- Date and time the commit was committed
                web_url TEXT,                        -- Web URL to view the commit
                additions INT,                       -- Number of additions in the commit
                deletions INT,                       -- Number of deletions in the commit
                total_changes INT,                   -- Total number of changes (additions + deletions)
                status VARCHAR(50),                  -- Commit status (can be NULL)
                project_id VARCHAR(15),                
                commit_diff TEXT,                  -- Key for commit differences
                UNIQUE (id, filename)
                
            );
        """)

        # Commit the changes
        connection.commit()

def store_commit_data(commit, project_id, connection):
    global n_dotp, n_dotr
    """
    Store commit and file data into gitlab_commits and gitlab_files tables.
     "id": "83398480d43158071662eeffd830e947b238a1a0",
    "title": "Merge branch 'Dev-Rulita' into 'develop'",
    "message": "Merge branch 'Dev-Rulita' into 'develop'\n\nRulita 140125| Fixing serverless issue git 190\n\nSee merge request VHPGitDev/vhp-master-source!2076",
    "author_name": "Muflih Fadly",
    "author_email": "fadly@sindata.net",
    "authored_date": "2025-01-15T00:50:39.000+00:00",
    "committer_name": "Muflih Fadly",
    "committer_email": "fadly@sindata.net",
    "committed_date": "2025-01-15T00:50:39.000+00:00",
    "web_url": "https://gitlab.com/VHPGitDev/vhp-master-source/-/commit/83398480d43158071662eeffd830e947b238a1a0",
    "stats": {
        "additions": 46,
        "deletions": 12,
        "total": 58
    },
    "status": null
    """

    commit_id = commit["id"]
    
    commit_diff = ""
    filename = ""
    url = f"https://gitlab.com/api/v4/projects/{project_id}/repository/commits/{commit_id}/diff"

    response = requests.request("GET", url, headers=headers, data="")
    filename = ""
    commit_diff = ""
    response_data = response.json()
    if response is not None:
        if response.status_code == 200:
            response_data = response.json()
            for diff_response in response_data:
                filename = diff_response["new_path"]
                commit_diff = diff_response["diff"]
                print(commit["committed_date"], filename)
                if filename.endswith(".p") or filename.endswith(".r") or filename.endswith(".i") or filename.endswith(".md") or filename.endswith(".txt") or filename.endswith(".xml"):
                    if filename.endswith(".p"):
                        n_dotp +=1
                    if filename.endswith(".r"):
                        n_dotr +=1

                    if filename.endswith(".xml"):
                        n_xml +=1
                        
                    with connection.cursor() as cursor:
                        # Insert into gitlab_commits
                        commit_query = """
                            INSERT INTO gitlab_commits (
                                id, filename, title, message, 
                                author_name, author_email, authored_date, 
                                committer_name, committer_email, committed_date, 
                                web_url, additions, deletions, total_changes, status, project_id, commit_diff
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (id, filename)
                            DO UPDATE SET 
                                title = EXCLUDED.title,
                                message = EXCLUDED.message,
                                author_name = EXCLUDED.author_name,
                                author_email = EXCLUDED.author_email,
                                authored_date = EXCLUDED.authored_date,
                                committer_name = EXCLUDED.committer_name,
                                committer_email = EXCLUDED.committer_email,
                                committed_date = EXCLUDED.committed_date,
                                web_url = EXCLUDED.web_url,
                                additions = EXCLUDED.additions,
                                deletions = EXCLUDED.deletions,
                                total_changes = EXCLUDED.total_changes,
                                status = EXCLUDED.status,
                                project_id = EXCLUDED.project_id,
                                commit_diff = EXCLUDED.commit_diff;
                        """
                        stats = diff_response.get("stats", {})
                        additions = stats.get("additions", 0)
                        deletions = stats.get("deletions", 0)
                        total_changes = stats.get("total", 0)
                    
                        commit_values = [
                            (
                                commit["id"],
                                filename, 
                                commit["title"], commit["message"],
                                commit["author_name"], commit["author_email"], commit["authored_date"],
                                commit["committer_name"], commit["committer_email"], commit["committed_date"],
                                commit["web_url"], 
                                additions, deletions, total_changes, 
                                commit.get("status"), 
                                project_id,
                                commit_diff
                            )
                        ]
                        
                        execute_batch(cursor, commit_query, commit_values)
                        connection.commit()

def get_all_commits(project_id, headers, connection):
    commits = []
    page = 1
    per_page = 10  # Number of results per page
    is_exists = False
    n_dotp = 0
    n_dotr = 0
    while True:
        url = f"https://gitlab.com/api/v4/projects/{project_id}/repository/commits"
        params = {"page": page, "per_page": per_page}
        print("Page:", page)
        # Fetch commits
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Error fetching commits: {response.status_code} - {response.text}")
            break

        data = response.json()
        if not data:
            break
        else:
            for rec in data:
                commit_id = rec["id"]
                sql_find = f"select id from gitlab_commits where id = '{commit_id}';"
                cursor = connection.cursor()
                cursor.execute(sql_find)
                result = cursor.fetchone()
                if result is None:
                    store_commit_data(rec, project_id, connection)
                else:
                    print(f"Commit ID: {commit_id} already exists.")
                    is_exists = True
                    break

        if is_exists:
            break
        page += 1
        

    return commits

if __name__ == "__main__":
    # PostgreSQL configuration
    db_config = {
        "host": os.getenv("host"),
        "database": os.getenv("database"),
        "user": os.getenv("user"),
        "password": os.getenv("password"),
    }

    project_id = os.getenv("gitlab_project_id")
    branch = os.getenv("gitlab_branch")
    headers = {
        'PRIVATE-TOKEN': os.getenv("gitlab_token"),
        'Cookie': '_cfuvid=fmTFyINfP48UAsCBxR.53c4U.MTQKGx9isYRy9jDKLQ-1736316897545-0.0.1.1-604800000'
        }
    # Connect to PostgreSQL database
    try:
        conn = psycopg2.connect(**db_config)
        print("Connected to the database.")
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        exit()

    # Create tables
    create_tables(conn)

    # Fetch commit history
    print("Fetching commit history...")
    commit_history = get_all_commits(project_id, headers, conn)
    print("Update .p:", n_dotp, ", dotr:", n_dotr, ", xml:", n_xml)
    conn.close()
