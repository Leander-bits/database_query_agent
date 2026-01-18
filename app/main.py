from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.router import router
from app.tools.rag import build_update_index, DOC_PATHS

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        build_update_index(doc_paths=DOC_PATHS)
        print("[RAG] FAISS index built.")
    except Exception as e:
        print(f"[RAG] Failed to build index on startup: {e}")
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router)