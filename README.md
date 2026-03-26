# Maximilian Discovery Engine

A Python pipeline that ingests ~140 sources daily, scores every article against a relevance profile using an LLM, and surfaces the top results as a ranked digest. Built to solve a personal problem: keeping up with fast-moving research across AI safety, AI governance, youth digital rights, cyberpsychology, and HCI without manually checking dozens of feeds.

Runs autonomously via GitHub Actions. No human in the loop once configured.

## How it works

```
140 RSS feeds → fetch & parse → deduplicate (rolling 10k-item store) → LLM relevance scoring (1-10) → ranked digest.md
```

**Fetch.** Pulls from ~80 discovery feeds (arXiv cs.CY and cs.HC, academic journals, think tanks, researcher blogs, long-tail Substacks) plus per-account RSS for ~60 researchers and writers on X/Twitter via Nitter.

**Deduplicate.** Every processed URL is logged in a rolling `seen_links.json` committed back to the repo, preventing repeat surfacing across runs.

**Score.** Each new item is scored 1–10 by an LLM (Groq-hosted Llama 3.3 70B) against a detailed relevance profile defined in `profile.py`. The profile encodes topical interests, preferred source types, and signal vs. noise heuristics.

**Output.** `digest.md` is generated with Must Read (8–10) and Worth a Look (5–7) tiers. Optional Telegram push notifications deliver results directly.

## Architecture

```
discovery.py    Core pipeline: fetch → dedup → score → write
profile.py      Relevance criteria (edit this to change what surfaces)
feeds.py        Feed list and X/Twitter accounts (edit to add/remove sources)
seen_links.json Rolling dedup store, persisted via git commits
digest.md       Latest output
```

## Source coverage

| Category | Examples | Count |
|----------|----------|-------|
| arXiv | cs.CY (Computers & Society), cs.HC (HCI), keyword searches | 5+ feeds |
| Academic journals | First Monday, Big Data & Society, New Media & Society, Social Media + Society, ACM CHI | 8+ feeds |
| Think tanks & orgs | Oxford Internet Institute, Berkman Klein, AI Now, Ada Lovelace, Alan Turing, Data & Society, CDT, EFF, 5Rights, RAND, 80,000 Hours | 15+ feeds |
| Researcher blogs | Karpathy, Simon Willison, Gary Marcus, Zvi Mowshowitz, Scott Alexander, Chris Olah, Lilian Weng, Paul Christiano, Alignment Forum, LessWrong | 15+ feeds |
| Substacks | AI Snake Oil, Algorithmic Bridge, ChinAI, Reboot, Works in Progress, Asterisk, Real Life, Logic | 15+ feeds |
| X/Twitter (via Nitter) | ~60 accounts including Karpathy, Andrew Ng, Yann LeCun, Timnit Gebru, danah boyd, Kate Crawford, Joy Buolamwini, Amy Orben | 60 accounts |

## Setup

### 1. Add your Groq API key

**GitHub repo → Settings → Secrets and variables → Actions → New repository secret**

- Name: `GROQ_API_KEY`
- Value: your key from [console.groq.com](https://console.groq.com) (free, no credit card required)

> **To use OpenRouter instead:** change the secret name to `OPENROUTER_API_KEY`, set `base_url` to `https://openrouter.ai/api/v1` in `discovery.py`, and set `MODEL` to `meta-llama/llama-3.3-70b-instruct:free`.

### 2. Telegram notifications (optional)

1. Message [@BotFather](https://t.me/BotFather) → `/newbot` → copy the bot token
2. Start a conversation with your bot
3. Visit `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates` → copy the chat ID
4. Add GitHub secrets: `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`

If these secrets are not set, the Telegram step is silently skipped.

### 3. Manual run

**Actions → Discovery Run → Run workflow** to test without waiting for the schedule.

## Scoring Architecture

The pipeline supports two scoring methods that can be used independently or compared:

### LLM-based Scoring (Default)

Uses Groq-hosted Llama 3.3 70B to evaluate articles against a detailed relevance rubric defined in `profile.py`. The LLM receives article title, summary, and source, then returns a 1-10 score with reasoning.

**Strengths:** Nuanced understanding, can apply complex heuristics (e.g., "skip NGO newsletters"), natural language reasoning.

**Limitations:** Requires API key, subject to rate limits, non-deterministic.

### Embedding-based Scoring (Fallback/Comparison)

Uses sentence-transformers (`all-MiniLM-L6-v2`) to compute cosine similarity between article embeddings and pre-defined "anchor texts" representing high-relevance topics.

```bash
# Run with embedding scorer instead of LLM
python discovery.py --use-embeddings

# Or via environment variable
USE_EMBEDDINGS=true python discovery.py
```

**Strengths:** Runs entirely offline, no API key needed, deterministic, fast (~100ms per batch).

**Limitations:** Less nuanced than LLM, requires tuning anchor texts for good performance.

### Comparing Scorers

The `analysis/scoring_evaluation.ipynb` notebook provides:
- Side-by-side score comparison (scatter plot, correlation)
- Score distribution histograms
- Precision/recall metrics by tier
- t-SNE visualization of the embedding space

## Output files

| File | Purpose |
|------|---------|
| `digest.md` | Latest ranked digest, updated each run |
| `seen_links.json` | Rolling dedup store, persists across runs via git commits |
| `feed_errors.log` | Feed fetch and parse errors for pruning dead feeds |

---

<sub>Built with AI-assisted development (Claude Code) for code quality, testing, and the embedding scorer.</sub>