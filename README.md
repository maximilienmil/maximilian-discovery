# Maximilian Discovery Engine

A Python pipeline that ingests 140 RSS feeds daily, scores every article against a relevance profile using an LLM, and surfaces the top results as a ranked digest. Built to solve a personal problem: keeping up with fast-moving research across AI safety, AI governance, youth digital rights, cyberpsychology, and HCI without manually checking dozens of feeds.

Runs autonomously via GitHub Actions. No human in the loop once configured.

## How it works

```
140 RSS feeds → fetch & parse → deduplicate (rolling 10k-item store) → LLM relevance scoring (1-10) → ranked digest.md
```

**Fetch.** Pulls from 140 discovery feeds including arXiv cs.CY and cs.HC, academic journals, think tanks, researcher blogs, and long-tail Substacks.

**Deduplicate.** Every processed URL is logged in a rolling `seen_links.json` committed back to the repo, preventing repeat surfacing across runs.

**Score.** Each new item is scored 1–10 by an LLM (Groq-hosted Llama 3.3 70B) against a detailed relevance profile defined in `profile.py`. The profile encodes topical interests, preferred source types, and signal vs. noise heuristics.

**Output.** `digest.md` is generated with Must Read (8–10) and Worth a Look (5–7) tiers. Optional Telegram push notifications deliver results directly.

## Architecture

```
discovery.py    Core pipeline: fetch → dedup → score → write
profile.py      Relevance criteria (edit this to change what surfaces)
feeds.py        Feed list (edit to add/remove sources)
seen_links.json Rolling dedup store, persisted via git commits
digest.md       Latest output
```

## Source coverage

| Category | Examples | Count |
|----------|----------|-------|
| arXiv | cs.CY, cs.HC, cs.AI, cs.LG + 8 keyword searches (interpretability, RLHF, alignment, etc.) | 12 feeds |
| Academic journals | First Monday, New Media & Society, Social Media + Society, Big Data & Society, ACM CHI/CSCW | 9 feeds |
| ML research blogs & labs | Neel Nanda, Chris Olah, Lilian Weng, Distill, Stanford HAI, EleutherAI, CHAI Berkeley | 43 feeds |
| Discovery | Substacks (AI Snake Oil, ChinAI, Zvi), think tanks (Berkman Klein, OII, Alan Turing), LessWrong, Alignment Forum | 49 feeds |
| Podcasts | Lex Fridman, Future of Life, TWIML, 80,000 Hours, Gradient Dissent, Machine Learning Street Talk | 27 feeds |

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