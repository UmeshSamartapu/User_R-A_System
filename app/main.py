from fastapi import FastAPI
from .routes import router

app = FastAPI(title="Test API with JWT & MongoDB")

app.include_router(router)