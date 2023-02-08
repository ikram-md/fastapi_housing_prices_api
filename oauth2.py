from datetime import datetime, timedelta
import os
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from dotenv import load_dotenv
from sqlalchemy.orm import Session

import models
from db_config import get_db
from dtos.token import TokenData
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

# SECRET KEY
# Encryption Algorithm
# Expiration time

load_dotenv()


def generate_token(payload: dict, ):
    """_summary_

    Args:
        payload (dict): _description_

    Returns:
        _type_: _description_
    """

    payload_copy = payload.copy()

    expiration_time = datetime.utcnow() + timedelta()

    expire = datetime.now() + timedelta(minutes=float(os.getenv('ACCESS_TOKEN_DURATION_MINUTES')))

    payload_copy.update({"exp": expire})

    token = jwt.encode(payload_copy, os.getenv(
        'SECRET_KEY'), algorithm=os.getenv('ALGORITHM'))

    return token


def verify_token(token: str, cred_exception):
    """_summary_

    Args:
        token (str): _description_
        cred_exception (_type_): _description_

    Raises:
        cred_exception: _description_
        cred_exception: _description_

    Returns:
        _type_: _description_
    """

    try:
        payload = jwt.decode(token, os.getenv(
            'SECRET_KEY'), algorithms=[os.getenv('ALGORITHM')])

        id: str = payload.get("user_id")
        if not id:
            raise cred_exception

        token_data = TokenData(id=id)

        return token_data

    except JWTError:
        raise cred_exception


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """_summary_

    Args:
        token (str, optional): _description_. Defaults to Depends(oauth2_scheme).
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Returns:
        _type_: _description_
    """
    credentials_excep = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized",
                                      headers={"WWW-Authenticate": "Bearer"})
    token_data: TokenData = verify_token(token, credentials_excep)
    found_user: models.User = db.query(models.User).filter(
        models.User.id == token_data.id).first()
    print(found_user.email)
    return found_user
