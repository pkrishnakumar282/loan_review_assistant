import os
import json

import faiss
import numpy as np

from src.embeddings import EmbeddingModel


class VectorStore:

    def __init__(self):

        self.embedding_model = EmbeddingModel()

        self.index = None
        self.documents = []

    def build(self, chunks):

        self.documents = chunks

        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        embeddings = self.embedding_model.encode(texts)

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(dimension)

        self.index.add(
            embeddings.astype(np.float32)
        )

    def search(self, query, top_k=8):

        query_embedding = self.embedding_model.encode(
            [query]
        )

        scores, indices = self.index.search(
            query_embedding.astype(np.float32),
            top_k
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0]
        ):

            if index == -1:
                continue

            result = self.documents[index].copy()

            result["vector_score"] = float(score)

            results.append(result)

        return results

    def save(self, directory):

        os.makedirs(
            directory,
            exist_ok=True
        )

        faiss.write_index(
            self.index,
            os.path.join(
                directory,
                "faiss.index"
            )
        )

        with open(
            os.path.join(
                directory,
                "documents.json"
            ),
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.documents,
                file,
                ensure_ascii=False,
                indent=2
            )

    def load(self, directory):

        self.index = faiss.read_index(
            os.path.join(
                directory,
                "faiss.index"
            )
        )

        with open(
            os.path.join(
                directory,
                "documents.json"
            ),
            "r",
            encoding="utf-8"
        ) as file:

            self.documents = json.load(file)