from typing import List
from models.models import Service
from services.qdrant_manager import QdrantManager
from langchain_openai import ChatOpenAI

class LangChainService:
    """
    Classe para lidar com operações de processamento de linguagem natural usando langchain.
    """
    
    def __init__(self, qdrant_manager: QdrantManager, llm: ChatOpenAI):
        self.qdrant_manager = qdrant_manager
        self.llm = llm
    
    def generate_response(self, question: str):
        return self.qdrant_manager.search_service_to_qdrant(question, llm=self.llm)
    
    def add_services(self, examples: List[Service]):
        return self.qdrant_manager.add_examples_to_qdrant(examples)