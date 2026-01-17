from sqlalchemy import create_engine, inspect
from urllib.parse import quote_plus

DRIVER = "ODBC Driver 17 for SQL Server"
SERVER = "."
DATABASE = "DataWarehouse"
dsn = f"DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=Yes;TrustServerCertificate=Yes;"

uri = f"mssql+pyodbc:///?odbc_connect={quote_plus(dsn)}"
insp = inspect(create_engine(uri))

print("Schemas:", insp.get_schema_names())
print("VIEWS in [serve]:", insp.get_view_names(schema="serve"))
print("TABLES in [serve]:", insp.get_table_names(schema="serve"))