from fastapi import FastAPI, Query
from qdrant import QdrantManager
from backend.handlers import search_handler, search_by_language_handler, health_handler


def register_routes(app: FastAPI, qdrant: QdrantManager) -> None:
    app.get("/search")(search_handler(qdrant))
    app.get("/search_by_language")(search_by_language_handler(qdrant))
    # app.get("/search_lecture")(search_lecture_handler(qdrant))
    app.get("/health")(health_handler())