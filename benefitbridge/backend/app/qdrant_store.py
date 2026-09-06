import json
from pathlib import Path
from typing import List
import numpy as np
from qdrant_client import QdrantClient, models
from sklearn.feature_extraction.text import TfidfVectorizer
from .config import settings

BASE = Path(__file__).resolve().parents[2]
DATA = BASE / "data" / "schemes.json"
LOCAL_QDRANT = BASE / "qdrant_storage"

class SchemeStore:
    def __init__(self):
        self.schemes = json.loads(DATA.read_text(encoding="utf-8"))
        self.vectorizer = TfidfVectorizer(ngram_range=(1,2), min_df=1, sublinear_tf=True)
        texts = [self._text(s) for s in self.schemes]
        matrix = self.vectorizer.fit_transform(texts)
        self.matrix = matrix
        self.dim = matrix.shape[1]
        if settings.qdrant_url:
            self.client = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key or None)
        else:
            self.client = QdrantClient(path=str(LOCAL_QDRANT))
        self._ensure_collection()

    def _text(self, s):
        return " ".join([
            s["name"], s["short_description"], s["category"], s["benefit"],
            s.get("keywords", ""), " ".join(s.get("life_events", [])),
            " ".join(s.get("occupations", [])), s.get("state", "")
        ])

    def _ensure_collection(self):
        try:
            exists = self.client.collection_exists(settings.qdrant_collection)
        except TypeError:
            exists = self.client.collection_exists(collection_name=settings.qdrant_collection)
        if not exists:
            self.client.create_collection(
                collection_name=settings.qdrant_collection,
                vectors_config=models.VectorParams(size=self.dim, distance=models.Distance.COSINE),
            )
            self._upsert()
        else:
            info = self.client.get_collection(settings.qdrant_collection)
            count = getattr(info, "points_count", 0) or 0
            if count == 0:
                self._upsert()

    def _upsert(self):
        points = []
        for idx, scheme in enumerate(self.schemes):
            vec = self.matrix[idx].toarray()[0].astype(float).tolist()
            points.append(models.PointStruct(id=idx + 1, vector=vec, payload={"scheme_id": scheme["id"]}))
        self.client.upsert(collection_name=settings.qdrant_collection, points=points)

    def search(self, query: str, limit: int = 8) -> List[dict]:
        q = self.vectorizer.transform([query]).toarray()[0].astype(float).tolist()
        try:
            hits = self.client.query_points(
                collection_name=settings.qdrant_collection,
                query=q,
                limit=limit,
                with_payload=True,
            ).points
        except Exception:
            # Compatible fallback for older qdrant-client versions.
            hits = self.client.search(collection_name=settings.qdrant_collection, query_vector=q, limit=limit, with_payload=True)
        by_id = {s["id"]: s for s in self.schemes}
        result = []
        for h in hits:
            sid = h.payload.get("scheme_id") if h.payload else None
            if sid in by_id:
                item = dict(by_id[sid])
                item["retrieval_score"] = float(getattr(h, "score", 0.0))
                result.append(item)
        return result
