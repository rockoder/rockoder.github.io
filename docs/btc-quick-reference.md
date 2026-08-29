# Beyond the Code - Quick Reference

## First-Time Setup Checklist

### For GitHub Actions (automated scraping only)
- [ ] Add `REDDIT_CLIENT_ID` to GitHub Secrets (create app at reddit.com/prefs/apps)
- [ ] Add `REDDIT_CLIENT_SECRET` to GitHub Secrets
- [ ] Commit and push pipeline files
- [ ] Run first scrape manually: `gh workflow run btc-scrape.yml`

### For Local Development (topic extraction + content generation)
- [ ] `pip install -r scripts/requirements.txt`
- [ ] `cp .env.example .env`
- [ ] Fill in Reddit credentials in `.env`
- [ ] Install `claude` and `codex` CLIs; log in to each once (`claude`, `codex login`)
- [ ] Test: `python scripts/run_pipeline.py --check-env`
- [ ] Run: `python scripts/run_pipeline.py --extract --generate --dry-run`

## Weekly Workflow

```
Whenever you want a new post →
    python scripts/run_pipeline.py --extract --generate
        → Review draft in PR
        → Pick headline (update title: in frontmatter)
        → Edit as needed
        → Merge to publish
```

There's no more automatic Mon/Thu draft — scraping stays automated daily, but
extraction and generation are on-demand local commands (they run through the
`claude`/`codex` CLIs, which are authenticated on this machine, not in CI).

## Common Commands

```bash
# Check topic bank status
python -c "import json; d=json.load(open('data/topic_bank.json')); print(f'Unused topics: {len([t for t in d[\"topics\"] if not t.get(\"used\")])}')"

# Trigger scraping manually
gh workflow run btc-scrape.yml

# Check workflow status
gh run list

# View workflow logs
gh run view <run-id> --log
```

## Local Testing

```bash
# Install deps
pip install -r scripts/requirements.txt

# Set up environment (copy template and fill in Reddit credentials)
cp .env.example .env
# Edit .env with your Reddit OAuth credentials

# Extract topics and generate a draft locally (safe - no PR, no git changes)
python scripts/run_pipeline.py --extract --generate --dry-run

# Or run stages individually:
python scripts/run_pipeline.py --scrape           # Just scrape sources
python scripts/run_pipeline.py --extract          # Just extract topics (codex)
python scripts/run_pipeline.py --generate --dry-run  # Just generate draft (claude + codex)
```

### Advanced Local Testing

```bash
# Check your environment variables and local CLI tools
python scripts/run_pipeline.py --check-env

# Run content generator directly with options
python scripts/content_generator.py --dry-run --skip-topic-update

# Create actual PR (when ready)
python scripts/run_pipeline.py --extract --generate
```

## Key Files

| What | Where |
|------|-------|
| Local runner | `scripts/run_pipeline.py` |
| Env template | `.env.example` |
| LLM config | `config/models.yaml` |
| Topic bank | `data/topic_bank.json` |
| Local drafts | `data/drafts/` (from --dry-run) |
| Prompts | `scripts/prompts/*.txt` |
| Full docs | `docs/beyond-the-code-pipeline.md` |

## Automated Schedule

| When | What |
|------|------|
| Daily 00:00 UTC | Scrape sources only (HN, Reddit, newsletters) |

Topic extraction and content generation are no longer scheduled — run them
locally whenever you want a new draft (see Weekly Workflow above).

## Troubleshooting

**No topics?** → Run scrapers, then `python scripts/topic_extractor.py` locally
**LLM failed?** → Check `claude`/`codex` CLI auth: `claude -p "hi" --tools ""`, `codex login status`
**PR failed?** → Run `gh auth status`, re-login if needed
**Reddit 403?** → Missing `REDDIT_CLIENT_ID`/`REDDIT_CLIENT_SECRET` secrets (Reddit blocks datacenter IPs without OAuth)
