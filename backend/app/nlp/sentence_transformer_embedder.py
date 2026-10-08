from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from app.nlp.base_embedder import BaseEmbedder

class SentenceTransformerEmbedder(BaseEmbedder):
    """
    SentenceTransformer implementation of BaseEmbedder using HuggingFace 'all-MiniLM-L6-v2'.
    """
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model = None

    @property
    def model(self) -> SentenceTransformer:
        # Lazy loading of model to optimize startup time
        if self._model is None:
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def get_embeddings(self, texts: List[str]) -> np.ndarray:
        if not texts:
            return np.array([])
        embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        return embeddings
