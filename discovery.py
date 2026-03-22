"""
Maximilian Discovery Engine
Runs via GitHub Actions 3x/day.
Fetches feeds, deduplicates, scores with an LLM, commits digest.

LLM backend: Groq free tier (llama-3.3-70b-versatile) via OpenAI-compatible API.
To switch to OpenRouter free tier instead, change:
  base_url -> "https://openrouter.ai/api/v1"
  api_key  -> os.environ["OPENROUTER_API_KEY"]
  MODEL    -> "meta-llama/llama-3.3-70b-instruct:free"
"""

import feedparser
import requests
from openai import OpenAI
import json
import random
import time
import os
import hashlib
from datetime import datetime, timedelta, timezone
from urllib.parse import quote, urlparse

from feeds import (
    DISCOVERY_FEEDS, NITTER_ACCOUNTS, NITTER_QUERIES, NITTER_LIST_SOURCES,
    NITTER_HARDCODED_FALLBACKS, OPML_DOMAINS
)
from profile import PROFILE

SEEN_LINKS_FILE = "seen_links.json"
ERRORS_FILE = "feed_errors.log"
DIGEST_FILE = "digest.md"
MAX_SEEN = 10_000
LOOKBACK_DAYS = 7
MAX_PER_FEED = 12
SCORE_THRESHOLD_HIGH = 8
SCORE_THRESHOLD_MEDIUM = 5


# ── NITTER INSTANCE MANAGEMENT ────────────────────────────────────────────────

def fetch_nitter_instances() -> list[str]:
    instances = set()

    # Source 1: zedeus wiki markdown
    try:
        r = requests.get(NITTER_LIST_SOURCES[0], timeout=10)
        for line in r.text.splitlines():
            if "https://" in line:
                for token in line.split():
                    token = token.strip("|()[]*` ")
                    if token.startswith("https://") and "." in token:
                        parsed = urlparse(token)
                        if parsed.netloc:
                            instances.add(f"https://{parsed.netloc}")
    except Exception as e:
        log_error(f"Nitter wiki list fetch failed: {e}")

    # Source 2: xnaas JSON
    try:
        r = requests.get(NITTER_LIST_SOURCES[1], timeout=10)
        data = r.json()
        for item in data:
            if isinstance(item, dict) and item.get("url"):
                instances.add(item["url"].rstrip("/"))
            elif isinstance(item, str) and item.startswith("http"):
                instances.add(item.rstrip("/"))
    except Exception as e:
        log_error(f"Nitter JSON list fetch failed: {e}")

    result = list(instances) + NITTER_HARDCODED_FALLBACKS
    return list(set(result))


def test_instance(url: str) -> bool:
    try:
        r = requests.get(url, timeout=4, allow_redirects=True)
        return r.status_code == 200 and "nitter" in r.text.lower()
    except Exception:
        return False


def get_live_instance(instances: list[str]) -> str | None:
    pool = instances[:]
    random.shuffle(pool)
    for url in pool[:12]:
        if test_instance(url):
            return url.rstrip("/")
        time.sleep(random.uniform(0.3, 0.8))
    return None


# ── LOGGING ───────────────────────────────────────────────────────────────────

def log_error(msg: str):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    with open(ERRORS_FILE, "a") as f:
        f.write(f"[{ts}] {msg}\n")
    print(f"ERROR: {msg}")


# ── DEDUPLICATION ─────────────────────────────────────────────────────────────

def url_hash(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:16]


def load_seen() -> set:
    if os.path.exists(SEEN_LINKS_FILE):
        try:
            with open(SEEN_LINKS_FILE) as f:
                data = json.load(f)
                return set(data.get("hashes", []))
        except Exception:
            return set()
    return set()


def save_seen(seen: set):
    hashes = list(seen)[-MAX_SEEN:]
    with open(SEEN_LINKS_FILE, "w") as f:
        json.dump({"hashes": hashes, "updated": datetime.now(timezone.utc).isoformat()}, f)


def is_from_opml(url: str) -> bool:
    try:
        domain = urlparse(url).netloc.lower().lstrip("www.")
        for known in OPML_DOMAINS:
            if domain == known or domain.endswith("." + known):
                return True
    except Exception:
        pass
    return False


