from urllib.parse import quote_plus
from sqlalchemy import create_engine

#URL OF THE DATABASE (postgreSQL)
username = ("postgres")
password = quote_plus("demo@8888")
db_name = ("Finance Analyser Database")

db_url = f"postgresql+psycopg2://{username}:{password}@localhost:5432/{db_name}"

engine = create_engine(db_url, echo=True)

with engine.connect() as conn:
    print("Connected successfully!")