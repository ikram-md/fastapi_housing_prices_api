from sqlalchemy.orm import relationship
from db_config import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, TIMESTAMP, text, ForeignKey


# we store all of our table models in this file.
class House(Base):
    """_summary_

    Args:
        Base (_type_): _description_
    """
    __tablename__ = "houses"

    id = Column(Integer, primary_key=True, nullable=False)
    address = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    waterfront = Column(Boolean, default=True)
    size = Column(Integer, nullable=False)
    desc = Column(String, server_default='No description was provided.')

    # 1:1 Relationship with users
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    owner = relationship('User')

    # timestamp column
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class User(Base):
    """_summary_

    Args:
        Base (_type_): _description_
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=True, default="")
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
