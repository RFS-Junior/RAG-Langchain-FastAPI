from typing import List
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings.openai import OpenAIEmbeddings

class QdrantConfig:
    """Configuration for Qdrant connection and collection."""
    URL = "localhost"
    PORT = 6333
    COLLECTION_NAME = "" #ADD YOUR COLLECTION
    VECTOR_SIZE = 1536
    DISTANCE = Distance.COSINE


class QdrantSingleton:
    """Singleton for managing a single instance of Qdrant."""
    _instance = None

    @staticmethod
    def get_instance():
        if QdrantSingleton._instance is None:
            QdrantSingleton._instance = QdrantSingleton()
        return QdrantSingleton._instance

    def __init__(self):
        if QdrantSingleton._instance is not None:
            raise Exception("This class is a singleton!")
        
        self._initialize()

    def _initialize(self):
        load_dotenv()
        self.client = QdrantClient(url=QdrantConfig.URL, port=QdrantConfig.PORT)
        self.collection_name = QdrantConfig.COLLECTION_NAME
        self.embeddings = OpenAIEmbeddings()

        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=QdrantConfig.VECTOR_SIZE, distance=QdrantConfig.DISTANCE)
            )

        self.qdrant_instance = Qdrant(
            client=self.client,
            collection_name=self.collection_name,
            embeddings=self.embeddings
        )

    def get_qdrant_instance(self):
        return self.qdrant_instance
    
    def select_examples(self, input: str, k: int) -> List[dict]:
        """
        Selects examples from Qdrant based on semantic similarity to the input query.
        """
        query_embedding = self.embeddings.embed_query(input)
        search_result = self.client.search(
            collection_name=self.qdrant_instance.collection_name,
            query_vector=query_embedding,
            limit=k
        )
        return [hit.payload for hit in search_result]

