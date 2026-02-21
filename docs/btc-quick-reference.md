# Beyond the Code - Quick Reference

## First-Time Setup Checklist

### For GitHub Actions (automated pipeline)
- [ ] Add `ANTHROPIC_API_KEY` to GitHub Secrets (or use OpenAI as primary)
- [ ] Add `OPENAI_API_KEY` to GitHub Secrets (fallback for Anthropic)
- [ ] Add `GOOGLE_API_KEY` to GitHub Secrets
- [ ] (Optional) Add `GROQ_API_KEY` to GitHub Secrets
- [ ] Add `REDDIT_CLIENT_ID` to GitHub Secrets (create app at reddit.com/prefs/apps)
- [ ] Add `REDDIT_CLIENT_SECRET` to GitHub Secrets
- [ ] Commit and push pipeline files
- [ ] Run first scrape manually: `gh workflow run btc-scrape.yml`

### For Local Development
- [ ] `pip install -r scripts/requirements.txt`
- [ ] `cp .env.example .env`
- [ ] Fill in API keys in `.env`
- [ ] Test: `python scripts/run_pipeline.py --check-env`
- [ ] Run: `python scripts/run_pipeline.py --all --dry-run`

## Weekly Workflow

```
Mon/Thu → Check email/GitHub for new draft PRs
        → Review draft in PR
        → Pick headline (update title: in frontmatter)
        → Edit as needed
        → Merge to publish
```

## Common Commands

```bash
# Check topic bank status
python -c "import json; d=json.load(open('data/topic_bank.json')); print(f'Unused topics: {len([t for t in d[\"topics\"] if not t.get(\"used\")])}')"

# Trigger scraping manually
gh workflow run btc-scrape.yml

# Trigger content generation manually
gh workflow run btc-generate.yml

# Check workflow status
gh run list

# View workflow logs
gh run view <run-id> --log
```

## Local Testing

```bash
# Install deps
pip install -r scripts/requirements.txt

# Set up environment (copy template and fill in your keys)
cp .env.example .env
# Edit .env with your API keys

# Run full pipeline in dry-run mode (safe - no PR, no git changes)
python scripts/run_pipeline.py --all --dry-run

# Or run stages individually:
python scripts/run_pipeline.py --scrape           # Just scrape sources
python scripts/run_pipeline.py --extract          # Just extract topics
python scripts/run_pipeline.py --generate --dry-run  # Just generate draft
```

### Advanced Local Testing

```bash
# Check your environment variables
python scripts/run_pipeline.py --check-env

# Run content generator directly with options
python scripts/content_generator.py --dry-run --skip-topic-update

# Create actual PR (when ready)
python scripts/run_pipeline.py --all
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
| Daily 00:00 UTC | Scrape sources, extract topics |
| Mon/Thu 08:00 UTC | Generate draft, create PR |

## Troubleshooting

**No topics?** → Run scrapers + extractor
**LLM failed?** → Check API keys, quota
**PR failed?** → Run `gh auth status`, re-login if needed
**Reddit 403?** → Missing `REDDIT_CLIENT_ID`/`REDDIT_CLIENT_SECRET` secrets (Reddit blocks datacenter IPs without OAuth)
