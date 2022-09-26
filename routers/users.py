from typing import List
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from db_config import get_db
from dtos.user_dto import User, UserSerilizer
import models, utils

# creating a router instance
router = APIRouter(
    prefix="/users"
)


@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=UserSerilizer)
async def create_user(data: User, db: Session = Depends(get_db)):
    data.password = utils.hash_password(data.password)

    # storing the user instance
    found_user = db.query(models.User).filter(models.User.email == data.email).first()
    if found_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with email {data.email} already exists")
    new_user = models.User(**data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Get all the users
@router.post('/', status_code=status.HTTP_200_OK, response_model=UserSerilizer)
async def get_users(db: Session = Depends(get_db)):
    found_users = db.query(models.User).findAll()
    if not found_users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No user has been found')
    return found_users


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=UserSerilizer)
async def get_user(id: int, db: Session = Depends(get_db)):
    found_user = db.query(models.User).filter(models.User.id == id).first()
    if not found_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    return found_user


@router.delete('/{id}/delete', status_code=status.HTTP_200_OK)
async def delete_user(id: int, db: Session = Depends(get_db)):
    found_user = db.query(models.User).filter(models.User.id == id).first()
    if not found_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id = {id} was not found")
    db.delete(found_user)
    db.commit()
    return {"success": "User deleted successfully."}


@router.patch('/{id}/update', status_code=status.HTTP_200_OK, response_model=UserSerilizer)
async def update_user(id: int, data: User, db: Session = Depends(get_db)):
    found_user = db.query(models.User).findOne(models.User.id == id).first()
    if not found_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id = {id} was not found")
    found_user.update(**data.dict(), synchronize_session=False)
    db.commit()
    return found_user
