from abc import ABC, abstractmethod
from typing import List
import numpy as np

class BaseEmbedder(ABC):
    """
    Abstract Base Class for text embedding models.
    Allows easy swapping between sentence-transformers, OpenAI, or other custom NLP models.
    """
    
    @abstractmethod
    def get_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Takes a list of text statements and returns a 2D numpy array of embeddings.
        """
        pass
