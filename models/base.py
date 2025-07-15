# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# Base = declarative_base()

# def get_database_session(database_url):
#     engine = create_engine(database_url)
#     SessionLocal = sessionmaker(bind=engine)
#     return SessionLocal()


# version = 1.0.0.2


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Dict

Base = declarative_base()

# Cache for created engines (one per database_url)
_engine_cache: Dict[str, sessionmaker] = {}

def get_database_session(database_url: str) -> Session:
    if database_url not in _engine_cache:
        engine = create_engine(
            database_url,
            pool_size=10,
            max_overflow=20,
            pool_timeout=200,
            pool_pre_ping=True  # Prevent reuse of stale connections
        )
        _engine_cache[database_url] = sessionmaker(bind=engine)

    SessionLocal = _engine_cache[database_url]
    return SessionLocal()

# def get_database_session(database_url):
#     engine = create_engine(
#         database_url
#     )

#     SessionLocal = sessionmaker(bind=engine)

#     return SessionLocal()