import re

def extract_temp_tables(df_content):
    # Pattern to capture 'DEFINE TEMP-TABLE <temp-table-name> LIKE <like-table-name>'
    temp_table_pattern = re.compile(
        r'^DEFINE\s+TEMP-TABLE\s+(\S+)\s+LIKE\s+(\S+)\s*\.?\s*$', 
        re.IGNORECASE
    )
    temp_tables = []

    for line in df_content.splitlines():
        match = temp_table_pattern.match(line.strip())
        if match:
            temp_table_name = match.group(1)
            like_table_name = match.group(2)
            temp_tables.append((temp_table_name, like_table_name))

    return temp_tables

# Example usage
df_content = """
DEFINE TEMP-TABLE reslin-list  LIKE res-line.
DEFINE TEMP-TABLE curr-resline LIKE res-line.
DEFINE TEMP-TABLE t-history    LIKE history.
"""

temp_tables = extract_temp_tables(df_content)
for temp_table in temp_tables:
    print(f"Temp Table: {temp_table[0]}, Like Table: {temp_table[1]}")
