from app.services.chat_service import get_chat_model
from app.prompts.search_prompts import GENERATE_SQL_QUERY_PROMPT
from langchain_core.prompts import PromptTemplate
from app.core.settings import settings
from app.tools.rag import retrieve_context
import json
import re
from supabase import create_client

# generate SQL query
def generate_sql_query(question:str) -> str:

    context = retrieve_context(question, k=1, max_chars=1500)

    chat_model = get_chat_model()
    prompt = PromptTemplate.from_template(GENERATE_SQL_QUERY_PROMPT)
    text = prompt.format(
        context=context,
        schema=settings.schema_name,
        table=settings.table_name,
        allowed_columns=", ".join(settings.allowed_columns),
        default_top=20,
        question=question,
    )
    response = chat_model.invoke(text).content.strip()
    try:
        response_clean = re.sub(r"```(json)?", "", response).strip("` \n")
        data = json.loads(response_clean)
        sql = data.get("sql", "").strip()
        return sql
    except Exception:
        m = re.search(r"(?is)(select\b.*?;)", response)
        return m.group(1).strip() if m else ""

def normalize_sql(sql: str) -> str:
    sql = sql.strip()
    if sql.startswith("```"):
        lines = sql.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        sql = "\n".join(lines).strip()
    m = re.search(r"\bSELECT\b", sql, re.IGNORECASE)
    if m:
        sql = sql[m.start():]
    return sql.strip()

# SQL query safety check
def is_safe_sql_query(sql_query: str) -> bool:
    forbidden_statements = ["INSERT", "UPDATE", "DELETE", "MERGE", "ALTER", "DROP", "TRUNCATE", "CREATE", "EXEC", "EXECUTE"]
    sql_query = normalize_sql(sql_query)
    upper_query = sql_query.upper().strip()
    if not upper_query.startswith("SELECT"):
        return False
    for statement in forbidden_statements:
        if statement in upper_query:
            return False
    return True

# ensure SQL query has LIMIT clause
def ensure_limit_clause(sql_query: str) -> str:
    s = sql_query.strip().rstrip(";")
    if re.search(r"\bLIMIT\s+\d+\b", s, flags=re.IGNORECASE):
        return s + ";"
    return f"{s} LIMIT 20;"

# execute SQL query
def execute_sql_query(sql_query: str, jwt: str):
    if not jwt:
        return [], "Missing user JWT. Please login first."
    sql_query = normalize_sql(sql_query)
    if not is_safe_sql_query(sql_query):
        return [], "SQL rejected by safety check."
    sql_query = ensure_limit_clause(sql_query)
    sql_query = sql_query.strip().rstrip(";")
    client = create_client(
        settings.supabase_url,
        settings.supabase_service_role_key
    )
    try:
        response = client.rpc(
            "execute_sql_query",
            {"sql_text": sql_query}
        ).execute()
    except Exception as e:
        return [], f"Supabase RPC error: {e}"
    rows = response.data
    if not rows:
        return [], "No matching records were found in the current result."
    return rows, "SQL executed successfully."