# ── FEED FETCHING ─────────────────────────────────────────────────────────────

def parse_date(entry) -> datetime | None:
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        try:
            return datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        except Exception:
            pass
    if hasattr(entry, "updated_parsed") and entry.updated_parsed:
        try:
            return datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)
        except Exception:
            pass
    return None


def fetch_feed(url: str, source_label: str) -> list[dict]:
    entries = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=LOOKBACK_DAYS)
    try:
        feed = feedparser.parse(
            url,
            request_headers={"User-Agent": "Mozilla/5.0 (compatible; discovery-bot/1.0)"},
            agent="discovery-bot",
        )
        if feed.bozo and not feed.entries:
            log_error(f"Feed parse error ({source_label}): {feed.bozo_exception}")
            return []

        for entry in feed.entries[:MAX_PER_FEED]:
            link = getattr(entry, "link", "").strip()
            if not link:
                continue
            if is_from_opml(link):
                continue

            published = parse_date(entry)
            if published and published < cutoff:
                continue

            title = getattr(entry, "title", "").strip()[:300]
            summary = ""
            if hasattr(entry, "summary"):
                summary = entry.summary[:600]
            elif hasattr(entry, "description"):
                summary = entry.description[:600]

            entries.append({
                "title": title,
                "link": link,
                "summary": summary,
                "source": source_label,
                "published": published.strftime("%Y-%m-%d") if published else "",
            })
    except Exception as e:
        log_error(f"Feed fetch error ({source_label}): {e}")

    return entries


def fetch_all(nitter_instance: str | None) -> list[dict]:
    all_entries = []

    # Static discovery feeds
    for url in DISCOVERY_FEEDS:
        label = urlparse(url).netloc or url[:50]
        entries = fetch_feed(url, label)
        all_entries.extend(entries)
        time.sleep(random.uniform(0.2, 0.6))

    # Nitter per-account RSS
    if nitter_instance:
        # Deduplicate handles (list may have repeats)
        seen_handles = set()
        for handle in NITTER_ACCOUNTS:
            h = handle.lower()
            if h in seen_handles:
                continue
            seen_handles.add(h)
            rss_url = f"{nitter_instance}/{handle}/rss"
            entries = fetch_feed(rss_url, f"@{handle}")
            all_entries.extend(entries)
            time.sleep(random.uniform(0.4, 0.9))

        # Nitter dynamic searches
        for query in NITTER_QUERIES:
            rss_url = f"{nitter_instance}/search?q={quote(query)}&f=rss"
            entries = fetch_feed(rss_url, f"nitter:{query[:40]}")
            all_entries.extend(entries)
            time.sleep(random.uniform(0.5, 1.0))
    else:
        print("No live Nitter instance — skipping Twitter layer")

    print(f"Total entries fetched: {len(all_entries)}")
    return all_entries


def deduplicate(entries: list[dict], seen: set) -> tuple[list[dict], set]:
    fresh = []
    new_hashes = set()
    for e in entries:
        h = url_hash(e["link"])
        if h not in seen and h not in new_hashes:
            fresh.append(e)
            new_hashes.add(h)
    return fresh, new_hashes


# ── LLM SCORING ───────────────────────────────────────────────────────────────

MODEL = "llama-3.3-70b-versatile"  # Groq free tier


def score_batch(entries: list[dict], client: OpenAI) -> list[dict]:
    if not entries:
        return entries

    batch_text = "\n\n".join([
        f"[{i}] SOURCE: {e['source']}\nTITLE: {e['title']}\nSUMMARY: {e['summary'][:400]}"
        for i, e in enumerate(entries)
    ])

    for attempt in range(2):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                max_tokens=2000,
                messages=[
                    {"role": "system", "content": PROFILE},
                    {"role": "user", "content": f"Score each item 1-10. Return a JSON array with objects: {{index, score, reason}}.\n\n{batch_text}"}
                ]
            )
            raw = response.choices[0].message.content.strip()
            # Strip markdown fences if present
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            scores = json.loads(raw.strip())
            for s in scores:
                idx = s.get("index")
                if isinstance(idx, int) and 0 <= idx < len(entries):
                    entries[idx]["score"] = s.get("score", 0)
                    entries[idx]["reason"] = s.get("reason", "")
            return entries
        except Exception as e:
            if attempt == 0:
                log_error(f"Score batch error (attempt 1): {e} — retrying")
                time.sleep(5)
            else:
                log_error(f"Score batch failed both attempts: {e}")
                for e_item in entries:
                    e_item.setdefault("score", 0)
                    e_item.setdefault("reason", "scoring failed")

    return entries


