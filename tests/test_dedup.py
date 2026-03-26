"""Tests for deduplication logic in discovery.py."""

from discovery import url_hash, deduplicate, load_seen, is_from_opml


class TestUrlHash:
    """Tests for URL hashing function."""

    def test_url_hash_returns_string(self) -> None:
        """Hash function returns a string."""
        result = url_hash("https://example.com/article")
        assert isinstance(result, str)

    def test_url_hash_consistent(self) -> None:
        """Same URL produces same hash."""
        url = "https://example.com/article"
        assert url_hash(url) == url_hash(url)

    def test_url_hash_different_urls(self) -> None:
        """Different URLs produce different hashes."""
        hash1 = url_hash("https://example.com/article1")
        hash2 = url_hash("https://example.com/article2")
        assert hash1 != hash2

    def test_url_hash_length(self) -> None:
        """Hash is truncated to 16 characters."""
        result = url_hash("https://example.com/article")
        assert len(result) == 16


class TestDeduplicate:
    """Tests for deduplicate function."""

    def test_rejects_seen_url(self) -> None:
        """URLs already in seen set are rejected."""
        entries = [{"link": "https://example.com/seen"}]
        seen = {url_hash("https://example.com/seen")}
        fresh, new_hashes = deduplicate(entries, seen)
        assert len(fresh) == 0
        assert len(new_hashes) == 0

    def test_accepts_new_url(self) -> None:
        """New URLs not in seen set are accepted."""
        entries = [{"link": "https://example.com/new"}]
        seen = {url_hash("https://example.com/old")}
        fresh, new_hashes = deduplicate(entries, seen)
        assert len(fresh) == 1
        assert fresh[0]["link"] == "https://example.com/new"
        assert len(new_hashes) == 1

    def test_empty_seen_list(self) -> None:
        """All entries accepted when seen list is empty."""
        entries = [
            {"link": "https://example.com/a"},
            {"link": "https://example.com/b"},
        ]
        fresh, new_hashes = deduplicate(entries, set())
        assert len(fresh) == 2
        assert len(new_hashes) == 2

    def test_empty_entries(self) -> None:
        """Empty entries list returns empty results."""
        seen = {url_hash("https://example.com/seen")}
        fresh, new_hashes = deduplicate([], seen)
        assert fresh == []
        assert new_hashes == set()

    def test_dedup_within_batch(self) -> None:
        """Duplicate URLs within the same batch are deduplicated."""
        entries = [
            {"link": "https://example.com/same"},
            {"link": "https://example.com/same"},
        ]
        fresh, new_hashes = deduplicate(entries, set())
        assert len(fresh) == 1
        assert len(new_hashes) == 1


class TestIsFromOpml:
    """Tests for OPML domain filtering."""

    def test_matches_opml_domain(self) -> None:
        """URLs from OPML domains are detected."""
        assert is_from_opml("https://www.nytimes.com/article") is True
        assert is_from_opml("https://techcrunch.com/news") is True

    def test_rejects_non_opml_domain(self) -> None:
        """URLs not in OPML are allowed through."""
        assert is_from_opml("https://arxiv.org/paper") is False
        assert is_from_opml("https://random-blog.com/post") is False

    def test_handles_www_prefix(self) -> None:
        """www prefix is stripped before matching."""
        assert is_from_opml("https://www.wired.com/article") is True
        assert is_from_opml("https://wired.com/article") is True

    def test_handles_malformed_url(self) -> None:
        """Malformed URLs don't crash, return False."""
        assert is_from_opml("not-a-url") is False
        assert is_from_opml("") is False

    def test_handles_none_gracefully(self) -> None:
        """None input doesn't crash."""
        # The function expects a string, but should handle edge cases
        try:
            result = is_from_opml(None)  # type: ignore
            assert result is False
        except (TypeError, AttributeError):
            # Also acceptable to raise an error for None
            pass


class TestLoadSeen:
    """Tests for loading seen links from file."""

    def test_returns_set(self, tmp_path, monkeypatch) -> None:
        """load_seen returns a set."""
        monkeypatch.chdir(tmp_path)
        result = load_seen()
        assert isinstance(result, set)

    def test_empty_when_file_missing(self, tmp_path, monkeypatch) -> None:
        """Returns empty set when file doesn't exist."""
        monkeypatch.chdir(tmp_path)
        result = load_seen()
        assert result == set()
