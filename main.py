import os
from fastapi import FastAPI
from dotenv import load_dotenv
from qdrant import QdrantManager
from routes import register_routes
from qdrant.indexes import create_indexes

load_dotenv()

def create_app() -> FastAPI:
    app = FastAPI(title="Course Search API", version="0.1.0")
    
    qdrant = QdrantManager(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
        collection_name=os.getenv("COLLECTION_NAME", "courses"),
        embedding_model=os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-minilm-l6-v2"),
    )
    create_indexes(qdrant.client, qdrant.collection_name) 
    register_routes(app, qdrant)
    return app

app = create_app()