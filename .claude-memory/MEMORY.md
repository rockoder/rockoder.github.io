# Project Memory - rockoder.github.io

## Workflow Rules

### Before Git Push: Update Documentation
When making code changes that affect configuration, setup, or behavior:
1. Update relevant docs in `docs/` before committing
2. Key docs: `docs/beyond-the-code-pipeline.md`, `docs/btc-quick-reference.md`
3. Document as if the next person won't have context

### Documentation Locations
| Change Type | Update These Files |
|-------------|-------------------|
| New GitHub secrets | `docs/beyond-the-code-pipeline.md` (Setup section), `docs/btc-quick-reference.md` (Checklist) |
| New env vars | Same as above, plus `.env` examples |
| Workflow changes | `docs/beyond-the-code-pipeline.md` (Architecture diagram, Schedule section) |
| New scripts | `docs/beyond-the-code-pipeline.md` (File Reference section) |
| Troubleshooting fixes | `docs/btc-quick-reference.md` (Troubleshooting section) |

## Project Structure

### Beyond the Code Pipeline
- **Scraping**: `scripts/hn_scraper_btc.py`, `scripts/reddit_scraper.py`, `scripts/newsletter_monitor.py`
- **Processing**: `scripts/topic_extractor.py`, `scripts/content_generator.py`
- **Config**: `config/models.yaml`
- **Workflows**: `.github/workflows/btc-scrape.yml`, `.github/workflows/btc-generate.yml`

### Required Secrets (GitHub Actions)
- `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` (at least one)
- `GOOGLE_API_KEY`
- `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET` (OAuth for Reddit API)
- `GROQ_API_KEY` (optional)

## Known Issues & Solutions

### Reddit 403 on GitHub Actions
Reddit blocks datacenter IPs. Fixed by using OAuth API instead of public JSON API.
- Requires `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET`
- Create "script" app at reddit.com/prefs/apps
