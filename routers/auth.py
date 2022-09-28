from fastapi import APIRouter, status, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from db_config import get_db
import models, utils
from dtos.login_dto import LoginDTO
from dtos.token import Token
from oauth2 import generate_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    prefix='/auth',
    tags=["Authentication"]
)


@router.post('/login')
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db),
                ):
    print(user_credentials)
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials.")
    # generate a token
    access_token = generate_token(payload={"user_id": user.id})

    return {"access_token" : access_token, "access_type" : "Bearer"}
