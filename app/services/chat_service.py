from langchain_openai import ChatOpenAI
from app.core.settings import settings

# get chat model
def get_chat_model()  -> ChatOpenAI:
    model = ChatOpenAI(
        api_key=settings.deepseek_api_key,
        base_url=settings.deepseek_base_url,
        model=settings.deepseek_model,
        temperature=0,
    )
    return model