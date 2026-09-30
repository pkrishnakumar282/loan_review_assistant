from rank_bm25 import BM25Okapi

from config import (
    TOP_K_VECTOR,
    TOP_K_KEYWORD,
    TOP_K_FINAL
)


class HybridSearch:

    def __init__(self, vector_store):

        self.vector_store = vector_store

        self.chunks = vector_store.documents

        tokenized_documents = [
            chunk["text"].lower().split()
            for chunk in self.chunks
        ]

        self.bm25 = BM25Okapi(
            tokenized_documents
        )

    def search(self, query):

        # -----------------------------
        # VECTOR SEARCH
        # -----------------------------

        vector_results = self.vector_store.search(
            query,
            TOP_K_VECTOR
        )

        # -----------------------------
        # BM25 KEYWORD SEARCH
        # -----------------------------

        query_tokens = query.lower().split()

        keyword_scores = self.bm25.get_scores(
            query_tokens
        )

        keyword_indices = sorted(
            range(len(keyword_scores)),
            key=lambda i: keyword_scores[i],
            reverse=True
        )[:TOP_K_KEYWORD]

        # -----------------------------
        # MERGE RESULTS
        # -----------------------------

        combined = {}

        for rank, result in enumerate(
            vector_results
        ):

            chunk_id = result["chunk_id"]

            combined.setdefault(
                chunk_id,
                {
                    "document": result,
                    "score": 0
                }
            )

            combined[chunk_id]["score"] += (
                1 / (rank + 1)
            )

        for rank, index in enumerate(
            keyword_indices
        ):

            chunk = self.chunks[index]

            chunk_id = chunk["chunk_id"]

            combined.setdefault(
                chunk_id,
                {
                    "document": chunk,
                    "score": 0
                }
            )

            combined[chunk_id]["score"] += (
                1 / (rank + 1)
            )

        # -----------------------------
        # SORT
        # -----------------------------

        ranked = sorted(
            combined.values(),
            key=lambda x: x["score"],
            reverse=True
        )

        results = []

        for item in ranked[:TOP_K_FINAL]:

            result = item["document"].copy()

            result["hybrid_score"] = item["score"]

            results.append(result)

        return results