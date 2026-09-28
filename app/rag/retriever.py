from typing import List, Dict


def keyword_retrieve(query: str, documents: List[Dict], top_k: int = 5) -> List[Dict]:
    """
    Lightweight baseline retriever.

    Replace this with BM25 + vector search + reranking in a future iteration.
    """
    query_terms = set(query.lower().split())
    scored = []

    for doc in documents:
        terms = set(doc["text"].lower().split())
        score = len(query_terms.intersection(terms))
        scored.append({**doc, "score": score})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]
