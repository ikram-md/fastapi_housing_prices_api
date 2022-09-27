from typing import List

from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session

import oauth2
from db_config import get_db
from dtos.house_dto import HouseResponse, House
import models

router = APIRouter(
    prefix='/houses',
    tags=['Houses']
)


@router.get('/', response_model=List[HouseResponse])
async def get_list_of_houses(db: Session = Depends(get_db), auth_middleware: int = Depends(oauth2.get_current_user)):
    """Fetches all the houses from the database"""
    query = db.query(models.House).all()
    return query


@router.post('/create', response_model=HouseResponse)
async def add_new_house(data: House, db: Session = Depends(get_db),
                        current_user: models.User = Depends(oauth2.get_current_user)):
    # QUERYING USING SQLALCHEMY

    new_house = models.House(owner_id=current_user.id, **data.dict())
    db.add(new_house)
    db.commit()
    db.refresh(new_house)
    return new_house


@router.get('/{id}', response_model=HouseResponse)
def find_house(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    """Find specific post by their ID"""
    found_house = db.query(models.House).filter(models.House.id == id).first()
    if not found_house:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unable to find house with id = {id}")
    return found_house


@router.delete('/{id}/delete')
async def delete_house(id: int, db: Session = Depends(get_db),
                       current_user: models.User = Depends(oauth2.get_current_user)):
    """Delete specified post by their id"""
    found_house = db.query(models.House).filter(models.House.id == id).first()
    if not found_house:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unable to find house with id = {id}")
    db.delete(found_house)
    db.commit()
    return {"success": f"Post with id = {id} has been deleted successfully."}


@router.put('/{id}', response_model=HouseResponse)
async def update_house(id: int, data: House, db: Session = Depends(get_db),
                       current_user: models.User = Depends(oauth2.get_current_user)):
    """Update the house instance with necessary information"""
    found_house = db.query(models.House).filter(models.House.id == id)
    if not found_house.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unable to find house with id = {id}")
    found_house.update(data.dict(), synchronize_session=False)
    db.commit()
    return {"success": "House has been updated ", "house": found_house.first()}
