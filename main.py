import time
from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy import delete
import models
from house_dto.house_dto import House
import psycopg2

from db_config import engine, get_db

# this will help us retrieve the column name for the tables
from psycopg2.extras import RealDictCursor

app = FastAPI()

# TODO: Connect to Postgres database.
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


@app.get('/houses')
async def get_list_of_houses(db: Session = Depends(get_db)):
    """Fetches all the houses from the database"""
    query = db.query(models.House).all()

    # cursor.execute("""SELECT * FROM houses ORDER BY id DESC""")
    # query = cursor.fetchall()
    return {"houses": query}


@app.post('/houses/create')
async def add_new_house(data: House, db: Session = Depends(get_db)):
    # QUERYING USING SQLALCHEMY

    new_house = models.House(**data.dict())
    db.add(new_house)
    db.commit()
    db.refresh(new_house)
    return {"success": "Instance has been successfully added to the database.", "new_house": new_house}


@app.get('/houses/{id}')
def find_house(id: int, db: Session = Depends(get_db)):
    """Find specific post by their ID"""
    found_house = db.query(models.House).filter(models.House.id == id).first()
    if not found_house:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unable to find house with id = {id}")
    return {"success": found_house}


@app.delete('/houses/{id}/delete')
async def delete_house(id: int, db: Session = Depends(get_db)):
    """Delete specified post by their id"""
    found_house = db.query(models.House).filter(models.House.id ==id).first()
    if not found_house:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unable to find house with id = {id}")
    db.delete(found_house)
    db.commit()
    return {"success": f"Post with id = {id} has been deleted successfully."}


@app.put('/houses/{id}')
async def update_house(id: int, data: House, db: Session = Depends(get_db)):
    """Update the house instance with necessary information"""
    found_house = db.query(models.House).filter(models.House.id ==id)
    if not found_house.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unable to find house with id = {id}")
    found_house.update(data.dict(), synchronize_session=False)
    db.commit()
    return {"success": "House has been updated ", "house" : found_house.first()}
