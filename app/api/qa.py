from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class AskIn(BaseModel):
    question:str = Field(..., description="The natural language question")

class AskOut(BaseModel):
    question:str
    sql:str
    rows: List[Dict[str, Any]] = []
    note:Optional[str] = None