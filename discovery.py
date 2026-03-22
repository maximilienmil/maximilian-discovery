"""
Maximilian Discovery Engine
Runs via GitHub Actions 3x/day.
Fetches feeds, deduplicates, scores with an LLM, commits digest, pushes to Telegram.

LLM backend: Groq free tier (llama-3.3-70b-versatile) via OpenAI-compatible API.
To switch to OpenRouter free tier instead, change:
  base_url -> "https://openrouter.ai/api/v1"
  api_key  -> os.environ["OPENROUTER_API_KEY"]
  MODEL    -> "meta-llama/llama-3.3-70b-instruct:free"

Telegram: set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in GitHub secrets.
If not set, Telegram is silently skipped.
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
from urllib.parse import urlparse

from feeds import DISCOVERY_FEEDS, OPML_DOMAINS
from profile import PROFILE

SEEN_LINKS_FILE = "seen_links.json"
ERRORS_FILE = "feed_errors.log"
DIGEST_FILE = "digest.md"
MAX_SEEN = 10_000
LOOKBACK_DAYS = 7
MAX_PER_FEED = 12
SCORE_THRESHOLD_HIGH = 8
SCORE_THRESHOLD_MEDIUM = 5
SCORE_THRESHOLD_TECH = 6        # minimum score for the Technical section
SCORE_THRESHOLD_PODCAST = 7     # minimum score for standard podcast episodes
SCORE_THRESHOLD_PODCAST_SEL = 8 # minimum score for selective podcast shows


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


PODCAST_TYPES = ("podcast", "podcast_selective")
LOOKBACK_DAYS_PODCAST = 30  # podcasts release infrequently; look back further


def fetch_feed(url: str, source_label: str, source_type: str) -> list[dict]:
    entries = []
    days = LOOKBACK_DAYS_PODCAST if source_type in PODCAST_TYPES else LOOKBACK_DAYS
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    try:
        # Try requests first (handles encoding better, avoids lxml strictness)
        feed = None
        try:
            r = requests.get(
                url,
                headers={"User-Agent": "Mozilla/5.0 (compatible; Feedfetcher-Google/1.0)"},
                timeout=15,
                allow_redirects=True,
            )
            if r.status_code == 200:
                feed = feedparser.parse(
                    r.content,
                    response_headers={"content-type": r.headers.get("content-type", "application/rss+xml")},
                )
        except Exception:
            pass

        # Fall back to feedparser direct fetch if requests failed or returned no entries
        if feed is None or (feed.bozo and not feed.entries):
            feed = feedparser.parse(
                url,
                request_headers={"User-Agent": "Mozilla/5.0 (compatible; Feedfetcher-Google/1.0)"},
            )

        if not feed.entries:
            if feed.bozo:
                log_error(f"Feed parse error ({source_label}): {feed.bozo_exception}")
            return []

        for entry in feed.entries[:MAX_PER_FEED]:
            link = getattr(entry, "link", "").strip()
            if not link:
                continue
            # Podcast episodes are intentionally from publishers already in the OPML
            # (e.g. HBR, McKinsey) — skip the domain filter for podcast source types
            if source_type not in PODCAST_TYPES and is_from_opml(link):
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
                "source_type": source_type,
                "published": published.strftime("%Y-%m-%d") if published else "",
            })
    except Exception as e:
        log_error(f"Feed fetch error ({source_label}): {e}")

    return entries


def fetch_all() -> list[dict]:
    all_entries = []
    for url, source_type in DISCOVERY_FEEDS:
        label = urlparse(url).netloc or url[:50]
        entries = fetch_feed(url, label, source_type)
        all_entries.extend(entries)
        time.sleep(random.uniform(0.2, 0.6))
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

def generate_digest(entries: list[dict], total_checked: int) -> str:
    podcasts = [e for e in entries if e.get("source_type") in ("podcast", "podcast_selective")]
    rest = [e for e in entries if e.get("source_type") not in ("podcast", "podcast_selective")]
    discovery = [e for e in rest if e.get("source_type") != "technical"]
    technical = [e for e in rest if e.get("source_type") == "technical"]

    must_read = sorted(
        [e for e in discovery if e.get("score", 0) >= SCORE_THRESHOLD_HIGH],
        key=lambda x: x.get("score", 0), reverse=True
    )
    worth_look = sorted(
        [e for e in discovery if SCORE_THRESHOLD_MEDIUM <= e.get("score", 0) < SCORE_THRESHOLD_HIGH],
        key=lambda x: x.get("score", 0), reverse=True
    )
    tech_picks = sorted(
        [e for e in technical if e.get("score", 0) >= SCORE_THRESHOLD_TECH],
        key=lambda x: x.get("score", 0), reverse=True
    )
    podcast_picks = sorted(
        [e for e in podcasts if (
            e.get("score", 0) >= SCORE_THRESHOLD_PODCAST_SEL if e.get("source_type") == "podcast_selective"
            else e.get("score", 0) >= SCORE_THRESHOLD_PODCAST
        )],
        key=lambda x: x.get("score", 0), reverse=True
    )

    ts = datetime.now(timezone.utc).strftime("%B %d, %Y · %H:%M UTC")
    lines = [
        f"# Discovery Digest — {ts}",
        f"\n**{len(must_read)} must-read** · **{len(worth_look)} worth a look** · **{len(tech_picks)} technical** · **{len(podcast_picks)} podcast** · {total_checked} items checked\n",
        "---\n",
    ]

    if not must_read and not worth_look and not tech_picks and not podcast_picks:
        lines.append("*No new high-signal items this cycle.*")
        return "\n".join(lines)

    if must_read:
        lines.append("## Must Read\n")
        for e in must_read[:20]:
            lines.append(f"**[{e['title']}]({e['link']})** &nbsp;`{e.get('score')}/10`")
            if e.get("reason"):
                lines.append(f"*{e['reason']}*")
            lines.append(f"<sub>{e.get('source', '')} &nbsp;·&nbsp; {e.get('published', '')}</sub>\n")

    if worth_look:
        lines.append("## Worth a Look\n")
        for e in worth_look[:15]:
            lines.append(f"**[{e['title']}]({e['link']})** &nbsp;`{e.get('score')}/10`")
            if e.get("reason"):
                lines.append(f"*{e['reason']}*")
            lines.append(f"<sub>{e.get('source', '')} &nbsp;·&nbsp; {e.get('published', '')}</sub>\n")

    if tech_picks:
        lines.append("## Research & Technical\n")
        for e in tech_picks[:15]:
            lines.append(f"**[{e['title']}]({e['link']})** &nbsp;`{e.get('score')}/10`")
            if e.get("reason"):
                lines.append(f"*{e['reason']}*")
            lines.append(f"<sub>{e.get('source', '')} &nbsp;·&nbsp; {e.get('published', '')}</sub>\n")

    if podcast_picks:
        lines.append("## Podcast Episodes\n")
        for e in podcast_picks[:10]:
            lines.append(f"**[{e['title']}]({e['link']})** &nbsp;`{e.get('score')}/10`")
            if e.get("reason"):
                lines.append(f"*{e['reason']}*")
            lines.append(f"<sub>{e.get('source', '')} &nbsp;·&nbsp; {e.get('published', '')}</sub>\n")

    return "\n".join(lines)


# ── TELEGRAM ──────────────────────────────────────────────────────────────────

def send_telegram(entries: list[dict], total_checked: int):
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
    if not bot_token or not chat_id:
        print("Telegram not configured — skipping.")
        return

    podcasts = [e for e in entries if e.get("source_type") in ("podcast", "podcast_selective")]
    rest = [e for e in entries if e.get("source_type") not in ("podcast", "podcast_selective")]
    discovery = [e for e in rest if e.get("source_type") != "technical"]
    technical = [e for e in rest if e.get("source_type") == "technical"]

    must_read = sorted(
        [e for e in discovery if e.get("score", 0) >= SCORE_THRESHOLD_HIGH],
        key=lambda x: x.get("score", 0), reverse=True
    )
    worth_look = sorted(
        [e for e in discovery if SCORE_THRESHOLD_MEDIUM <= e.get("score", 0) < SCORE_THRESHOLD_HIGH],
        key=lambda x: x.get("score", 0), reverse=True
    )
    tech_picks = sorted(
        [e for e in technical if e.get("score", 0) >= SCORE_THRESHOLD_TECH],
        key=lambda x: x.get("score", 0), reverse=True
    )
    podcast_picks = sorted(
        [e for e in podcasts if (
            e.get("score", 0) >= SCORE_THRESHOLD_PODCAST_SEL if e.get("source_type") == "podcast_selective"
            else e.get("score", 0) >= SCORE_THRESHOLD_PODCAST
        )],
        key=lambda x: x.get("score", 0), reverse=True
    )

    ts = datetime.now(timezone.utc).strftime("%b %d · %H:%M UTC")
    parts = [f"<b>Discovery Digest — {ts}</b>"]
    parts.append(f"<i>{len(must_read)} must-read · {len(worth_look)} worth a look · {len(tech_picks)} technical · {len(podcast_picks)} podcast · {total_checked} checked</i>")

    if must_read:
        parts.append("\n<b>Must Read</b>")
        for e in must_read[:10]:
            title = e["title"][:90].replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")
            reason = e.get("reason", "")[:120].replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")
            parts.append(f'• <a href="{e["link"]}">{title}</a> <code>{e.get("score")}/10</code>')
            if reason:
                parts.append(f'  <i>{reason}</i>')

    if worth_look:
        parts.append("\n<b>Worth a Look</b>")
        for e in worth_look[:8]:
            title = e["title"][:90].replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")
            parts.append(f'• <a href="{e["link"]}">{title}</a> <code>{e.get("score")}/10</code>')

    if tech_picks:
        parts.append("\n<b>Research &amp; Technical</b>")
        for e in tech_picks[:6]:
            title = e["title"][:90].replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")
            parts.append(f'• <a href="{e["link"]}">{title}</a> <code>{e.get("score")}/10</code>')

    if podcast_picks:
        parts.append("\n<b>Podcast Episodes</b>")
        for e in podcast_picks[:5]:
            title = e["title"][:90].replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")
            reason = e.get("reason", "")[:120].replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")
            parts.append(f'• <a href="{e["link"]}">{title}</a> <code>{e.get("score")}/10</code>')
            if reason:
                parts.append(f'  <i>{reason}</i>')

    msg = "\n".join(parts)
    if len(msg) > 4000:
        msg = msg[:3950] + "\n\n<i>[truncated]</i>"

    try:
        r = requests.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": msg,
                "parse_mode": "HTML",
                "disable_web_page_preview": True,
            },
            timeout=15,
        )
        if r.status_code == 200:
            print("Telegram: sent.")
        else:
            log_error(f"Telegram send failed: {r.status_code} {r.text[:200]}")
    except Exception as e:
        log_error(f"Telegram exception: {e}")


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    print("=== Maximilian Discovery Engine ===")
    print(f"Run time: {datetime.now(timezone.utc).isoformat()}")

    print("Fetching feeds...")
    all_entries = fetch_all()

    seen = load_seen()
    fresh, new_hashes = deduplicate(all_entries, seen)
    print(f"New after dedup: {len(fresh)} (seen pool: {len(seen)})")

    if not fresh:
        digest = f"# Discovery Digest — {datetime.now(timezone.utc).strftime('%B %d, %Y · %H:%M UTC')}\n\n*No new items this cycle.*"
        with open(DIGEST_FILE, "w") as f:
            f.write(digest)
        print("Nothing new. Digest written.")
        return

    print(f"Scoring {len(fresh)} items...")
    scored = score_all(fresh)

    save_seen(seen | new_hashes)

    digest = generate_digest(scored, len(fresh))
    with open(DIGEST_FILE, "w") as f:
        f.write(digest)

    high_count = len([e for e in scored if e.get("score", 0) >= SCORE_THRESHOLD_HIGH])
    print(f"Done. High-signal: {high_count}. Digest written to {DIGEST_FILE}.")

    send_telegram(scored, len(fresh))


if __name__ == "__main__":
    main()