def score_all(entries: list[dict]) -> list[dict]:
    client = OpenAI(
        api_key=os.environ["GROQ_API_KEY"],
        base_url="https://api.groq.com/openai/v1",
    )
    scored = []
    for i in range(0, len(entries), 25):
        batch = entries[i:i + 25]
        scored.extend(score_batch(batch, client))
        time.sleep(1.5)
    return scored


# ── DIGEST GENERATION ─────────────────────────────────────────────────────────

def generate_digest(entries: list[dict], nitter_status: str, total_checked: int) -> str:
    high = sorted(
        [e for e in entries if e.get("score", 0) >= SCORE_THRESHOLD_HIGH],
        key=lambda x: x.get("score", 0), reverse=True
    )
    medium = sorted(
        [e for e in entries if SCORE_THRESHOLD_MEDIUM <= e.get("score", 0) < SCORE_THRESHOLD_HIGH],
        key=lambda x: x.get("score", 0), reverse=True
    )

    ts = datetime.now(timezone.utc).strftime("%B %d, %Y · %H:%M UTC")
    lines = [
        f"# Discovery Digest — {ts}",
        f"\n**{len(high)} must-read** · **{len(medium)} worth a look** · {total_checked} items checked · Nitter: {nitter_status}\n",
        "---\n",
    ]

    if not high and not medium:
        lines.append("*No new high-signal items this cycle.*")
        return "\n".join(lines)

    if high:
        lines.append("## Must Read\n")
        for e in high[:20]:
            lines.append(f"**[{e['title']}]({e['link']})** &nbsp;`{e.get('score')}/10`")
            if e.get("reason"):
                lines.append(f"*{e['reason']}*")
            lines.append(f"<sub>{e.get('source', '')} &nbsp;·&nbsp; {e.get('published', '')}</sub>\n")

    if medium:
        lines.append("## Worth a Look\n")
        for e in medium[:15]:
            lines.append(f"**[{e['title']}]({e['link']})** &nbsp;`{e.get('score')}/10`")
            if e.get("reason"):
                lines.append(f"*{e['reason']}*")
            lines.append(f"<sub>{e.get('source', '')} &nbsp;·&nbsp; {e.get('published', '')}</sub>\n")

    return "\n".join(lines)


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    print("=== Maximilian Discovery Engine ===")
    print(f"Run time: {datetime.now(timezone.utc).isoformat()}")

    # Nitter setup
    print("Fetching Nitter instances...")
    instances = fetch_nitter_instances()
    live = get_live_instance(instances)
    nitter_status = live if live else "unavailable"
    print(f"Nitter: {nitter_status}")

    # Fetch
    print("Fetching feeds...")
    all_entries = fetch_all(live)

    # Dedup
    seen = load_seen()
    fresh, new_hashes = deduplicate(all_entries, seen)
    print(f"New after dedup: {len(fresh)} (seen pool: {len(seen)})")

    if not fresh:
        digest = f"# Discovery Digest — {datetime.now(timezone.utc).strftime('%B %d, %Y · %H:%M UTC')}\n\n*No new items this cycle.*"
        with open(DIGEST_FILE, "w") as f:
            f.write(digest)
        print("Nothing new. Digest written.")
        return

    # Score
    print(f"Scoring {len(fresh)} items with Claude...")
    scored = score_all(fresh)

    # Update seen
    save_seen(seen | new_hashes)

    # Generate digest
    digest = generate_digest(scored, nitter_status, len(fresh))
    with open(DIGEST_FILE, "w") as f:
        f.write(digest)

    high_count = len([e for e in scored if e.get("score", 0) >= SCORE_THRESHOLD_HIGH])
    print(f"Done. High-signal: {high_count}. Digest written to {DIGEST_FILE}.")


if __name__ == "__main__":
    main()
