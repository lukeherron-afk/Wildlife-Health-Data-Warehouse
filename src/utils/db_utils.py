import os
from sqlalchemy import create_engine

def get_engine():
    """
    Returns a SQLAlchemy engine with smart defaults.
    Prioritizes Docker environment variables, then falls back to local dev settings.
    """
    db_host = os.getenv("DB_HOST", "localhost")
    db_user = os.getenv("DB_USER", "postgres")
    db_pass = os.getenv("DB_PASS", "postgres")
    db_name = os.getenv("DB_NAME", "wildlife_health")
    
    conn_string = f"postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}"
    return create_engine(conn_string)