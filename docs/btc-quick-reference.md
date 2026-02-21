# Beyond the Code - Quick Reference

## First-Time Setup Checklist

- [ ] Add `ANTHROPIC_API_KEY` to GitHub Secrets (or use OpenAI as primary)
- [ ] Add `OPENAI_API_KEY` to GitHub Secrets (fallback for Anthropic)
- [ ] Add `GOOGLE_API_KEY` to GitHub Secrets
- [ ] (Optional) Add `GROQ_API_KEY` to GitHub Secrets
- [ ] Add `REDDIT_CLIENT_ID` to GitHub Secrets (create app at reddit.com/prefs/apps)
- [ ] Add `REDDIT_CLIENT_SECRET` to GitHub Secrets
- [ ] Commit and push pipeline files
- [ ] Run first scrape manually: `gh workflow run btc-scrape.yml`

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

# Set API keys (need Anthropic OR OpenAI, plus Google, plus Reddit OAuth)
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."
export GOOGLE_API_KEY="AIza..."
export REDDIT_CLIENT_ID="..."
export REDDIT_CLIENT_SECRET="..."

# Run full pipeline locally
python scripts/hn_scraper_btc.py
python scripts/reddit_scraper.py
python scripts/newsletter_monitor.py
python scripts/topic_extractor.py
python scripts/content_generator.py
```

## Key Files

| What | Where |
|------|-------|
| LLM config | `config/models.yaml` |
| Topic bank | `data/topic_bank.json` |
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
