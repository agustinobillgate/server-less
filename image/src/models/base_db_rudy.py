from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

def get_database_session(database_url):
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()

# DB_HOST = "52.220.146.33"
# DB_NAME = "vhp"
# DB_USER = "postgres"
# DB_PASSWORD = "VHPLite#2023"
# DB_PORT     = 5432
# DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

DB_HOST = "db-vhplite.cjjyqihtbwnm.ap-southeast-1.rds.amazonaws.com"
DB_NAME = "postgres"
DB_USER = "adminvhplite23"
DB_PASSWORD = "superlite#rds"
DB_PORT     = 5432
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False)
Base = declarative_base()