from functools import lru_cache
from langchain_ollama import ChatOllama
from app.core.settings import settings

# 获取Ollama模型
@lru_cache(maxsize=1)
def get_ollama_model()  -> ChatOllama:
    model = ChatOllama(
        model=settings.ollama_model,
        base_url=settings.ollama_base_url,
        temperature=0.0,
        model_kwargs={
            "format": "json",
            "num_predict": 200,
            "top_p": 0.9,
            "num_ctx": 2048,
        },
    )
    return model