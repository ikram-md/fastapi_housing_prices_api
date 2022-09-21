from typing import Optional
from pydantic import BaseModel


class House(BaseModel):
    address: str
    size: int
    waterfront: bool
    price: float
    desc: Optional[str]
