"""Tests for the embedding-based scorer."""

from __future__ import annotations

from unittest.mock import MagicMock, patch
import numpy as np
import pytest


# Test data
RELEVANT_ARTICLE = {
    "title": "Mechanistic Interpretability: Circuit Analysis in GPT-2",
    "summary": "We use activation patching to identify attention head circuits responsible for indirect object identification. This work extends prior mechanistic interpretability research.",
}

IRRELEVANT_ARTICLE = {
    "title": "TechCorp Announces $50M Funding Round",
    "summary": "Startup funding news. CEO excited about expansion. Will hire 100 engineers.",
}

YOUTH_PSYCH_ARTICLE = {
    "title": "Longitudinal Study: Social Media and Adolescent Development",
    "summary": "Three-year study of 5000 teenagers examining social media effects on identity formation and psychological well-being.",
}


class MockSentenceTransformer:
    """Mock sentence transformer that returns deterministic embeddings."""
    
    def __init__(self, model_name: str):
        self.model_name = model_name
        self._embedding_dim = 384
        np.random.seed(42)  # Deterministic for tests
    
    def encode(
        self,
        texts: str | list[str],
        convert_to_numpy: bool = True,
        show_progress_bar: bool = True,
    ) -> np.ndarray:
        """Generate deterministic embeddings based on text content."""
        if isinstance(texts, str):
            texts = [texts]
        
        embeddings = []
        for text in texts:
            # Create embeddings that reflect relevance
            text_lower = text.lower()
            
            # Base random embedding (seeded)
            np.random.seed(hash(text) % 2**32)
            base = np.random.randn(self._embedding_dim)
            
            # Add signal for relevant keywords
            relevance_keywords = [
                "interpretability", "circuit", "activation", "alignment",
                "adolescent", "teenager", "longitudinal", "cognitive",
                "attention", "arxiv", "empirical", "methodology"
            ]
            noise_keywords = [
                "funding", "startup", "ceo", "hiring", "product launch",
                "press release", "earnings"
            ]
            
            relevance_boost = sum(1 for kw in relevance_keywords if kw in text_lower)
            noise_penalty = sum(1 for kw in noise_keywords if kw in text_lower)
            
            # Modify embedding magnitude based on relevance
            # This creates separation in cosine similarity
            if relevance_boost > 0:
                base = base + np.ones(self._embedding_dim) * 0.3 * relevance_boost
            if noise_penalty > 0:
                base = base - np.ones(self._embedding_dim) * 0.2 * noise_penalty
            
            # Normalize
            base = base / (np.linalg.norm(base) + 1e-9)
            embeddings.append(base)
        
        return np.array(embeddings)


@pytest.fixture
def mock_model():
    """Fixture that patches the sentence-transformers import."""
    with patch.dict("sys.modules", {"sentence_transformers": MagicMock()}):
        import sys
        mock_st = sys.modules["sentence_transformers"]
        mock_st.SentenceTransformer = MockSentenceTransformer
        yield mock_st


@pytest.fixture
def reset_cache():
    """Reset the module-level cache before each test."""
    import evaluate_embeddings
    evaluate_embeddings._model = None
    evaluate_embeddings._anchor_embeddings = None
    evaluate_embeddings._negative_embeddings = None
    yield


class TestEmbeddingDimensions:
    """Test that embeddings have correct dimensions."""
    
    def test_embedding_dimension_constant(self):
        """Verify the expected embedding dimension constant."""
        from evaluate_embeddings import EMBEDDING_DIM
        assert EMBEDDING_DIM == 384
    
    def test_mock_embedding_dimensions(self, mock_model):
        """Test that mock model returns correct dimensions."""
        model = MockSentenceTransformer("test")
        embedding = model.encode("test text")
        assert embedding.shape == (1, 384)
    
    def test_batch_embedding_dimensions(self, mock_model):
        """Test batch encoding dimensions."""
        model = MockSentenceTransformer("test")
        texts = ["text one", "text two", "text three"]
        embeddings = model.encode(texts)
        assert embeddings.shape == (3, 384)


class TestCosineSimilarity:
    """Test cosine similarity computation."""
    
    def test_cosine_similarity_identical_vectors(self):
        """Identical vectors should have similarity of 1."""
        from evaluate_embeddings import cosine_similarity
        vec = np.array([1.0, 0.0, 0.0])
        matrix = np.array([[1.0, 0.0, 0.0]])
        sim = cosine_similarity(vec, matrix)
        assert np.isclose(sim[0], 1.0, atol=1e-6)
    
    def test_cosine_similarity_orthogonal_vectors(self):
        """Orthogonal vectors should have similarity of 0."""
        from evaluate_embeddings import cosine_similarity
        vec = np.array([1.0, 0.0, 0.0])
        matrix = np.array([[0.0, 1.0, 0.0]])
        sim = cosine_similarity(vec, matrix)
        assert np.isclose(sim[0], 0.0, atol=1e-6)
    
    def test_cosine_similarity_opposite_vectors(self):
        """Opposite vectors should have similarity of -1."""
        from evaluate_embeddings import cosine_similarity
        vec = np.array([1.0, 0.0, 0.0])
        matrix = np.array([[-1.0, 0.0, 0.0]])
        sim = cosine_similarity(vec, matrix)
        assert np.isclose(sim[0], -1.0, atol=1e-6)
    
    def test_cosine_similarity_range(self):
        """Cosine similarity should always be between -1 and 1."""
        from evaluate_embeddings import cosine_similarity
        np.random.seed(123)
        vec = np.random.randn(384)
        matrix = np.random.randn(10, 384)
        sims = cosine_similarity(vec, matrix)
        assert all(-1 <= s <= 1 for s in sims)
    
    def test_cosine_similarity_batch(self):
        """Test similarity against multiple anchors."""
        from evaluate_embeddings import cosine_similarity
        vec = np.array([1.0, 1.0, 0.0])
        matrix = np.array([
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [1.0, 1.0, 0.0],
        ])
        sims = cosine_similarity(vec, matrix)
        assert len(sims) == 3
        # Third vector is parallel, should have highest sim
        assert sims[2] > sims[0]
        assert sims[2] > sims[1]


