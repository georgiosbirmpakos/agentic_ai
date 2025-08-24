import psycopg2
from psycopg2.extras import RealDictCursor
from langchain_ollama import ChatOllama
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
from config import DB_CONFIG, SCHEMA, OLLAMA_MODEL

server = FastMCP("nl-query-mcp")
llm = ChatOllama(model=OLLAMA_MODEL)

def translate(question: str) -> str:
    """Convert natural language to SQL using Ollama."""
    prompt = (
        f"Convert this request into valid PostgreSQL SQL using schema `{SCHEMA}`. "
        f"Only output SQL, no explanation, no markdown.\n"
        f"Request: {question}"
    )
    response = llm.invoke(prompt)
    sql = response.content.strip()
    if sql.startswith("```"):
        sql = sql.strip("`").replace("sql", "", 1).strip()
    return sql

def run_query(sql: str):
    """Execute SQL on Postgres and return rows."""
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(f"SET search_path TO {SCHEMA};")
            cur.execute(sql)
            return cur.fetchall()
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()

@server.tool(
    name="query_db",
    description="Ask a natural language question and get results from the ESG Postgres DB",
)
def query_db(question: str) -> TextContent:
    sql = translate(question)
    try:
        rows = run_query(sql)
        return TextContent(type="text", text=f"SQL: {sql}\nResults: {rows}")
    except Exception as e:
        return TextContent(type="text", text=f"❌ SQL: {sql}\nError: {e}")

if __name__ == "__main__":
    server.run()
