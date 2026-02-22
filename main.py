import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from qdrant import QdrantManager
from routes import register_routes
from qdrant.indexes import create_indexes

load_dotenv()

def create_app() -> FastAPI:
    app = FastAPI(title="Course Search API", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

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

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
