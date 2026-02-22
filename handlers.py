from fastapi import Query
from qdrant import QdrantManager
from qdrant.search import search, search_by_language
from typing import Callable


def search_handler(qdrant: QdrantManager) -> Callable:
    def handler(
        query: str = Query(..., description="Search query text"),
        top_k: int = Query(5, description="Number of results to return"),
    ):
        results = search(qdrant, query=query, top_k=top_k)
        return {"results": results}
    return handler


def search_by_language_handler(qdrant: QdrantManager) -> Callable:
    def handler(
        query: str = Query(..., description="Search query text"),
        language: str = Query(..., description="Language code, e.g. 'en', 'fr'"),
        top_k: int = Query(5, description="Number of results to return"),
    ):
        results = search_by_language(qdrant, query=query, language=language, top_k=top_k)
        return {"results": results}
    return handler


# def search_lecture_handler(qdrant: QdrantManager) -> Callable:
#     def handler(
#         keyword: str = Query(..., description="Keyword to search in lecture titles"),
#         top_k: int = Query(5, description="Number of results to return"),
#     ):
#         results = keyword_search_lecture(qdrant, keyword=keyword, top_k=top_k)
#         return {"results": results}
#     return handler


def health_handler() -> Callable:
    def handler():
        return {"status": "ok"}
    return handler