#!/usr/bin/env python3
"""
Topic extractor for Beyond the Code content pipeline.
Aggregates scraped content and uses LLM to extract recurring themes.
"""

import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding="utf-8")

# Import our LLM client
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))
from llm_client import LLMClient

# Timeliness hooks - seasonal relevance
TIMELINESS_HOOKS = {
    1: ["new year goals", "job market", "layoffs", "new beginnings", "resolutions"],
    2: ["layoffs", "job search", "performance improvement plans", "winter blues"],
    3: ["promotion cycles", "annual reviews fallout", "job market picks up"],
    4: ["Q2 planning", "mid-year anxiety starting", "spring energy"],
    5: ["summer planning", "vacation guilt", "promotion results"],
    6: ["mid-year reviews", "H1 reflections", "summer slowdown begins"],
    7: ["summer slowdown", "quiet quitting peak", "vacation coverage"],
    8: ["back to school energy", "H2 planning", "new projects"],
    9: ["fall energy", "Q4 prep", "year-end push begins"],
    10: ["performance review prep", "Q4 crunch", "year-end politics"],
    11: ["calibration season", "stack ranking", "promotion packets"],
    12: ["year-end reflections", "holiday politics", "new year job search prep"]
}

TOPIC_EXTRACTION_PROMPT = """You are analyzing content scraped from Hacker News, Reddit, and engineering newsletters to identify compelling topics for a blog called "Beyond the Code."

TARGET AUDIENCE: Senior Engineers and above (Staff, Principal, Directors) in corporate tech settings.

CONTENT FOCUS: Non-technical topics that matter to senior technical professionals:
- Career navigation, promotions, and politics
- Management dynamics and organizational behavior
- Burnout, work-life balance, remote work
- The hidden rules of corporate advancement
- Team dynamics and leadership challenges

CURRENT TIMELINESS CONTEXT (month {month}): {timeliness_context}

Here is today's scraped content:

{content}

---

Extract 3-5 compelling topics from this content. For each topic:

1. THEME: A clear, specific topic statement (not generic like "career growth" - be specific like "Why high performers get passed over for promotion")

2. CONTRARIAN_ANGLE: What's the conventional wisdom on this topic, and what's the contrarian take that would make senior engineers stop and think? The best angles challenge something everyone assumes is true.

3. ENGAGEMENT_SIGNALS: What in the source material suggests this resonates? (high comment counts, heated debates, personal anecdotes)

4. TIMELINESS_FIT: How does this connect to current seasonal relevance? (performance reviews, layoffs, etc.)

5. SOURCES: List the source IDs (hn:id, reddit:id, newsletter:feed_id) that informed this topic

6. SCORE: Rate 1-100 based on:
   - Engagement signals from source (30%)
   - Strength of contrarian angle (30%)
   - Fit with Beyond the Code themes (20%)
   - Timeliness (20%)

Respond in JSON format:
```json
{{
  "topics": [
    {{
      "theme": "...",
      "contrarian_angle": "...",
      "engagement_signals": "...",
      "timeliness_fit": "...",
      "sources": ["hn:123", "reddit:abc"],
      "score": 85
    }}
  ]
}}
```
"""


def load_scraped_data(data_dir: Path, date_str: str) -> dict:
    """Load all scraped data for a given date."""
    data = {
        "hn": None,
        "reddit": None,
        "newsletters": None
    }

    # Try to load each source
    hn_path = data_dir / f"hn_nontech_{date_str}.json"
    if hn_path.exists():
        with open(hn_path, "r") as f:
            data["hn"] = json.load(f)

    reddit_path = data_dir / f"reddit_{date_str}.json"
    if reddit_path.exists():
        with open(reddit_path, "r") as f:
            data["reddit"] = json.load(f)

    newsletters_path = data_dir / f"newsletters_{date_str}.json"
    if newsletters_path.exists():
        with open(newsletters_path, "r") as f:
            data["newsletters"] = json.load(f)

    return data


def format_content_for_llm(data: dict, max_items: int = 15) -> str:
    """Format scraped data into a prompt-friendly format."""
    sections = []

    # Format HN posts
    if data["hn"] and data["hn"].get("posts"):
        hn_section = "## Hacker News Posts\n\n"
        for post in data["hn"]["posts"][:max_items]:
            hn_section += f"### [hn:{post['id']}] {post['title']}\n"
            hn_section += f"Score: {post['score']} | Comments: {post['comment_count']}\n"
            if post.get("post_text"):
                hn_section += f"Text: {post['post_text'][:300]}...\n"
            if post.get("comments"):
                hn_section += "Top comments:\n"
                for thread in post["comments"][:2]:
                    hn_section += f"- {thread['top'][:200]}...\n"
            hn_section += "\n"
        sections.append(hn_section)

    # Format Reddit posts
    if data["reddit"] and data["reddit"].get("posts"):
        reddit_section = "## Reddit Posts\n\n"
        for post in data["reddit"]["posts"][:max_items]:
            reddit_section += f"### [reddit:{post['id']}] r/{post['subreddit']}: {post['title']}\n"
            reddit_section += f"Score: {post['score']} | Comments: {post['comment_count']}\n"
            if post.get("selftext"):
                reddit_section += f"Text: {post['selftext'][:300]}...\n"
            if post.get("comments"):
                reddit_section += "Top comments:\n"
                for comment in post["comments"][:2]:
                    reddit_section += f"- {comment['body'][:200]}...\n"
            reddit_section += "\n"
        sections.append(reddit_section)

    # Format newsletter articles
    if data["newsletters"] and data["newsletters"].get("articles"):
        newsletter_section = "## Newsletter Articles\n\n"
        for article in data["newsletters"]["articles"][:max_items]:
            newsletter_section += f"### [newsletter:{article['feed_id']}] {article['title']}\n"
            newsletter_section += f"Source: {article['feed_name']}\n"
            if article.get("summary"):
                newsletter_section += f"Summary: {article['summary'][:200]}...\n"
            newsletter_section += "\n"
        sections.append(newsletter_section)

    return "\n".join(sections)


