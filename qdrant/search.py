from qdrant_client.http.models import Document, Filter, FieldCondition , MatchValue , MatchPhrase
from qdrant import QdrantManager


def search(qdrant: QdrantManager, query: str, top_k: int = 5) -> list[dict]:
    response = qdrant.client.query_points(
        collection_name=qdrant.collection_name,
        query=Document(text=query, model=qdrant.embedding_model),
        limit=top_k,
    )
    return [{"score": p.score, **p.payload} for p in response.points]


def search_by_language(qdrant: QdrantManager, query: str, language: str, top_k: int = 5) -> list[dict]:
    language_filter = Filter(
        must=[FieldCondition(key="language", match=MatchValue(value=language))]
    )
    response = qdrant.client.query_points(
        collection_name=qdrant.collection_name,
        query=Document(text=query, model=qdrant.embedding_model),
        limit=top_k,
        query_filter=language_filter,
    )
    return [{"score": p.score, **p.payload} for p in response.points]


# def keyword_search_lecture(qdrant: QdrantManager, keyword: str, top_k: int = 5) -> list[dict]:
#     # Partial/substring match filter
#     keyword_filter = Filter(
#         must=[FieldCondition(key="lectureTitle", match=MatchPhrase(phrase=keyword))]
#     )
    
#     # Scroll through the collection using the filter
#     records, _ = qdrant.client.scroll(
#         collection_name=qdrant.collection_name,
#         scroll_filter=keyword_filter,
#         limit=top_k,
#     )
    
#     return [{"id": p.id, **p.payload} for p in records]