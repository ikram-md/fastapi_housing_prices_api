from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    access_type: str


class TokenData(BaseModel):
    id: Optional[str] = None