class TestSimilarityToScore:
    """Test the similarity-to-score mapping."""
    
    def test_score_range(self):
        """Scores should always be between 1 and 10."""
        from evaluate_embeddings import similarity_to_score
        for pos_sim in np.linspace(-0.5, 1.0, 20):
            for neg_sim in np.linspace(0, 0.5, 10):
                score = similarity_to_score(pos_sim, neg_sim)
                assert 1 <= score <= 10
    
    def test_high_similarity_high_score(self):
        """High positive similarity should produce high scores."""
        from evaluate_embeddings import similarity_to_score
        score = similarity_to_score(0.6, 0.1)
        assert score >= 8
    
    def test_low_similarity_low_score(self):
        """Low positive similarity should produce low scores."""
        from evaluate_embeddings import similarity_to_score
        score = similarity_to_score(0.05, 0.1)
        assert score <= 3
    
    def test_negative_anchors_reduce_score(self):
        """High negative similarity should reduce scores."""
        from evaluate_embeddings import similarity_to_score
        high_neg = similarity_to_score(0.4, 0.5)
        low_neg = similarity_to_score(0.4, 0.1)
        assert high_neg < low_neg


class TestArticleScoring:
    """Test article scoring with mocked model."""
    
    def test_relevant_scores_higher_than_irrelevant(self, mock_model, reset_cache):
        """Clearly relevant articles should score higher than irrelevant ones."""
        from evaluate_embeddings import score_batch_embeddings
        
        articles = [
            RELEVANT_ARTICLE.copy(),
            IRRELEVANT_ARTICLE.copy(),
        ]
        scored = score_batch_embeddings(articles)
        
        assert scored[0]["score"] > scored[1]["score"]
    
    def test_score_batch_returns_all_entries(self, mock_model, reset_cache):
        """Batch scoring should return same number of entries."""
        from evaluate_embeddings import score_batch_embeddings
        
        articles = [
            RELEVANT_ARTICLE.copy(),
            IRRELEVANT_ARTICLE.copy(),
            YOUTH_PSYCH_ARTICLE.copy(),
        ]
        scored = score_batch_embeddings(articles)
        
        assert len(scored) == 3
    
    def test_score_batch_adds_required_fields(self, mock_model, reset_cache):
        """Scored entries should have score, reason, and debug info."""
        from evaluate_embeddings import score_batch_embeddings
        
        articles = [RELEVANT_ARTICLE.copy()]
        scored = score_batch_embeddings(articles)
        
        assert "score" in scored[0]
        assert "reason" in scored[0]
        assert "embedding_debug" in scored[0]
    
    def test_score_batch_empty_list(self, mock_model, reset_cache):
        """Empty list should return empty list."""
        from evaluate_embeddings import score_batch_embeddings
        
        scored = score_batch_embeddings([])
        assert scored == []
    
    def test_score_single_article(self, mock_model, reset_cache):
        """Test single article scoring function."""
        from evaluate_embeddings import score_article
        
        score, reason, debug = score_article(
            RELEVANT_ARTICLE["title"],
            RELEVANT_ARTICLE["summary"],
        )
        
        assert 1 <= score <= 10
        assert isinstance(reason, str)
        assert "max_positive_sim" in debug
        assert "max_negative_sim" in debug


class TestAnchorTexts:
    """Test anchor text configuration."""
    
    def test_anchor_texts_not_empty(self):
        """Anchor texts list should not be empty."""
        from evaluate_embeddings import ANCHOR_TEXTS
        assert len(ANCHOR_TEXTS) > 0
    
    def test_negative_anchors_not_empty(self):
        """Negative anchors list should not be empty."""
        from evaluate_embeddings import NEGATIVE_ANCHORS
        assert len(NEGATIVE_ANCHORS) > 0
    
    def test_anchor_texts_are_strings(self):
        """All anchors should be non-empty strings."""
        from evaluate_embeddings import ANCHOR_TEXTS, NEGATIVE_ANCHORS
        for anchor in ANCHOR_TEXTS + NEGATIVE_ANCHORS:
            assert isinstance(anchor, str)
            assert len(anchor) > 0


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_title_and_summary(self, mock_model, reset_cache):
        """Handle empty title and summary gracefully."""
        from evaluate_embeddings import score_batch_embeddings
        
        articles = [{"title": "", "summary": ""}]
        scored = score_batch_embeddings(articles)
        
        assert len(scored) == 1
        assert 1 <= scored[0]["score"] <= 10
    
    def test_missing_summary_key(self, mock_model, reset_cache):
        """Handle missing summary key."""
        from evaluate_embeddings import score_batch_embeddings
        
        articles = [{"title": "Test title"}]
        scored = score_batch_embeddings(articles)
        
        assert len(scored) == 1
        assert "score" in scored[0]
    
    def test_very_long_text_truncated(self, mock_model, reset_cache):
        """Very long text should be handled (truncated internally)."""
        from evaluate_embeddings import score_batch_embeddings
        
        articles = [{
            "title": "A" * 1000,
            "summary": "B" * 5000,
        }]
        scored = score_batch_embeddings(articles)
        
        assert len(scored) == 1
        assert "score" in scored[0]
