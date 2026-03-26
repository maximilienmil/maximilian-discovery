"""Tests for LLM scoring pipeline in discovery.py."""

import json
from unittest.mock import MagicMock, patch

from discovery import score_batch, score_all


class MockChoice:
    """Mock for OpenAI response choice."""

    def __init__(self, content: str) -> None:
        self.message = MagicMock()
        self.message.content = content


class MockResponse:
    """Mock for OpenAI API response."""

    def __init__(self, content: str) -> None:
        self.choices = [MockChoice(content)]


class TestScoreBatch:
    """Tests for score_batch function."""

    def test_returns_valid_json_format(self) -> None:
        """Scoring returns entries with index, score, reason."""
        entries = [
            {"title": "Test Article", "summary": "A test summary", "source": "test.com"}
        ]
        mock_response = json.dumps([{"index": 0, "score": 7, "reason": "Test reason"}])
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = MockResponse(mock_response)

        result = score_batch(entries, mock_client)

        assert len(result) == 1
        assert result[0]["score"] == 7
        assert result[0]["reason"] == "Test reason"

    def test_scores_in_valid_range(self) -> None:
        """Scores are within 1-10 range."""
        entries = [
            {"title": "High Score", "summary": "Important", "source": "test.com"},
            {"title": "Low Score", "summary": "Not important", "source": "test.com"},
        ]
        mock_response = json.dumps([
            {"index": 0, "score": 9, "reason": "High value"},
            {"index": 1, "score": 2, "reason": "Low value"},
        ])
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = MockResponse(mock_response)

        result = score_batch(entries, mock_client)

        for entry in result:
            assert 1 <= entry["score"] <= 10

    def test_handles_empty_entries(self) -> None:
        """Empty entries list returns empty list."""
        mock_client = MagicMock()
        result = score_batch([], mock_client)
        assert result == []
        mock_client.chat.completions.create.assert_not_called()

    def test_handles_markdown_fenced_json(self) -> None:
        """Handles LLM response wrapped in markdown code fences."""
        entries = [{"title": "Test", "summary": "Test", "source": "test.com"}]
        mock_response = '```json\n[{"index": 0, "score": 8, "reason": "Good"}]\n```'
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = MockResponse(mock_response)

        result = score_batch(entries, mock_client)

        assert result[0]["score"] == 8

    def test_handles_api_error_gracefully(self) -> None:
        """API errors result in score 0 for all entries."""
        entries = [{"title": "Test", "summary": "Test", "source": "test.com"}]
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")

        with patch("discovery.time.sleep"):  # Skip retry delays
            result = score_batch(entries, mock_client)

        assert result[0].get("score", 0) == 0
        assert "scoring failed" in result[0].get("reason", "")

    def test_handles_invalid_json_response(self) -> None:
        """Invalid JSON from LLM is handled gracefully."""
        entries = [{"title": "Test", "summary": "Test", "source": "test.com"}]
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = MockResponse("not valid json")

        with patch("discovery.time.sleep"):
            result = score_batch(entries, mock_client)

        assert result[0].get("score", 0) == 0

    def test_handles_partial_scores(self) -> None:
        """Entries without scores in response get default score."""
        entries = [
            {"title": "Scored", "summary": "Test", "source": "test.com"},
            {"title": "Unscored", "summary": "Test", "source": "test.com"},
        ]
        mock_response = json.dumps([{"index": 0, "score": 7, "reason": "Good"}])
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = MockResponse(mock_response)

        result = score_batch(entries, mock_client)

        assert result[0]["score"] == 7
        # Second entry should not have a score key set by the function
        assert result[1].get("score") is None or result[1].get("score", 0) == 0


class TestScoreAll:
    """Tests for score_all function."""

    @patch("discovery.OpenAI")
    @patch.dict("os.environ", {"GROQ_API_KEY": "test-key"})
    def test_batches_entries(self, mock_openai_class: MagicMock) -> None:
        """Entries are processed in batches of 25."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        # Create 30 entries to trigger 2 batches
        entries = [
            {"title": f"Article {i}", "summary": f"Summary {i}", "source": "test.com"}
            for i in range(30)
        ]

        # Mock response that returns scores for any batch
        def create_response(*args, **kwargs):
            return MockResponse(json.dumps([
                {"index": i, "score": 5, "reason": "OK"}
                for i in range(25)  # Max batch size
            ]))

        mock_client.chat.completions.create.side_effect = create_response

        with patch("discovery.time.sleep"):
            result = score_all(entries)

        # Should have called API twice (25 + 5 entries)
        assert mock_client.chat.completions.create.call_count == 2
        assert len(result) == 30

    @patch("discovery.OpenAI")
    @patch.dict("os.environ", {"GROQ_API_KEY": "test-key"})
    def test_empty_entries_list(self, mock_openai_class: MagicMock) -> None:
        """Empty entries list doesn't call API."""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        with patch("discovery.time.sleep"):
            result = score_all([])

        mock_client.chat.completions.create.assert_not_called()
        assert result == []
