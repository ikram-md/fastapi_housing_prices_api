import time
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import psycopg2
from sqlalchemy\
    .ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2

SQLALCH_DB_URL = 'postgresql://postgres:postgres159753@localhost/postgres'
engine = create_engine(SQLALCH_DB_URL)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# this function creates a session towards our database and could be injected in other services
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


# Connect to Postgres database.

while True:
    try:
        conn = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="postgres159753",
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connected successfully.")
        break

    except Exception as error:
        print("Connection to the database failed", error)
        time.sleep(2)
