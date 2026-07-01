from urllib.parse import quote_plus
from sqlalchemy import create_engine

from sql_maped_db import Base

#URL OF THE DATABASE (postgreSQL)
username = ("postgres")
password = quote_plus("password123")
db_name = ("Finance_Tracker_DB")

db_url = f"postgresql+psycopg2://{username}:{password}@localhost:5432/{db_name}"

engine = create_engine(db_url, echo=True)

with engine.connect() as conn:
    print("Connected successfully!")