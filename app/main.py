from fastapi import FastAPI
from app.api.router import router

app = FastAPI(title="Database QA")
app.include_router(router)