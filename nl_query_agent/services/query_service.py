from ..db.connector import PostgresConnector
from ..llm.translator import NL2SQLTranslator

class QueryService:
    def __init__(self):
        self.db = PostgresConnector()
        self.translator = NL2SQLTranslator()

    def handle_question(self, question: str):
        sql = self.translator.translate(question)
        return {"question": question, "sql": sql, "results": self.db.run_query(sql)}
