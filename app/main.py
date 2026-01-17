from fastapi import FastAPI
from app.api.router import router

app = FastAPI(title="Outbound Lookup QA")
app.include_router(router)