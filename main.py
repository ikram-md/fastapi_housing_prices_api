from fastapi import FastAPI
import models
from db_config import engine

from routers import houses, users, auth

app = FastAPI()


# ensures that our models are in sync.
models.Base.metadata.create_all(bind=engine)

# include our routers
app.include_router(houses.router)
app.include_router(users.router)
app.include_router(auth.router)

