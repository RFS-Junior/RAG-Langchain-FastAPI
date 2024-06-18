import os
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from models.models import Service, QuestionRequest
from services.langachain_service import LangChainService
from services.qdrant_manager import QdrantManager
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

qdrant_manager = QdrantManager()

langchain_service = LangChainService(qdrant_manager=qdrant_manager, llm=llm)

@app.get("/")
async def root():
    """
    Raiz da API para verificar se está em execução.
    """
    return {"message": "Hello World"}

@app.post("/search_service")
async def search_service(question_request: QuestionRequest):
    """
    Endpoint para pesquisar um serviço com base em uma pergunta.
    """
    try:
        question = question_request.question
        response =  langchain_service.generate_response(question)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/add_examples")
async def add_examples(examples: List[Service]):
    """
    Endpoint para adicionar exemplos de serviços.
    """
    try:
        langchain_service.add_services(examples)
        return {"message": "Examples added successfully!"}
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
