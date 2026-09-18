import urllib
from sqlalchemy import create_engine

SERVER_NAME = r'localhost'
DATABASE_NAME = 'ECommerce_DWH'

params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER_NAME};"
    f"DATABASE={DATABASE_NAME};"
    f"Trusted_Connection=yes;"
    f"TrustServerCertificate=yes;"
)

CONNECTION_STRING = f"mssql+pyodbc:///?odbc_connect={params}"

def get_db_engine():
    """
    SQLAlchemy Engine nesnesi döndürür.
    """
    return create_engine(CONNECTION_STRING,fast_executemany=True)