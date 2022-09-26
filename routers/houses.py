from typing import List

from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from db_config import get_db
from dtos.house_dto import HouseResponse, House
import models

router = APIRouter()


@router.get('/houses', response_model=List[HouseResponse])
async def get_list_of_houses(db: Session = Depends(get_db), ):
    """Fetches all the houses from the database"""
    query = db.query(models.House).all()

    # cursor.execute("""SELECT * FROM houses ORDER BY id DESC""")
    # query = cursor.fetchall()
    return query


@router.post('/houses/create', response_model=HouseResponse)
async def add_new_house(data: House, db: Session = Depends(get_db)):
    # QUERYING USING SQLALCHEMY

    new_house = models.House(**data.dict())
    db.add(new_house)
    db.commit()
    db.refresh(new_house)
    return new_house


@router.get('/houses/{id}', response_model=HouseResponse)
def find_house(id: int, db: Session = Depends(get_db)):
    """Find specific post by their ID"""
    found_house = db.query(models.House).filter(models.House.id == id).first()
    if not found_house:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unable to find house with id = {id}")
    return found_house


@router.delete('/houses/{id}/delete')
async def delete_house(id: int, db: Session = Depends(get_db)):
    """Delete specified post by their id"""
    found_house = db.query(models.House).filter(models.House.id == id).first()
    if not found_house:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unable to find house with id = {id}")
    db.delete(found_house)
    db.commit()
    return {"success": f"Post with id = {id} has been deleted successfully."}


@router.put('/houses/{id}', response_model=HouseResponse)
async def update_house(id: int, data: House, db: Session = Depends(get_db)):
    """Update the house instance with necessary information"""
    found_house = db.query(models.House).filter(models.House.id == id)
    if not found_house.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unable to find house with id = {id}")
    found_house.update(data.dict(), synchronize_session=False)
    db.commit()
    return {"success": "House has been updated ", "house": found_house.first()}
