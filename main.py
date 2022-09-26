import time
from fastapi import FastAPI, HTTPException, status, Depends
import models
import psycopg2
from db_config import engine, get_db
# this will help us retrieve the column name for the tables
from psycopg2.extras import RealDictCursor
from routers import houses, users, auth

app = FastAPI()

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

# ensures that our models are in sync.
models.Base.metadata.create_all(bind=engine)

# include our routers
app.include_router(houses.router)
app.include_router(users.router)
app.include_router(auth.router)
