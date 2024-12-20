from fastapi import FastAPI
from .api import auth as auth_api
from .api import users as users_api
from core.database import engine
from .models import user as user_model
from utils.logger import logger

user_model.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_api.router, prefix="/auth", tags=["auth"])
app.include_router(users_api.router, prefix="/users", tags=["users"])

@app.on_event("startup")
async def startup_event():
    logger.info("Application started")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown")