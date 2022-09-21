from typing import Optional
from pydantic import BaseModel


class House(BaseModel):
    address: str
    size: int
    waterfront: bool
    price: float
    desc: Optional[str]


class HouseResponse(BaseModel):
    id : int
    address: str
    desc: Optional[str]
    price: int

    class Config:
        orm_mode = True
