from functools import lru_cache
from urllib.parse import quote_plus
from langchain_community.utilities import SQLDatabase
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine
from app.core.settings import settings

def _build_uri() -> str:
    dsn = (
        f"DRIVER={settings.ssms_driver};"
        f"SERVER={settings.ssms_host};"
        f"DATABASE={settings.ssms_db};"
        f"Trusted_Connection=Yes;"
        f"TrustServerCertificate=Yes;"
    )
    odbc_connect = quote_plus(dsn)
    uri = f"mssql+pyodbc:///?odbc_connect={odbc_connect}"
    return uri

@lru_cache(maxsize=1)
def get_sql_database() -> SQLDatabase:
    uri = _build_uri()
    return SQLDatabase.from_uri(
        uri,
        include_tables=[settings.lookup_table],
        schema=settings.lookup_schema,
        sample_rows_in_table_info=3,
    )

@lru_cache(maxsize=1)
def get_sql_engine() -> Engine:
    uri = _build_uri()
    engine = create_engine(uri, fast_executemany=False)
    return engine