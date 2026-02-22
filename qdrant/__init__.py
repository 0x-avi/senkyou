# qdrant/__init__.py
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http import models

load_dotenv()

class QdrantManager:
    def __init__(self, url: str, api_key: str, collection_name: str = "courses", embedding_model: str = "sentence-transformers/all-minilm-l6-v2"):
        self.url = url
        self.api_key = api_key
        self.collection_name = collection_name
        self.embedding_model = embedding_model

        self.client = QdrantClient(url=self.url, api_key=self.api_key)

        # Ensure collection exists
        existing = [c.name for c in self.client.get_collections().collections]
        if self.collection_name not in existing:
            print('couldnt find collection')
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=384,
                    distance=models.Distance.COSINE
                )
            )