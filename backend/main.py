from fastapi import FastAPI
from pydantic import BaseModel
from rag_engine import ask_rag

app = FastAPI()


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {"status": "API çalışıyor"}


@app.post("/ask")
def ask_question(req: QuestionRequest):
    result = ask_rag(req.question)
    return result