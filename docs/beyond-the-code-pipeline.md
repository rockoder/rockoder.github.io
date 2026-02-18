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

1. **Daily (automated)**: Scrapes HN, Reddit, and newsletters for career/workplace topics
2. **Daily (automated)**: Extracts themes and scores topics using AI
3. **Twice weekly (automated)**: Generates a blog post draft with critique loop
4. **Human review**: You review the PR, pick a headline, edit, and merge

### Output

- Draft posts appear as GitHub PRs in `src/content/beyondthecode/`
- PR description includes headline options, quality scores, and pull quotes
- You edit and merge when ready to publish

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    DAILY (00:00 UTC)                            │
│  btc-scrape.yml workflow                                        │
├─────────────────────────────────────────────────────────────────┤
│  hn_scraper_btc.py → data/hn_nontech_{date}.json               │
│  reddit_scraper.py → data/reddit_{date}.json                   │
│  newsletter_monitor.py → data/newsletters_{date}.json          │
│  topic_extractor.py → data/topic_bank.json                     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│              TWICE WEEKLY (Mon/Thu 08:00 UTC)                   │
│  btc-generate.yml workflow                                      │
├─────────────────────────────────────────────────────────────────┤
│  content_generator.py:                                          │
│    1. Select best unused topic                                  │
│    2. Generate outline (Claude)                                 │
│    3. Critique outline (Gemini)                                 │
│    4. Generate draft (Claude)                                   │
│    5. Critique draft (Gemini)                                   │
│    6. Apply revisions (Claude)                                  │
│    7. Generate headline options                                 │
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

---

## Setup

### 1. Add GitHub Secrets

Go to: **Repository → Settings → Secrets and variables → Actions → New repository secret**

Add these secrets:

| Secret Name | Required | Description | How to Get |
|-------------|----------|-------------|------------|
| `ANTHROPIC_API_KEY` | Yes* | Claude API key | [console.anthropic.com](https://console.anthropic.com/) |
| `GOOGLE_API_KEY` | Yes | Gemini API key (free tier) | [aistudio.google.com](https://aistudio.google.com/app/apikey) |
| `OPENAI_API_KEY` | Yes* | OpenAI API key (fallback for Anthropic) | [platform.openai.com](https://platform.openai.com/api-keys) |
| `GROQ_API_KEY` | No | Groq API key (free fallback) | [console.groq.com](https://console.groq.com/) |

*Either `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` is required. OpenAI serves as fallback when Anthropic is unavailable.

### 2. Install Local Dependencies (for manual runs)

```bash
cd /Users/gpagade/personal-code/rockoder.github.io
pip install -r scripts/requirements.txt
```

### 3. Set Local Environment Variables (for manual runs)

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export GOOGLE_API_KEY="AIza..."
export OPENAI_API_KEY="sk-..."      # fallback for Anthropic
export GROQ_API_KEY="gsk_..."       # optional
```

Or create a `.env` file (already gitignored):

```bash
# .env
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AIza...
OPENAI_API_KEY=sk-...
GROQ_API_KEY=gsk_...
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

Once set up, the pipeline runs automatically:

| Time | What Happens |
|------|--------------|
| Daily 00:00 UTC | Scrapers run, topics extracted, data committed |
| Mon/Thu 08:00 UTC | Draft generated, PR created |

### Your Weekly Workflow

1. **Check for new PRs** (Mon/Thu afternoons)
   - Look for PRs titled `[Draft] ...`

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

## Manual Usage

### Run Everything Locally

```bash
# Step 1: Scrape all sources
python scripts/hn_scraper_btc.py
python scripts/reddit_scraper.py
python scripts/newsletter_monitor.py

# Step 2: Extract topics
python scripts/topic_extractor.py

# Step 3: Generate a post (creates PR)
python scripts/content_generator.py
```

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
python scripts/content_generator.py
# Output: Creates PR with draft
```

### Trigger Workflows Manually

```bash
# Trigger daily scrape
gh workflow run btc-scrape.yml

# Trigger content generation
gh workflow run btc-generate.yml

# Check workflow status
gh run list --workflow=btc-scrape.yml
gh run list --workflow=btc-generate.yml
```

---

## Customization

### Change LLM Models

Edit `config/models.yaml`:

```yaml
models:
  draft_writing:
    provider: "anthropic"
    model: "claude-sonnet-4-20250514"  # Change to claude-3-haiku for cheaper
    fallback:
      provider: "anthropic"
      model: "claude-3-haiku-20240307"
```

Available providers: `anthropic`, `openai`, `gemini`, `groq`

Available models:
- **anthropic**: `claude-sonnet-4-20250514`, `claude-3-haiku-20240307`
- **openai**: `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo`
- **gemini**: `gemini-2.0-flash`, `gemini-1.5-pro`
- **groq**: `llama-3.1-70b-versatile`

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

Edit the cron expressions in `.github/workflows/`:

```yaml
# btc-scrape.yml - Currently daily at midnight UTC
schedule:
  - cron: '0 0 * * *'  # Change as needed

# btc-generate.yml - Currently Mon/Thu at 8am UTC
schedule:
  - cron: '0 8 * * 1,4'  # Change days/time as needed
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

API key issues or rate limits.

```bash
# Test API keys
python -c "from scripts.llm_client import LLMClient; c=LLMClient(); print(c.generate('topic_extraction', 'Say hello'))"
```

Check:
- API keys are set correctly
- You have credits/quota remaining
- The model name in `config/models.yaml` is valid

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
├── .github/workflows/
│   ├── btc-scrape.yml      # Daily scraping workflow
│   └── btc-generate.yml    # Twice-weekly generation workflow
├── config/
│   └── models.yaml         # LLM provider configuration
├── data/
│   ├── topic_bank.json     # Persistent topic storage
│   ├── hn_nontech_*.json   # Daily HN scrape results
│   ├── reddit_*.json       # Daily Reddit scrape results
│   └── newsletters_*.json  # Daily newsletter results
├── scripts/
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

With the default configuration (Gemini free tier + Claude/OpenAI paid):

| Usage | Anthropic | OpenAI (fallback) |
|-------|-----------|-------------------|
| Topic extraction (daily) | Free (Gemini Flash) | Free (Gemini Flash) |
| Outline generation (2x/week) | ~$0.10/post (Haiku) | ~$0.05/post (GPT-4o-mini) |
| Outline critique (2x/week) | Free (Gemini Flash) | Free (Gemini Flash) |
| Draft writing (2x/week) | ~$0.50/post (Sonnet) | ~$0.40/post (GPT-4o) |
| Draft critique (2x/week) | Free (Gemini Flash) | Free (Gemini Flash) |
| Final revision (2x/week) | ~$0.30/post (Sonnet) | ~$0.25/post (GPT-4o) |
| **Monthly total (8 posts)** | **~$7-10** | **~$5-8** |

To reduce costs:
- Use `claude-3-haiku` or `gpt-4o-mini` for draft writing
- Switch primary provider to OpenAI if you have credits there
