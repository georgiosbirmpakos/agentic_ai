from langchain_ollama import ChatOllama
from ..config import OLLAMA_MODEL, SCHEMA

class NL2SQLTranslator:
    def __init__(self):
        self.llm = ChatOllama(model=OLLAMA_MODEL)

    def translate(self, question: str) -> str:
        prompt = f"Convert this request into valid PostgreSQL SQL using schema `{SCHEMA}`. Only output SQL.\nRequest: {question}"
        response = self.llm.invoke(prompt)
        sql = response.content.strip()

        # remove markdown fences if present
        if sql.startswith("```"):
            sql = sql.strip("`")        # remove backticks
            sql = sql.replace("sql", "", 1).strip()  # drop leading 'sql'

        return sql

