from qdrant_client import QdrantClient
from qdrant_client.http import models


def create_indexes(client: QdrantClient, collection_name: str) -> None:
    indexes = [
        ("language", models.PayloadSchemaType.KEYWORD),
        (
            "lectureTitle",
            models.TextIndexParams(
                type=models.TextIndexType.TEXT,
                tokenizer=models.TokenizerType.WORD,
                lowercase=True,
                phrase_matching=True,
            ),
        ),
    ]

    for field_name, schema in indexes:
        client.create_payload_index(
            collection_name=collection_name,
            field_name=field_name,
            field_schema=schema,
        )