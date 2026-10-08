from typing import List, Dict, Any
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from app.nlp.base_embedder import BaseEmbedder
from app.nlp.sentence_transformer_embedder import SentenceTransformerEmbedder

def map_similarity_to_score(similarity: float) -> int:
    """
    Maps continuous Cosine Similarity score [0.0 - 1.0] to OBE correlation level (1, 2, 3).
    - Similarity >= 0.55 -> 3 (Substantial)
    - Similarity >= 0.35 -> 2 (Moderate)
    - Similarity < 0.35  -> 1 (Slight)
    """
    if similarity >= 0.55:
        return 3
    elif similarity >= 0.35:
        return 2
    else:
        return 1

def generate_copo_matrix(
    co_records: List[Dict[str, str]],
    po_records: List[Dict[str, str]],
    embedder: BaseEmbedder = None
) -> Dict[str, Any]:
    """
    Generates CO-PO correlation matrix using semantic NLP similarity.
    co_records: List of dicts with 'CO Number' and 'Statement'
    po_records: List of dicts with 'PO Number' and 'Statement'
    """
    if embedder is None:
        embedder = SentenceTransformerEmbedder()

    co_statements = [r["Statement"] for r in co_records]
    po_statements = [r["Statement"] for r in po_records]

    co_labels = [r["CO Number"] for r in co_records]
    po_labels = [r["PO Number"] for r in po_records]

    # Generate Embeddings
    co_embeddings = embedder.get_embeddings(co_statements)
    po_embeddings = embedder.get_embeddings(po_statements)

    # Compute Cosine Similarity Matrix (Shape: len(CO) x len(PO))
    sim_matrix = cosine_similarity(co_embeddings, po_embeddings)

    matrix_rows = []
    for i, co_label in enumerate(co_labels):
        scores = {}
        raw_similarities = {}
        for j, po_label in enumerate(po_labels):
            raw_sim = float(sim_matrix[i][j])
            score = map_similarity_to_score(raw_sim)
            scores[po_label] = score
            raw_similarities[po_label] = round(raw_sim, 4)

        matrix_rows.append({
            "co": co_label,
            "statement": co_statements[i],
            "scores": scores,
            "rawSimilarities": raw_similarities
        })

    return {
        "poList": po_labels,
        "poStatements": dict(zip(po_labels, po_statements)),
        "matrix": matrix_rows
    }
