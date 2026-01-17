from fastapi import APIRouter, Header
from app.api.qa import AskIn, AskOut
from app.services.search_service import generate_sql_query
from app.services.search_service import execute_sql_query

router = APIRouter()

@router.get("/health")
def health():
    return {"ok": True}

@router.post("/ask", response_model=AskOut)
def ask(body: AskIn, authorization: str = Header(default="")):
    try:
        sql = generate_sql_query(body.question)
    except Exception as e:
        sql = ""
        print(f"[SQL-GEN] error: {e}")
    rows, note = [], "No sql generated"
    jwt = ""
    if authorization and authorization.startswith("Bearer "):
        jwt = authorization[len("Bearer "):].strip()
    if sql.strip():
        try:
            rows, note = execute_sql_query(sql, jwt)
        except Exception as e:
            rows = []
            note = f"Execution error: {e}"
    return AskOut(question=body.question, sql=sql, rows=rows, note=note)