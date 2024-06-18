import uuid, json
from fastapi import HTTPException
from utils.qdrant_singleton import QdrantSingleton
from langchain_core.prompts.few_shot import FewShotPromptTemplate
from langchain_core.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from models.models import Service
from typing import List

class QdrantManager:
    """
    Classe para gerenciar operações relacionadas ao Qdrant.
    """

    def __init__(self):
        self.qdrant_instance = QdrantSingleton.get_instance()

    def search_service_to_qdrant(self, question: str, llm: ChatOpenAI):
        """
        Gera uma resposta para uma entrada de texto dada usando RetrievalQA.
        """
        
        examples = self.qdrant_instance.select_examples(input=question, k=2)
        
        example_prompt = PromptTemplate(
            input_variables=["input", "output"],
            template="Input: {input}\nOutput: {output}"
        )
        
        few_shot_prompt = FewShotPromptTemplate(
            examples=examples,
            example_prompt=example_prompt,
            prefix = """Você é um especialista em ...""",
            suffix = "Input: {input}\nOutput:",
            input_variables = ["input"]
        )
        
        formatted_examples = "\n\n".join([
            example_prompt.format(
                input=ex['description'],
                output=ex
            ) for ex in examples
        ])
        
        formatted_prompt = few_shot_prompt.prefix + "\n\n" + formatted_examples + "\n\n" + few_shot_prompt.suffix.format(input=question)
        
        response = llm.invoke(formatted_prompt)
        
        try:
            return json.loads(response.content.replace("'", '"'))
        
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=400, detail=f"JSON Decode Error: {e}")
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
    
    def add_examples_to_qdrant(self, examples: List[Service]):
        """
        Adiciona uma lista de exemplos à coleção Qdrant.
        """
        points = []
        for i, example in enumerate(examples):
            if not isinstance(example, Service):
                raise ValueError(f"O exemplo na posição {i} não é do tipo Service")
            
            vector = self.qdrant_instance.embeddings.embed_query(example.description)
                        
            payload = {} #ADD YOUR JSON STRUCTURE

            points.append({
                "id": str(uuid.uuid4()),
                "vector": vector,
                "payload": payload
            })
                    
        self.qdrant_instance.get_qdrant_instance().client.upsert(
            collection_name=self.qdrant_instance.get_qdrant_instance().collection_name,
            wait=True,
            points=points
        )
