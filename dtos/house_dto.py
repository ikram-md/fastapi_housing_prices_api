from typing import Optional
from pydantic import BaseModel

from dtos.user_dto import UserSerilizer


class House(BaseModel):
    address: str
    size: int
    waterfront: bool
    price: float
    desc: Optional[str]


class HouseResponse(BaseModel):
    id: int
    address: str
    desc: Optional[str]
    price: int
    owner_id: int
    owner : UserSerilizer

    class Config:
        orm_mode = True
