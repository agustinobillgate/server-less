# DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?application_name=aws_lambda_serverless"
#     session = get_database_session(DATABASE_URL)
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from datetime import datetime, timedelta


DB_HOST = "psql.staging.e1-vhp.com"
DB_NAME = "vhptools"
DB_USER = "postgres"
DB_PASSWORD = "DevPostgreSQL#2024"
DB_PORT     = 5432
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?application_name=aws_lambda_serverless"
dashboard_engine = create_engine(DATABASE_URL)
dashboard_SessionLocal = sessionmaker(bind=dashboard_engine)
dashboard_metadata = MetaData()


sql_rptid_1 = text("""
                SELECT  
                    DATE(t.test_datetime) AS test_datetime,
                    td.vhp_module,
                    td.endpoint_module,
                    STRING_AGG(DISTINCT td.compare_status, '; ') AS compare_status
                FROM test t 
                JOIN test_detail td ON t.id = td.test_id
                WHERE DATE(t.test_datetime) = :today
                    AND lower(td.compare_status) LIKE :errkey
                    AND td.compare_status NOT IN ('OK', 'Different Results', 'RECID', 'RECID DIFF')
                GROUP BY DATE(t.test_datetime), td.vhp_module, td.endpoint_module
                ORDER BY DATE(t.test_datetime) DESC, td.vhp_module, td.endpoint_module;
                """)

sql_rptid_2 = text("""
                SELECT  
                    DATE(t.test_datetime) AS test_datetime,
                    td.vhp_module,
                    td.endpoint_module,
                    STRING_AGG(DISTINCT td.compare_status, '; ') AS compare_status
                FROM test t 
                JOIN test_detail td ON t.id = td.test_id
                WHERE DATE(t.test_datetime) = :today
                    AND td.compare_status NOT IN ('OK', 'Different Results', 'RECID', 'RECID DIFF')
                    AND lower(td.endpoint_module) LIKE :endpoint
                GROUP BY DATE(t.test_datetime), td.vhp_module, td.endpoint_module
                ORDER BY DATE(t.test_datetime) DESC, td.vhp_module, td.endpoint_module;
                """)

sql_rptid_0 = text("""
                SELECT  
                    DATE(t.test_datetime) AS test_datetime,
                    td.vhp_module,
                    td.endpoint_module,
                    
                    STRING_AGG(DISTINCT 
                        CASE
                            WHEN td.compare_status LIKE '%Internal Server Error%' THEN 'Internal Error'
                            WHEN td.compare_status LIKE '%Progress Status%' THEN 'Progress Status'
                            WHEN td.compare_status LIKE '%NoneType%' THEN 'NoneType'
                            WHEN td.compare_status LIKE '%datetime%' THEN 'Datetime Error'
                            WHEN td.compare_status LIKE '%collation%' THEN 'Collation Error'
                            WHEN td.compare_status LIKE '%TypeError%' THEN 'Type Error'
                            WHEN td.compare_status LIKE '%KeyError%' THEN 'Key Error'
                            WHEN td.compare_status LIKE '%IndexError%' THEN 'Index Error'
                            WHEN td.compare_status LIKE '%AttributeError%' THEN 'Attribute Error'
                            WHEN td.compare_status LIKE '%ValueError%' THEN 'Value Error'
                            WHEN td.compare_status LIKE '%NameError%' THEN 'Name Error'
                            WHEN td.compare_status LIKE '%404%' THEN 'Not Found (404)'
                            ELSE 'Other'
                        END, '; '
                    ) AS error_type,
                    STRING_AGG(DISTINCT td.compare_status, '; ') AS compare_status
                FROM test t 
                JOIN test_detail td ON t.id = td.test_id
                WHERE DATE(t.test_datetime) = :today
                   AND td.endpoint_module LIKE :endpoint%
                AND (
                        td.compare_status LIKE '%Internal Server Error%' OR
                        td.compare_status LIKE '%Progress Status%' OR
                        td.compare_status LIKE '%NoneType%' OR
                        td.compare_status LIKE '%datetime%' OR
                        td.compare_status LIKE '%collation%' OR
                        td.compare_status LIKE '%TypeError%' OR
                        td.compare_status LIKE '%KeyError%' OR
                        td.compare_status LIKE '%IndexError%' OR
                        td.compare_status LIKE '%AttributeError%' OR
                        td.compare_status LIKE '%ValueError%' OR
                        td.compare_status LIKE '%NameError%' OR
                        td.compare_status LIKE '%404%'
                    )
                GROUP BY DATE(t.test_datetime), td.vhp_module, td.endpoint_module
                ORDER BY DATE(t.test_datetime) DESC, td.vhp_module, td.endpoint_module;

                
                """)

def clean_status(value: str) -> str:
    # Split by ';', remove empty strings and strip whitespace
    parts = [v.strip() for v in value.split(";") if v.strip()]
    # Remove duplicates while preserving order
    seen = set()
    unique = []
    for part in parts:
        if part not in seen:
            seen.add(part)
            unique.append(part)
    return "; ".join(unique)

def main_dashboard(params: dict) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    print("Received query parameters in main_dashboard:")
    for key, value in params.items():
        print(f"{key} = {value}")

    rptid = params.get("rptid")
    errkey = params.get("errkey", "%")  # default to match all
    endpoint = params.get("ep", "%")
    endpoint = endpoint.lower()
    errkey = errkey.lower()

    session = dashboard_SessionLocal()
    txt = ""
    table_data = []
    try:
        # Reflect the table
        sql_name = f"sql_rptid_{rptid}"
        print(sql_name)
        sql_stmt = globals().get(sql_name)
        print(sql_stmt) 
        result = session.execute(sql_stmt, {"today": today, "errkey": f"%{errkey}%", "endpoint": f"%{endpoint}%"})
        rows = result.fetchall()
        column_names = result.keys()

        table_data = [
            {
               key: (
                    value.replace("OK;", "")
                        .replace("Different Results;", "")
                        .strip()
                    if isinstance(value, str) else value
                )
                for key, value in dict(zip(column_names, row)).items()
            }
            for row in rows
        ]

        
    except Exception as e:
        print("SQLAlchemy DB error:", e)
        table_data = []
    finally:
        session.close()

    return {
        "title": "Cloud VHP Dashboard",
        "params": params,
        "txt": txt,
        "table_data": table_data
    }