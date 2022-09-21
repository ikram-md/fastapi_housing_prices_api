from db_config import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, PrimaryKeyConstraint, TIMESTAMP, text


# we store all of our table models in this file.
class House(Base):
    __tablename__ = "houses"

    id = Column(Integer, primary_key=True,nullable=False)
    address = Column(String, nullable=False)
    price =Column(Float, nullable=False)
    waterfront = Column(Boolean, default=True)
    size = Column(Integer, nullable=False)
    desc= Column(String, server_default='No description was provided.')
    #timestamp column
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))