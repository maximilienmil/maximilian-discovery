"""Tests for digest generation in discovery.py."""

from discovery import generate_digest


class TestGenerateDigest:
    """Tests for generate_digest function."""

    def test_produces_valid_markdown(self) -> None:
        """Output is valid markdown with header."""
        entries = [
            {
                "title": "Test Article",
                "link": "https://example.com/test",
                "source": "example.com",
                "source_type": "discovery",
                "published": "2024-01-15",
                "score": 9,
                "reason": "Important finding",
            }
        ]
        result = generate_digest(entries, total_checked=10)

        assert result.startswith("# Discovery Digest")
        assert "Test Article" in result
        assert "https://example.com/test" in result

    def test_must_read_threshold(self) -> None:
        """Articles with score 8-10 appear in Must Read section."""
        entries = [
            {
                "title": "High Score Article",
                "link": "https://example.com/high",
                "source": "example.com",
                "source_type": "discovery",
                "published": "2024-01-15",
                "score": 9,
                "reason": "Very important",
            }
        ]
        result = generate_digest(entries, total_checked=5)

        assert "## Must Read" in result
        assert "High Score Article" in result

    def test_worth_look_threshold(self) -> None:
        """Articles with score 5-7 appear in Worth a Look section."""
        entries = [
            {
                "title": "Medium Score Article",
                "link": "https://example.com/medium",
                "source": "example.com",
                "source_type": "discovery",
                "published": "2024-01-15",
                "score": 6,
                "reason": "Somewhat interesting",
            }
        ]
        result = generate_digest(entries, total_checked=5)

        assert "## Worth a Look" in result
        assert "Medium Score Article" in result

    def test_low_score_excluded(self) -> None:
        """Articles with score 1-4 are not included."""
        entries = [
            {
                "title": "Low Score Article",
                "link": "https://example.com/low",
                "source": "example.com",
                "source_type": "discovery",
                "published": "2024-01-15",
                "score": 3,
                "reason": "Not relevant",
            }
        ]
        result = generate_digest(entries, total_checked=5)

        assert "Low Score Article" not in result

    def test_technical_section_separate(self) -> None:
        """Technical articles appear in Research & Technical section."""
        entries = [
            {
                "title": "arXiv Paper",
                "link": "https://arxiv.org/abs/1234",
                "source": "arxiv.org",
                "source_type": "technical",
                "published": "2024-01-15",
                "score": 8,
                "reason": "Novel method",
            }
        ]
        result = generate_digest(entries, total_checked=5)

        assert "## Research & Technical" in result
        assert "arXiv Paper" in result

    def test_podcast_section_separate(self) -> None:
        """Podcast episodes appear in Podcast Episodes section."""
        entries = [
            {
                "title": "Great Podcast Episode",
                "link": "https://podcast.com/ep1",
                "source": "podcast.com",
                "source_type": "podcast",
                "published": "2024-01-15",
                "score": 8,
                "reason": "Insightful interview",
            }
        ]
        result = generate_digest(entries, total_checked=5)

        assert "## Podcast Episodes" in result
        assert "Great Podcast Episode" in result

    def test_empty_entries_message(self) -> None:
        """Empty entries produces appropriate message."""
        result = generate_digest([], total_checked=50)

        assert "No new high-signal items" in result

    def test_no_high_scores_message(self) -> None:
        """No articles above threshold shows message."""
        entries = [
            {
                "title": "Low Score",
                "link": "https://example.com/low",
                "source": "example.com",
                "source_type": "discovery",
                "published": "2024-01-15",
                "score": 2,
                "reason": "Not relevant",
            }
        ]
        result = generate_digest(entries, total_checked=10)

        assert "No new high-signal items" in result

    def test_includes_stats(self) -> None:
        """Digest includes statistics about items checked."""
        entries = [
            {
                "title": "Article",
                "link": "https://example.com/a",
                "source": "example.com",
                "source_type": "discovery",
                "published": "2024-01-15",
                "score": 8,
                "reason": "Good",
            }
        ]
        result = generate_digest(entries, total_checked=42)

        assert "42 items checked" in result

    def test_archive_picks_included(self) -> None:
        """Archive picks appear in Older Picks section when provided."""
        entries = [
            {
                "title": "Regular Article",
                "link": "https://example.com/reg",
                "source": "example.com",
                "source_type": "discovery",
                "published": "2024-01-15",
                "score": 8,
                "reason": "Good",
            }
        ]
        archive_picks = [
            {
                "title": "Older Good Article",
                "link": "https://example.com/old",
                "source": "example.com",
                "source_type": "podcast",
                "published": "2023-12-01",
                "score": 8,
                "reason": "Still relevant",
            }
        ]
        result = generate_digest(entries, total_checked=5, archive_picks=archive_picks)

        assert "## Older Picks" in result
        assert "Older Good Article" in result

    def test_handles_missing_fields(self) -> None:
        """Entries with missing optional fields don't crash."""
        entries = [
            {
                "title": "Minimal Entry",
                "link": "https://example.com/min",
                "source": "example.com",
                "source_type": "discovery",
                "score": 8,
                # Missing: published, reason
            }
        ]
        result = generate_digest(entries, total_checked=1)

        assert "Minimal Entry" in result
        assert "## Must Read" in result
