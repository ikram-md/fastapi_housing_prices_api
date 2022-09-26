from pydantic import BaseModel, EmailStr


class User(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    email: EmailStr
    password: str


class UserSerilizer(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    id : int
    email: str

    class Config:
        """_summary_
        """
        orm_mode = True
