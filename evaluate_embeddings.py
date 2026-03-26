"""
Embedding-based article scorer using sentence-transformers.

This module provides an alternative scoring path using cosine similarity
between article embeddings and relevance anchor texts extracted from profile.py.
Works offline with no API key required.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from sentence_transformers import SentenceTransformer

# Anchor texts extracted from profile.py relevance criteria
# These represent the core interests for similarity matching
ANCHOR_TEXTS: list[str] = [
    # Core domains (from reading interests)
    "AI capabilities, LLM mechanisms, capability evaluations, benchmarks, failure modes",
    "AI safety, alignment, mechanistic interpretability, circuits, activation patching, superposition, RLHF, scalable oversight, constitutional AI, deceptive alignment",
    "Cognitive effects of technology, attention, memory, screens and algorithms affecting minds, enactivism",
    "Adolescent cyberpsychology, social media effects on youth, identity development online, parasocial relationships, longitudinal studies",
    "Future of knowledge work, researchers and writers when thinking gets automated",
    
    # High-signal indicators (from 8-10 criteria)
    "New conceptual framework, superposition hypothesis, mechanistic interpretability circuits",
    "Empirical study with novel counterintuitive findings, longitudinal youth cognition platform effects",
    "AI lab research, senior researcher, insider perspective, not journalism",
    "Mechanistic interpretability, circuit analysis, activation steering, probing, RLHF internals",
    "HCI empirical study, real participants, children adolescents, novel methodology",
    "arXiv preprint cs.HC cs.CY cs.AI cs.LG with policy or cognitive implications",
    "Falsifiable claim with evidence that could change priors",
    "Cross-disciplinary philosophy HCI cognitive science platform design economics child rights",
    
    # Source signals
    "Alignment Forum, Distill, ACM CHI CSCW FAccT, Oxford Internet Institute, Berkman Klein",
    "Paul Christiano, Neel Nanda, Chris Olah, Victoria Krakovna, alignment researchers",
]

# Negative anchors - articles similar to these should score lower
NEGATIVE_ANCHORS: list[str] = [
    "NGO newsletter, advocacy update, press release, government statement",
    "Geopolitics, international relations, diplomatic summit",
    "Country-specific human rights incident, journalist hacked, political prisoner",
    "News event about company, person, legislation, will be outdated",
    "Product launch, funding round, earnings report",
    "Self-help listicle, productivity tips, thought leader",
]

MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDING_DIM = 384  # Dimension for all-MiniLM-L6-v2

# Global model cache
_model: SentenceTransformer | None = None
_anchor_embeddings: np.ndarray | None = None
_negative_embeddings: np.ndarray | None = None


def load_model() -> "SentenceTransformer":
    """Load the sentence-transformer model (cached after first call)."""
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        logging.info("Loading sentence-transformer model: %s", MODEL_NAME)
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def get_anchor_embeddings() -> tuple[np.ndarray, np.ndarray]:
    """Compute embeddings for anchor texts (cached after first call)."""
    global _anchor_embeddings, _negative_embeddings
    if _anchor_embeddings is None:
        model = load_model()
        _anchor_embeddings = model.encode(ANCHOR_TEXTS, convert_to_numpy=True)
        _negative_embeddings = model.encode(NEGATIVE_ANCHORS, convert_to_numpy=True)
    return _anchor_embeddings, _negative_embeddings


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Compute cosine similarity between vectors a and matrix b."""
    # Normalize vectors
    a_norm = a / (np.linalg.norm(a) + 1e-9)
    b_norm = b / (np.linalg.norm(b, axis=1, keepdims=True) + 1e-9)
    return np.dot(b_norm, a_norm)


def similarity_to_score(
    positive_sim: float,
    negative_sim: float,
    min_score: int = 1,
    max_score: int = 10,
) -> int:
    """
    Convert similarity scores to a 1-10 relevance score.
    
    Uses the difference between max positive and max negative similarity,
    then maps to score range with calibrated thresholds.
    """
    # Net similarity: positive signal minus negative signal
    net_sim = positive_sim - (negative_sim * 0.5)  # Negative anchors weighted less
    
    # Empirical thresholds for calibration
    # MiniLM similarities typically range from 0.0-0.6 for related content
    if net_sim >= 0.55:
        return 10
    elif net_sim >= 0.45:
        return 9
    elif net_sim >= 0.38:
        return 8
    elif net_sim >= 0.32:
        return 7
    elif net_sim >= 0.26:
        return 6
    elif net_sim >= 0.20:
        return 5
    elif net_sim >= 0.15:
        return 4
    elif net_sim >= 0.10:
        return 3
    elif net_sim >= 0.05:
        return 2
    else:
        return 1


