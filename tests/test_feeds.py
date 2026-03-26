"""Tests for feed configuration in feeds.py."""

from urllib.parse import urlparse

from feeds import DISCOVERY_FEEDS, OPML_DOMAINS


class TestFeedUrls:
    """Tests for feed URL validity."""

    def test_all_urls_syntactically_valid(self) -> None:
        """All feed URLs have valid URL syntax."""
        for url, source_type in DISCOVERY_FEEDS:
            parsed = urlparse(url)
            assert parsed.scheme in ("http", "https"), f"Invalid scheme in {url}"
            assert parsed.netloc, f"Missing netloc in {url}"

    def test_no_duplicate_feeds(self) -> None:
        """No duplicate feed URLs exist."""
        urls = [url for url, _ in DISCOVERY_FEEDS]
        assert len(urls) == len(set(urls)), "Duplicate feed URLs found"

    def test_all_urls_are_strings(self) -> None:
        """All URLs are strings, not None or other types."""
        for url, source_type in DISCOVERY_FEEDS:
            assert isinstance(url, str), f"URL is not a string: {url}"
            assert url.strip(), "Empty URL found"


class TestFeedCategories:
    """Tests for feed category configuration."""

    VALID_CATEGORIES = {"technical", "discovery", "podcast", "podcast_selective"}

    def test_all_categories_valid(self) -> None:
        """All feed categories are from the expected set."""
        for url, source_type in DISCOVERY_FEEDS:
            assert source_type in self.VALID_CATEGORIES, (
                f"Unknown category '{source_type}' for {url}"
            )

    def test_technical_feeds_non_empty(self) -> None:
        """Technical category has at least one feed."""
        technical = [f for f in DISCOVERY_FEEDS if f[1] == "technical"]
        assert len(technical) > 0, "No technical feeds configured"

    def test_discovery_feeds_non_empty(self) -> None:
        """Discovery category has at least one feed."""
        discovery = [f for f in DISCOVERY_FEEDS if f[1] == "discovery"]
        assert len(discovery) > 0, "No discovery feeds configured"

    def test_podcast_feeds_non_empty(self) -> None:
        """Podcast categories have at least one feed."""
        podcasts = [f for f in DISCOVERY_FEEDS if "podcast" in f[1]]
        assert len(podcasts) > 0, "No podcast feeds configured"


class TestOpmlDomains:
    """Tests for OPML domain configuration."""

    def test_opml_domains_is_set(self) -> None:
        """OPML_DOMAINS is a set for O(1) lookup."""
        assert isinstance(OPML_DOMAINS, set)

    def test_opml_domains_non_empty(self) -> None:
        """OPML domains list is not empty."""
        assert len(OPML_DOMAINS) > 0

    def test_opml_domains_lowercase(self) -> None:
        """All OPML domains are lowercase for consistent matching."""
        for domain in OPML_DOMAINS:
            assert domain == domain.lower(), f"Domain not lowercase: {domain}"

    def test_opml_domains_no_protocol(self) -> None:
        """OPML domains don't include http/https prefix."""
        for domain in OPML_DOMAINS:
            assert not domain.startswith("http"), f"Domain has protocol: {domain}"
            assert not domain.startswith("www."), f"Domain has www prefix: {domain}"

    def test_no_feed_urls_in_opml_domains(self) -> None:
        """Feed URLs shouldn't match their own OPML exclusion list."""
        # Podcasts are intentionally allowed through, so only check non-podcast
        non_podcast_feeds = [
            (url, stype) for url, stype in DISCOVERY_FEEDS
            if stype not in ("podcast", "podcast_selective")
        ]
        for url, source_type in non_podcast_feeds:
            domain = urlparse(url).netloc.lower().lstrip("www.")
            # Check exact match and subdomain match
            is_blocked = domain in OPML_DOMAINS or any(
                domain.endswith("." + opml) for opml in OPML_DOMAINS
            )
            assert not is_blocked, (
                f"Feed {url} would be blocked by OPML domain {domain}"
            )
