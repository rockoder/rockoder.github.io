# Beyond the Code: Automated Content Pipeline

A multi-source content pipeline that scrapes career/workplace topics from HN, Reddit, and newsletters, then uses AI to generate blog post drafts with human review before publishing.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Setup](#setup)
- [Daily Operations](#daily-operations)
- [Manual Usage](#manual-usage)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)

---

## Overview

### What It Does

1. **Daily (automated, GitHub Actions)**: Scrapes HN, Reddit, and newsletters for career/workplace topics
2. **On-demand (local, `codex` CLI)**: Extracts themes and scores topics using AI
3. **On-demand (local, `claude` + `codex` CLIs)**: Generates a blog post draft with critique loop
4. **Human review**: You review the PR, pick a headline, edit, and merge

Topic extraction and content generation run locally through the `claude`
(Claude Code) and `codex` (Codex CLI) tools, which are authenticated to
subscriptions on this machine rather than paid API keys. Neither can run
unattended on a GitHub Actions runner, so only the scrapers (no LLM calls)
stay on a daily schedule — extraction and generation are commands you run
yourself whenever you want a new draft.

### Output

- Draft posts appear as GitHub PRs in `src/content/beyondthecode/`
- PR description includes headline options, quality scores, and pull quotes
- You edit and merge when ready to publish

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                DAILY (00:00 UTC) — GitHub Actions                │
│  btc-scrape.yml workflow                                        │
├─────────────────────────────────────────────────────────────────┤
│  hn_scraper_btc.py → data/hn_nontech_{date}.json               │
│  reddit_scraper.py → data/reddit_{date}.json                   │
│  newsletter_monitor.py → data/newsletters_{date}.json          │
│  (no LLM calls — nothing here needs a subscription/CLI login)  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│              ON-DEMAND (local, run when you want a post)         │
├─────────────────────────────────────────────────────────────────┤
│  topic_extractor.py → data/topic_bank.json          (codex)    │
│                              ↓                                  │
│  content_generator.py:                                          │
│    1. Select best unused topic                                  │
│    2. Generate outline                              (claude)   │
│    3. Critique outline                               (codex)   │
│    4. Generate draft                                (claude)   │
│    5. Critique draft                                  (codex)   │
│    6. Apply revisions                                (claude)   │
│    7. Generate headline options                     (claude)   │
│    8. Create PR as draft                                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      HUMAN REVIEW                               │
├─────────────────────────────────────────────────────────────────┤
│  1. Review PR                                                   │
│  2. Pick headline from options                                  │
│  3. Edit draft as needed                                        │
│  4. Mark ready & merge → Published                              │
└─────────────────────────────────────────────────────────────────┘
```

`claude` and `codex` are both CLI tools authenticated locally (Claude Code
subscription and free ChatGPT/Codex login), so the on-demand box above only
runs on your machine — there's no equivalent GitHub Actions workflow for it
anymore.

---

## Setup

### 1. Add GitHub Secrets

Go to: **Repository → Settings → Secrets and variables → Actions → New repository secret**

Add these secrets (only used by `btc-scrape.yml`, which just scrapes — no LLM calls run in CI):

| Secret Name | Required | Description | How to Get |
|-------------|----------|-------------|------------|
| `REDDIT_CLIENT_ID` | Yes | Reddit OAuth app client ID | [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps) - Create "script" app |
| `REDDIT_CLIENT_SECRET` | Yes | Reddit OAuth app secret | Same as above - shown after creating app |

No LLM API keys are needed in GitHub Secrets. Topic extraction and content
generation run locally via the `claude` and `codex` CLIs, authenticated to
your own subscriptions on this machine — see step 3 below.

**Reddit App Setup**: Go to reddit.com/prefs/apps → "create another app" → Select "script" type → Set redirect URI to `http://localhost:8080` → Note the client ID (under app name) and secret.

### 2. Install Local Dependencies (for manual runs)

```bash
cd /Users/gpagade/personal-code/rockoder.github.io
pip install -r scripts/requirements.txt
```

### 3. Set Local Environment Variables (for manual runs)

Copy the example file and fill in your Reddit credentials:

```bash
cp .env.example .env
# Edit .env with your favorite editor
```

Or export variables directly:

```bash
export REDDIT_CLIENT_ID="..."       # Reddit OAuth
export REDDIT_CLIENT_SECRET="..."   # Reddit OAuth
```

The `.env` file is already gitignored and will be automatically loaded by `run_pipeline.py`.

You also need the `claude` and `codex` CLIs installed and logged in once —
no environment variable is needed for either:

```bash
claude          # log in with your Claude Code subscription, then exit
codex login     # log in with your ChatGPT account
codex login status   # confirms you're logged in
```

### 4. Commit the Pipeline Files

```bash
git add .
git commit -m "Add Beyond the Code content pipeline"
git push
```

---

## Daily Operations

### Automated Flow (No Action Needed)

Once set up, only scraping runs automatically:

| Time | What Happens |
|------|--------------|
| Daily 00:00 UTC | Scrapers run (HN, Reddit, newsletters), scraped data committed |

Topic extraction and draft generation are **not** scheduled — they run
through the local `claude`/`codex` CLIs, so you trigger them yourself
whenever you want a new post.

### Your On-Demand Workflow

1. **Generate a draft when you're ready**
   ```bash
   python scripts/run_pipeline.py --extract --generate
   ```
   This extracts topics from the latest scraped data (via `codex`), then runs
   the outline/critique/draft/critique/revise/headline loop (via `claude` +
   `codex`) and opens a draft PR.

2. **Review the PR**
   - Read the draft in `src/content/beyondthecode/`
   - Check quality scores in PR description
   - Look at pull quote candidates

3. **Pick a headline**
   - PR description has 5 headline options
   - Update the `title:` in the frontmatter

4. **Edit the draft**
   - Fix any issues
   - Add personal touches
   - Verify voice consistency

5. **Merge when ready**
   - Mark PR as ready for review
   - Merge to master
   - Site deploys automatically

---

## Local Development

### Quick Start (Recommended)

The easiest way to run the pipeline locally is using the unified runner script:

```bash
# 1. Install dependencies
pip install -r scripts/requirements.txt

# 2. Set up environment variables
cp .env.example .env
# Edit .env and add your Reddit credentials

# 3. Make sure claude/codex are installed and logged in (see Setup above)

# 4. Run full pipeline in dry-run mode (no PR, no git changes)
python scripts/run_pipeline.py --all --dry-run
```

Dry-run mode saves drafts to `data/drafts/` instead of creating PRs, and doesn't modify the topic bank.

### Using run_pipeline.py

The unified runner script (`scripts/run_pipeline.py`) provides a single interface:

```bash
# Check environment variables
python scripts/run_pipeline.py --check-env

# Run full pipeline (dry-run - safe for testing)
python scripts/run_pipeline.py --all --dry-run

# Run only scrapers
python scripts/run_pipeline.py --scrape

# Run only topic extraction (requires scraped data)
python scripts/run_pipeline.py --extract

# Run only content generation (requires topics in bank)
python scripts/run_pipeline.py --generate --dry-run

# Run full pipeline and create actual PR
python scripts/run_pipeline.py --all
```

Options:
- `--dry-run`: Save draft locally instead of creating PR
- `--skip-topic-update`: Don't mark topic as used (for repeated testing)
- `--check-env`: Only check environment variables, don't run anything
- `--fail-fast`: Stop on first error (default: continue on error)

### Debug Intermediate Output

Every content generation run saves intermediate results for debugging and prompt improvement:

```
data/debug/2026-02-22_143022/
├── 01_topic.json           # Selected topic
├── 02_outline.md           # Generated outline
├── 03_outline_critique.json # Outline critique scores
├── 04_draft.md             # Initial draft
├── 05_draft_critique.json  # Draft critique scores
├── 06_draft_revised.md     # Final draft (after revisions)
├── 07_headlines.json       # Headline options
└── 08_series_info.json     # Series detection result
```

This output is saved regardless of `--dry-run` mode and is gitignored.

### Run Individual Components

```bash
# Just scrape HN
python scripts/hn_scraper_btc.py
# Output: data/hn_nontech_2026-02-19.json

# Just scrape Reddit
python scripts/reddit_scraper.py
# Output: data/reddit_2026-02-19.json

# Just check newsletters
python scripts/newsletter_monitor.py
# Output: data/newsletters_2026-02-19.json

# Just extract topics (needs scraped data first)
python scripts/topic_extractor.py
# Output: Updates data/topic_bank.json

# Just generate content (needs topics in bank)
python scripts/content_generator.py --dry-run
# Output: Saves draft to data/drafts/

# Generate content and create PR
python scripts/content_generator.py
# Output: Creates PR with draft
```

### content_generator.py Options

```bash
python scripts/content_generator.py --help

Options:
  --dry-run           Save draft locally instead of creating PR
  --skip-topic-update Don't mark topic as used (for testing)
```

### Trigger the Scrape Workflow Manually

```bash
# Trigger daily scrape
gh workflow run btc-scrape.yml

# Check workflow status
gh run list --workflow=btc-scrape.yml
```

Content generation has no workflow to trigger — run it locally instead:
`python scripts/run_pipeline.py --extract --generate`.

---

## Customization

### Change LLM Models

Edit `config/models.yaml`. There are only two providers now, both local CLIs:

```yaml
models:
  draft_writing:
    provider: "claude_code"
    model: "sonnet"   # or "opus" / "haiku" — any alias `claude --model` accepts

  draft_critique:
    provider: "codex"
    # model omitted -> uses whatever your `codex` CLI default is
```

Available providers:
- **claude_code**: shells out to `claude -p ...`. `model` accepts any alias the `claude` CLI understands (`sonnet`, `opus`, `haiku`, or a full model id).
- **codex**: shells out to `codex exec ...`. Omit `model` to use the CLI's own default, or set it to any model `codex exec -m <model>` accepts.

There's no `fallback:` support left — a failed CLI call raises instead of
silently trying a paid API. If you want a fallback, the simplest option is
to point the failing task at the other CLI provider and re-run.

### Change Scraping Sources

**Add Reddit subreddits** - Edit `scripts/reddit_scraper.py`:
```python
SUBREDDITS = [
    "experienceddevs",
    "cscareerquestions",
    "managers",
    "yourNewSubreddit",  # Add here
]
```

**Add newsletter feeds** - Edit `scripts/newsletter_monitor.py`:
```python
RSS_FEEDS = {
    "new_feed": {
        "name": "New Newsletter",
        "url": "https://example.com/feed.xml",
        "focus": ["topic1", "topic2"]
    },
    # ... existing feeds
}
```

**Add HN keywords** - Edit `scripts/hn_scraper_btc.py`:
```python
NONTECH_KEYWORDS = [
    "career", "promotion", ...,
    "your_new_keyword",  # Add here
]
```

### Change Voice/Style

Edit the prompt templates in `scripts/prompts/`:

| File | Controls |
|------|----------|
| `outline.txt` | Post structure, section headers, named patterns |
| `draft.txt` | Writing style, formatting, voice requirements |
| `critique.txt` | Quality criteria, scoring rubric |

### Change Schedule

Edit the cron expression in `.github/workflows/btc-scrape.yml` (the only
scheduled workflow left — content generation is local/on-demand, not cron-based):

```yaml
# btc-scrape.yml - Currently daily at midnight UTC
schedule:
  - cron: '0 0 * * *'  # Change as needed
```

Cron format: `minute hour day-of-month month day-of-week`

---

## Troubleshooting

### "No unused topics in bank"

The topic bank is empty or all topics are used.

```bash
# Check topic bank status
python -c "import json; d=json.load(open('data/topic_bank.json')); print(f'Total: {len(d[\"topics\"])}, Unused: {len([t for t in d[\"topics\"] if not t.get(\"used\")])}')"

# Run scrapers to get fresh content
python scripts/hn_scraper_btc.py
python scripts/reddit_scraper.py
python scripts/newsletter_monitor.py

# Extract new topics
python scripts/topic_extractor.py
```

### "LLM call failed"

`claude`/`codex` CLI auth issues, or a bad model name.

```bash
# Test each CLI directly
claude -p "hi" --tools ""
codex exec "hi" --sandbox read-only

# Check codex login status
codex login status

# Test through the pipeline's client
python -c "from scripts.llm_client import LLMClient; c=LLMClient(); print(c.generate('topic_extraction', 'Say hello'))"
```

Check:
- `claude` and `codex` are installed and on your `PATH`
- Both are logged in (`claude` via your subscription, `codex login status` shows ChatGPT login)
- The model name in `config/models.yaml` is one `claude`/`codex` actually accepts

### "Failed to create PR"

Git or gh CLI issues.

```bash
# Check gh authentication
gh auth status

# Re-authenticate if needed
gh auth login --web

# Check you're on master branch
git checkout master
git pull
```

### Workflow Failed

```bash
# Check workflow logs
gh run list --workflow=btc-scrape.yml
gh run view <run-id> --log

# Or check in GitHub UI:
# Repository → Actions → Select workflow → Click failed run
```

### Reset Topic Bank

If you want to start fresh:

```bash
# Backup existing
cp data/topic_bank.json data/topic_bank.backup.json

# Reset
echo '{"topics": [], "last_updated": null}' > data/topic_bank.json

# Re-run extraction
python scripts/topic_extractor.py
```

### Mark Topic as Unused

If you want to regenerate a post for a topic:

```python
import json

with open('data/topic_bank.json', 'r') as f:
    bank = json.load(f)

# Find and reset the topic
for topic in bank['topics']:
    if 'your search term' in topic['theme'].lower():
        topic['used'] = False
        print(f"Reset: {topic['theme']}")

with open('data/topic_bank.json', 'w') as f:
    json.dump(bank, f, indent=2)
```

---

## File Reference

```
rockoder.github.io/
├── .env.example            # Template for local environment variables
├── .github/workflows/
│   └── btc-scrape.yml      # Daily scraping workflow (no LLM calls)
├── config/
│   └── models.yaml         # claude_code/codex CLI routing per task
├── data/
│   ├── topic_bank.json     # Persistent topic storage
│   ├── hn_nontech_*.json   # Daily HN scrape results
│   ├── reddit_*.json       # Daily Reddit scrape results
│   ├── newsletters_*.json  # Daily newsletter results
│   ├── drafts/             # Local drafts from --dry-run mode (gitignored)
│   └── debug/              # Intermediate results for debugging (gitignored)
├── scripts/
│   ├── run_pipeline.py     # Unified local runner (recommended)
│   ├── llm_client.py       # Unified LLM interface
│   ├── hn_scraper_btc.py   # HN non-tech scraper
│   ├── reddit_scraper.py   # Reddit career subreddits
│   ├── newsletter_monitor.py # RSS feed monitor
│   ├── topic_extractor.py  # AI theme extraction
│   ├── content_generator.py # Main orchestrator
│   ├── requirements.txt    # Python dependencies
│   └── prompts/
│       ├── outline.txt     # Outline generation prompt
│       ├── draft.txt       # Draft writing prompt
│       └── critique.txt    # Quality critique prompt
└── src/content/beyondthecode/
    └── *.md                # Generated blog posts
```

---

## Cost Estimates

There's no per-token billing anymore. Outline/draft/revision run through the
`claude` CLI against an existing Claude Code subscription, and both critique
steps plus topic extraction run through the `codex` CLI against a free
ChatGPT plan — so the marginal cost per post is effectively $0 beyond those
subscriptions.

The one thing worth watching: the free ChatGPT plan backing `codex` has its
own usage caps/rate limits. If `codex exec` starts failing with a quota or
rate-limit error, check your ChatGPT plan's usage before assuming something
is broken in the pipeline.
