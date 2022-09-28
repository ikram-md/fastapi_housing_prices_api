from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

import models
from db_config import get_db
from dtos.token import Token, TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

# SECRET KEY
# Encryption Algorithm
# Expiration time

SECRET_KEY = "8788bdc9e5de2f484ed982969adb9ef8a64adba993d5e08fc5b28dfe45872d66"
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION_MINUTES = 30


def generate_token(payload: dict, ):

    payload_copy = payload.copy()

    expiration_time = datetime.utcnow() + timedelta()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_DURATION_MINUTES)

    payload_copy.update({"exp": expire})

    token = jwt.encode(payload_copy, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token: str, cred_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")

        if not id:
            raise cred_exception

        token_data = TokenData(id=id)

        return token_data

    except JWTError:
        raise cred_exception


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_excep = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized",
                                      headers={"WWW-Authenticate": "Bearer"})
    token_data: TokenData = verify_token(token, credentials_excep)
    found_user: models.User = db.query(models.User).filter(models.User.id == token_data.id).first()
    print(found_user.email)
    return found_user
