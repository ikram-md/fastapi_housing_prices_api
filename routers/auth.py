from fastapi import APIRouter, status, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from db_config import get_db
import models
import utils
from dtos.login_dto import LoginDTO
from dtos.token import Token
from oauth2 import generate_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import os
from dotenv import load_dotenv
router = APIRouter(
    prefix='/auth',
    tags=["Authentication"]
)


# Load env variables
load_dotenv()


@router.post('/login')
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db),
                ):
    """_summary_

    Args:
        user_credentials (OAuth2PasswordRequestForm, optional): _description_. Defaults to Depends().
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: 404 if the user was not found.
        HTTPException: 403 if the credentials were invalid.

    Returns:
        dictionary: token access
    """
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials.")
    access_token = generate_token(payload={"user_id": user.id})

    return {"access_token": access_token, "access_type": "Bearer"}


@router.get("/register")
async def register():
    """ Funtion to register the user, accepts specific DTO.
    Returns:
        NULL: If user creation fails
    """
    print("current env variable")
    print(os.getenv('ALGORITHM'))
    return {"msg": "registered in here"}
