from fastapi import FastAPI
from pydantic import BaseModel
from .services.query_service import QueryService

app = FastAPI()
service = QueryService()

class NLQuery(BaseModel):
    question: str

@app.post("/query")
def query_db(nl: NLQuery):
    return service.handle_question(nl.question)