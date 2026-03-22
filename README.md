# Maximilian Discovery Engine

Automated RSS pipeline that surfaces obscure, high-signal articles 3x/day — scored against Maximilian's relevance profile using Claude.

## What it does

1. **Fetches** ~80 discovery feeds (arXiv, academic journals, think tanks, researcher blogs, long-tail Substacks) plus per-account RSS for ~60 X/Twitter accounts via Nitter
2. **Deduplicates** against a rolling 10,000-item seen list committed back to the repo
3. **Scores** every new item 1–10 with Claude using a detailed relevance profile (youth digital rights, AI governance, cyberpsychology, HCI)
4. **Writes** `digest.md` with Must Read (8–10) and Worth a Look (5–7) sections

Runs at 06:00, 12:00, and 18:00 UTC daily via GitHub Actions.

## Setup

### 1. Add your Groq API key

Go to: **GitHub repo → Settings → Secrets and variables → Actions → New repository secret**

- Name: `GROQ_API_KEY`
- Value: your key from [console.groq.com](https://console.groq.com) (free, no credit card required)

> **To use OpenRouter instead:** change the secret name to `OPENROUTER_API_KEY`, set `base_url` to `https://openrouter.ai/api/v1` in `discovery.py`, and set `MODEL` to `meta-llama/llama-3.3-70b-instruct:free`.

### 2. Trigger a manual run (optional)

Go to **Actions → Discovery Run → Run workflow** to test immediately without waiting for the schedule.

## Output files

| File | Description |
|------|-------------|
| `digest.md` | Latest digest — updated each run |
| `seen_links.json` | Rolling dedup store — persists across runs via git commits |
| `feed_errors.log` | Feed fetch and parse errors — useful for pruning dead feeds |

## Customization

- **`profile.py`** — Edit the scoring criteria without touching any logic
- **`feeds.py`** — Add/remove feeds, accounts, and Nitter search queries
- **`discovery.py`** — Core pipeline logic (fetch → dedup → score → write)

## Feeds covered

- **arXiv** — cs.CY (Computers & Society) and cs.HC (HCI) plus keyword searches
- **Academic journals** — First Monday, Big Data & Society, New Media & Society, Social Media + Society, ICS, ACM CHI
- **Think tanks** — OII Oxford, Berkman Klein, AI Now, Ada Lovelace, Alan Turing, Data & Society, CDT, EFF, 5Rights, Pew, Children's Commissioner, RAND, 80,000 Hours
- **Researcher blogs** — Karpathy, Simon Willison, Gary Marcus, Zvi Mowshowitz, Scott Alexander, Eugene Wei, Gwern, Timnit Gebru/DAIR, Abeba Birhane, Chris Olah, Lilian Weng, Paul Christiano, Alignment Forum, LessWrong
- **Long-tail Substacks** — AI Snake Oil, Convivial Society, Reboot, Works in Progress, Asterisk, Real Life, Logic, ChinAI, Algorithmic Bridge, and more
- **X/Twitter via Nitter** — ~60 accounts including Karpathy, Andrew Ng, Yann LeCun, Timnit Gebru, danah boyd, Kate Crawford, Joy Buolamwini, Amy Orben, and others
