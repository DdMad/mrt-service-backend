from fastapi import FastAPI
from app.api.api import router
from app.services.mrt_service import MrtService
from app.core.config import settings


app = FastAPI()


@app.get("/")
async def root():
    return 'Hello World!'

app.include_router(router, prefix=settings.API_V1_STR)