def score_article(title: str, summary: str) -> tuple[int, str, dict[str, float]]:
    """
    Score a single article using embedding similarity.
    
    Returns:
        Tuple of (score, reason, debug_info)
        - score: 1-10 relevance score
        - reason: explanation of the score
        - debug_info: dict with similarity values for analysis
    """
    model = load_model()
    pos_anchors, neg_anchors = get_anchor_embeddings()
    
    # Combine title and summary for embedding
    text = f"{title}. {summary}"[:512]  # Truncate to model limit
    embedding = model.encode(text, convert_to_numpy=True)
    
    # Ensure embedding is 1D (single text)
    if embedding.ndim == 2:
        embedding = embedding[0]
    
    # Compute similarities
    pos_sims = cosine_similarity(embedding, pos_anchors)
    neg_sims = cosine_similarity(embedding, neg_anchors)
    
    max_pos_sim = float(np.max(pos_sims))
    max_neg_sim = float(np.max(neg_sims))
    avg_pos_sim = float(np.mean(pos_sims))
    
    # Find which anchor matched best
    best_anchor_idx = int(np.argmax(pos_sims))
    best_anchor = ANCHOR_TEXTS[best_anchor_idx][:80]
    
    score = similarity_to_score(max_pos_sim, max_neg_sim)
    
    reason = f"Embedding similarity {max_pos_sim:.2f} to '{best_anchor}...'"
    
    debug_info = {
        "max_positive_sim": max_pos_sim,
        "max_negative_sim": max_neg_sim,
        "avg_positive_sim": avg_pos_sim,
        "best_anchor_idx": best_anchor_idx,
        "embedding_norm": float(np.linalg.norm(embedding)),
    }
    
    return score, reason, debug_info


def score_batch_embeddings(
    entries: list[dict[str, str | int]],
) -> list[dict[str, str | int]]:
    """
    Score a batch of entries using embedding similarity.
    
    Args:
        entries: List of article dicts with 'title' and 'summary' keys
        
    Returns:
        Same entries with 'score', 'reason', and 'embedding_debug' added
    """
    if not entries:
        return entries
    
    model = load_model()
    pos_anchors, neg_anchors = get_anchor_embeddings()
    
    # Batch encode all articles
    texts = [
        f"{e.get('title', '')}. {e.get('summary', '')}"[:512]
        for e in entries
    ]
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
    
    for i, (entry, embedding) in enumerate(zip(entries, embeddings)):
        pos_sims = cosine_similarity(embedding, pos_anchors)
        neg_sims = cosine_similarity(embedding, neg_anchors)
        
        max_pos_sim = float(np.max(pos_sims))
        max_neg_sim = float(np.max(neg_sims))
        
        best_anchor_idx = int(np.argmax(pos_sims))
        best_anchor = ANCHOR_TEXTS[best_anchor_idx][:60]
        
        score = similarity_to_score(max_pos_sim, max_neg_sim)
        
        entry["score"] = score
        entry["reason"] = f"Similarity {max_pos_sim:.2f} to '{best_anchor}...'"
        entry["embedding_debug"] = {
            "max_pos": max_pos_sim,
            "max_neg": max_neg_sim,
            "anchor_idx": best_anchor_idx,
        }
    
    return entries


def get_embedding(text: str) -> np.ndarray:
    """Get embedding for a single text (for analysis/visualization)."""
    model = load_model()
    return model.encode(text, convert_to_numpy=True)


def get_embeddings_batch(texts: list[str]) -> np.ndarray:
    """Get embeddings for multiple texts (for analysis/visualization)."""
    model = load_model()
    return model.encode(texts, convert_to_numpy=True, show_progress_bar=False)


# CLI interface for standalone testing
if __name__ == "__main__":
    
    test_articles = [
        {
            "title": "Mechanistic Interpretability of GPT-2: Identifying Attention Head Circuits",
            "summary": "We present a systematic analysis of attention head circuits in GPT-2, using activation patching to identify specific heads responsible for indirect object identification.",
        },
        {
            "title": "New funding round for AI startup",
            "summary": "TechCorp announced $50M Series B funding today. CEO says they will expand to new markets.",
        },
        {
            "title": "Longitudinal Study: Social Media Use and Adolescent Well-being Over 3 Years",
            "summary": "We tracked 5000 teenagers over three years measuring social media use and psychological outcomes. Contrary to cross-sectional studies, we find nuanced effects varying by platform type.",
        },
    ]
    
    print("Testing embedding-based scorer...\n")
    scored = score_batch_embeddings(test_articles)
    
    for article in scored:
        print(f"Score: {article['score']}/10")
        print(f"Title: {article['title']}")
        print(f"Reason: {article['reason']}")
        print(f"Debug: {article.get('embedding_debug')}")
        print("-" * 60)