def load_topic_bank(data_dir: Path) -> dict:
    """Load existing topic bank."""
    bank_path = data_dir / "topic_bank.json"
    if bank_path.exists():
        with open(bank_path, "r") as f:
            return json.load(f)
    return {"topics": [], "last_updated": None}


def save_topic_bank(data_dir: Path, bank: dict):
    """Save topic bank."""
    bank_path = data_dir / "topic_bank.json"
    with open(bank_path, "w") as f:
        json.dump(bank, f, indent=2, ensure_ascii=False)


def dedupe_topics(new_topics: list, existing_topics: list) -> list:
    """Remove topics too similar to existing ones."""
    existing_themes = {t["theme"].lower() for t in existing_topics}

    unique = []
    for topic in new_topics:
        theme_lower = topic["theme"].lower()
        # Simple dedupe: check if theme is too similar
        is_dupe = any(
            theme_lower in existing or existing in theme_lower
            for existing in existing_themes
        )
        if not is_dupe:
            unique.append(topic)
            existing_themes.add(theme_lower)

    return unique


def main():
    """Main extraction function."""
    today = datetime.now(timezone.utc)
    date_str = today.strftime("%Y-%m-%d")
    month = today.month

    print("=== Topic Extractor for Beyond the Code ===\n")

    # Setup paths
    data_dir = script_dir.parent / "data"

    # Load scraped data
    print(f"Loading scraped data for {date_str}...")
    data = load_scraped_data(data_dir, date_str)

    sources_found = sum(1 for v in data.values() if v is not None)
    if sources_found == 0:
        print("No scraped data found for today. Run the scrapers first.")
        sys.exit(1)

    print(f"  Found data from {sources_found} sources")

    # Format content for LLM
    content = format_content_for_llm(data)
    if not content.strip():
        print("No content to analyze.")
        sys.exit(1)

    print(f"  Formatted {len(content)} characters of content")

    # Get timeliness context
    timeliness_context = ", ".join(TIMELINESS_HOOKS.get(month, []))

    # Build prompt
    prompt = TOPIC_EXTRACTION_PROMPT.format(
        month=month,
        timeliness_context=timeliness_context,
        content=content
    )

    # Call LLM
    print("\nExtracting topics with LLM...")
    client = LLMClient()

    try:
        response = client.generate("topic_extraction", prompt)

        # Parse JSON from response
        # Handle markdown code blocks
        if "```json" in response:
            json_str = response.split("```json")[1].split("```")[0]
        elif "```" in response:
            json_str = response.split("```")[1].split("```")[0]
        else:
            json_str = response

        result = json.loads(json_str.strip())
        new_topics = result.get("topics", [])

    except json.JSONDecodeError as e:
        print(f"Failed to parse LLM response as JSON: {e}")
        print(f"Response was: {response[:500]}...")
        sys.exit(1)
    except Exception as e:
        print(f"LLM call failed: {e}")
        sys.exit(1)

    print(f"  Extracted {len(new_topics)} topics")

    # Load existing topic bank
    bank = load_topic_bank(data_dir)
    existing_topics = bank.get("topics", [])

    # Add metadata to new topics
    for topic in new_topics:
        topic["id"] = str(uuid.uuid4())[:8]
        topic["extracted_date"] = date_str
        topic["used"] = False

    # Dedupe against existing
    unique_topics = dedupe_topics(new_topics, existing_topics)
    print(f"  {len(unique_topics)} unique topics after deduplication")

    # Add to bank
    bank["topics"] = unique_topics + existing_topics
    bank["last_updated"] = date_str

    # Keep bank manageable (last 100 topics)
    bank["topics"] = bank["topics"][:100]

    # Save
    save_topic_bank(data_dir, bank)
    print(f"\nTopic bank updated with {len(unique_topics)} new topics")

    # Print summary
    print("\n=== New Topics Extracted ===")
    for i, topic in enumerate(unique_topics, 1):
        print(f"\n{i}. {topic['theme']}")
        print(f"   Score: {topic['score']}")
        print(f"   Contrarian angle: {topic['contrarian_angle'][:100]}...")


if __name__ == "__main__":
    main()
