#!/usr/bin/env python3
"""
Newsletter RSS monitor for Beyond the Code content pipeline.
Monitors engineering leadership newsletters for topic ideas.
"""

import feedparser
import json
import os
import sys
import re
from datetime import datetime, timezone, timedelta
from typing import Optional

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding="utf-8")

# Newsletter RSS feeds to monitor
RSS_FEEDS = {
    "simon_willison": {
        "name": "Simon Willison's Weblog",
        "url": "https://simonwillison.net/atom/everything/",
        "focus": ["ai", "engineering", "career", "big tech"]
    },
    "marcus_on_ai": {
        "name": "Marcus on AI",
        "url": "https://garymarcus.substack.com/feed",
        "focus": ["ai", "engineering", "career", "big tech"]
    },
    "pragmatic_engineer": {
        "name": "The Pragmatic Engineer",
        "url": "https://newsletter.pragmaticengineer.com/feed",
        "focus": ["engineering", "management", "career", "big tech"]
    },
    "lenny": {
        "name": "Lenny's Newsletter",
        "url": "https://www.lennysnewsletter.com/feed",
        "focus": ["product", "growth", "leadership"]
    },
    "software_lead_weekly": {
        "name": "Software Lead Weekly",
        "url": "https://softwareleadweekly.com/feed/",
        "focus": ["leadership", "management", "engineering"]
    },
    "leaddev": {
        "name": "LeadDev",
        "url": "https://leaddev.com/rss.xml",
        "focus": ["engineering leadership", "management", "career"]
    },
    "staffeng": {
        "name": "StaffEng",
        "url": "https://staffeng.com/feed.xml",
        "focus": ["staff engineer", "principal", "career"]
    },
    "engineering_managers": {
        "name": "Engineering Managers Newsletter",
        "url": "https://www.theengineeringmanager.com/feed/",
        "focus": ["management", "leadership", "teams"]
    }
}

# Keywords for filtering relevant content
RELEVANT_KEYWORDS = [
    "ai", "career", "promotion", "leadership", "management", "culture",
    "burnout", "remote", "hiring", "interview", "performance",
    "staff engineer", "principal", "senior", "mentor", "growth",
    "communication", "team", "conflict", "feedback", "meetings",
    "politics", "influence", "visibility", "impact", "strategy" 
]

KEYWORD_PATTERN = re.compile(
    r'\b(' + '|'.join(re.escape(kw) for kw in RELEVANT_KEYWORDS) + r')\b',
    re.IGNORECASE
)


def parse_feed(feed_id: str, feed_config: dict, max_age_days: int = 7) -> list[dict]:
    """
    Parse an RSS feed and extract recent articles.

    Args:
        feed_id: Unique identifier for the feed
        feed_config: Feed configuration with name, url, focus
        max_age_days: Only include articles from last N days

    Returns:
        List of article dicts
    """
    articles = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=max_age_days)

    try:
        feed = feedparser.parse(feed_config["url"])

        if feed.bozo and feed.bozo_exception:
            print(f"  Warning parsing {feed_config['name']}: {feed.bozo_exception}")

        for entry in feed.entries:
            # Parse publication date
            pub_date = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                pub_date = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
            elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                pub_date = datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)

            # Skip old articles
            if pub_date and pub_date < cutoff:
                continue

            # Extract content
            title = entry.get("title", "")
            summary = entry.get("summary", "")
            link = entry.get("link", "")

            # Check relevance
            combined = f"{title} {summary}".lower()
            matches = KEYWORD_PATTERN.findall(combined)
            unique_matches = list(set(m.lower() for m in matches))

            articles.append({
                "feed_id": feed_id,
                "feed_name": feed_config["name"],
                "title": title,
                "summary": clean_html(summary)[:500],
                "link": link,
                "published": pub_date.isoformat() if pub_date else None,
                "matched_keywords": unique_matches,
                "relevance_score": len(unique_matches),
                "feed_focus": feed_config["focus"]
            })

    except Exception as e:
        print(f"  Error parsing {feed_config['name']}: {e}")

    return articles


def clean_html(text: str) -> str:
    """Remove HTML tags from text."""
    clean = re.sub(r'<[^>]+>', '', text)
    clean = re.sub(r'\s+', ' ', clean)
    return clean.strip()


def calculate_relevance_score(article: dict) -> float:
    """
    Calculate relevance score for an article.
    Higher = more relevant to Beyond the Code topics.
    """
    base_score = len(article.get("matched_keywords", []))

    # Bonus for high-value keywords
    high_value = ["staff engineer", "principal", "promotion", "leadership", "politics"]
    for kw in high_value:
        if kw in article.get("matched_keywords", []):
            base_score += 2

    return base_score


def main():
    """Main monitoring function."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    print("=== Newsletter Monitor for Beyond the Code ===\n")

    all_articles = []

    for feed_id, feed_config in RSS_FEEDS.items():
        print(f"Fetching {feed_config['name']}...")
        articles = parse_feed(feed_id, feed_config, max_age_days=7)
        print(f"  Found {len(articles)} recent articles")
        all_articles.extend(articles)

    print(f"\nTotal articles: {len(all_articles)}")

    # Calculate relevance and sort
    for article in all_articles:
        article["relevance_score"] = calculate_relevance_score(article)

    # Filter to only relevant articles (at least 1 keyword match)
    relevant = [a for a in all_articles if a["relevance_score"] > 0]
    relevant.sort(key=lambda x: x["relevance_score"], reverse=True)

    print(f"Relevant articles (with keyword matches): {len(relevant)}")

    # Prepare output
    output = {
        "scraped_date": today,
        "source": "newsletters",
        "feeds_checked": list(RSS_FEEDS.keys()),
        "total_articles": len(all_articles),
        "relevant_count": len(relevant),
        "articles": relevant[:30]  # Top 30 most relevant
    }

    # Save to data directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "..", "data")
    os.makedirs(data_dir, exist_ok=True)

    output_path = os.path.join(data_dir, f"newsletters_{today}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nSaved {len(relevant[:30])} articles to {output_path}")

    # Print summary
    print("\n=== Top 5 Most Relevant Articles ===")
    for i, article in enumerate(relevant[:5], 1):
        print(f"{i}. [{article['feed_name']}] {article['title'][:50]}...")
        if article.get("matched_keywords"):
            print(f"   Keywords: {', '.join(article['matched_keywords'][:5])}")


if __name__ == "__main__":
    main()
