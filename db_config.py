from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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
