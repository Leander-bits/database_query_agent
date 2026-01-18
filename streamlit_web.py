import requests
import pandas as pd
import streamlit as st
from supabase import create_client, Client

SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_ANON_KEY = st.secrets.get("SUPABASE_ANON_KEY", "")
BACKEND_URL = st.secrets.get("BACKEND_URL", "")

def supabase_sign_in(email: str, password: str) -> str:
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        raise RuntimeError("Missing SUPABASE_URL / SUPABASE_ANON_KEY in Streamlit secrets.")    
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    response = supabase.auth.sign_in_with_password({"email": email, "password": password})
    if not response.session or not response.session.access_token:
        raise RuntimeError("Login succeeded but no session/access_token returned.")
    return response.session.access_token

st.set_page_config(
    page_title="Internal Query Agent",
    page_icon="📦",
    layout="wide",
)
if "jwt" not in st.session_state:
    st.session_state.jwt = ""
with st.sidebar:
    st.header("Login")
    if st.session_state.jwt:
        st.success("Logged in successfully.")
        if st.button("Logout"):
            st.session_state.jwt = ""
            st.rerun()
    else:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Sign in"):
            try:
                st.session_state.jwt = supabase_sign_in(email, password)
                st.success("Logged in successfully.")
            except Exception as e:
                st.error(f"Login failed: {e}")
st.write("Internal Query Agent - Use natur language to get the information you need from the database")
st.caption("Enter a natural language question, and I will help you generate SQL and query the database.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "Hello, I am the Internal Query Assistant. You can ask me questions in natural language, for example: \n\n"
                        "The POD link of a specific order? \n\n"
                        "The consignee address of a specific order? \n"
            }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def call_backend(question: str, ):
    payload = {
        "question": question
    }
    try:
        headers = {}
        if st.session_state.get("jwt"):
            headers["Authorization"] = f"Bearer {st.session_state.jwt}"
        response = requests.post(BACKEND_URL, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {
            "question": question,
            "sql_query": "",
            "rows": [],
            "note": f"请求后端出错: {e}"
        }
if not st.session_state.get("jwt"):
    st.info("Please login first (sidebar) to use the query agent.")
    st.stop()
prompt = st.chat_input("Enter your question here...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Querying the database, please wait…")
        result = call_backend(prompt)
        sql_query = result.get("sql") or "<No SQL query generated>"
        note_text = result.get("note") or "<SQL query executed not successfully>"
        rows = result.get("rows") or []
        assistant_text = f"**Generated SQL：**\n```sql\n{sql_query}\n```\n"
        if note_text:
            assistant_text += f"**Status：** {note_text}\n"
        message_placeholder.markdown(assistant_text)
        if rows:
            df = pd.DataFrame(rows)
            st.markdown("**Query Result（Top 50）：**")
            st.dataframe(df)
    st.session_state.messages.append({"role": "assistant", "content": assistant_text})