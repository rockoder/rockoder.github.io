#!/usr/bin/env python3
"""
Hacker News scraper for Beyond the Code content pipeline.
Filters for non-tech career/workplace topics and Ask HN discussions.
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import sys
import time
import re
from datetime import datetime, timezone
from typing import Optional
from urllib.parse import urlparse

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding="utf-8")

HN_API_ITEM = "https://hacker-news.firebaseio.com/v0/item/{}.json"
HN_BEST_URL = "https://news.ycombinator.com/best"
HN_ASK_URL = "https://news.ycombinator.com/ask"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/537.36"
}

# Keywords for filtering non-tech career/workplace topics
NONTECH_KEYWORDS = [
    "career", "promotion", "burnout", "management", "layoffs", "layoff",
    "remote", "salary", "interview", "hiring", "fired", "quit", "quitting",
    "toxic", "culture", "politics", "leadership", "manager", "boss",
    "work-life", "worklife", "balance", "wfh", "rto", "return to office",
    "performance review", "pip", "negotiation", "negotiate", "comp",
    "compensation", "equity", "stock", "vesting", "job market", "job search",
    "networking", "mentor", "mentorship", "imposter", "impostor",
    "staff engineer", "principal", "senior", "lead", "director", "vp",
    "startup", "big tech", "faang", "maang", "corporate", "enterprise",
    "consulting", "contractor", "freelance", "side project", "hustle",
    "advice", "lessons", "learned", "mistake", "regret", "success", "failure",
    "happiness", "fulfillment", "meaning", "purpose", "motivation",
    "communication", "conflict", "feedback", "difficult conversation",
    "team", "teamwork", "collaboration", "meeting", "meetings"
]

# Compile regex pattern for efficiency
NONTECH_PATTERN = re.compile(
    r'\b(' + '|'.join(re.escape(kw) for kw in NONTECH_KEYWORDS) + r')\b',
    re.IGNORECASE
)


def get_item_metadata(item_id: str) -> Optional[dict]:
    """Fetch item metadata from HN API."""
    try:
        r = requests.get(HN_API_ITEM.format(item_id), timeout=10)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None


def is_nontech_topic(title: str, text: str = "") -> tuple[bool, list[str]]:
    """
    Check if a post is about non-tech career/workplace topics.
    Returns (is_match, matched_keywords).
    """
    combined = f"{title} {text}".lower()
    matches = NONTECH_PATTERN.findall(combined)
    unique_matches = list(set(m.lower() for m in matches))
    return len(unique_matches) > 0, unique_matches


def is_ask_hn(title: str) -> bool:
    """Check if this is an Ask HN post."""
    return title.lower().startswith("ask hn:")


def get_comment_threads(item_id: str, max_threads: int = 5, max_replies: int = 5) -> list[dict]:
    """
    Fetch top comment threads for a post.
    Returns list of {top: str, replies: [str], score: int, author: str}
    """
    url = f"https://news.ycombinator.com/item?id={item_id}"

    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code != 200:
            return []

        soup = BeautifulSoup(r.text, "html.parser")
        rows = soup.select("tr.comtr")

        threads = []
        current = None

        for row in rows:
            indent = row.select_one("td.ind img")
            depth = int(indent["width"]) // 40 if indent else 0

            text_el = row.select_one(".commtext")
            if not text_el:
                continue

            # Remove reply links
            for reply in text_el.select("div.reply"):
                reply.decompose()

            text = text_el.get_text(separator="\n").strip()

            # Get comment author
            author_el = row.select_one("a.hnuser")
            author = author_el.text if author_el else "unknown"

            if depth == 0:
                if len(threads) >= max_threads:
                    break
                current = {
                    "top": text,
                    "author": author,
                    "replies": []
                }
                threads.append(current)
            else:
                if current and len(current["replies"]) < max_replies:
                    current["replies"].append({
                        "text": text,
                        "author": author,
                        "depth": depth
                    })

        return threads
    except Exception as e:
        print(f"Error fetching comments for {item_id}: {e}")
        return []


def scrape_hn_page(url: str, seen_ids: set, limit: int = 50) -> list[dict]:
    """Scrape a single HN page for posts."""
    posts = []

    while len(posts) < limit:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            break

        soup = BeautifulSoup(resp.text, "html.parser")
        rows = soup.select("tr.athing")

        for row in rows:
            if len(posts) >= limit:
                break

            item_id = row.get("id")
            if item_id in seen_ids:
                continue

            title_el = row.select_one("span.titleline > a")
            if not title_el:
                continue

            title = title_el.text.strip()
            link = title_el.get("href")

            # Fix internal links
            is_internal = False
            if link.startswith("item?id="):
                link = f"https://news.ycombinator.com/{link}"
                is_internal = True
            elif link.startswith("https://news.ycombinator.com/item?id="):
                is_internal = True

            # Get metadata
            meta = get_item_metadata(item_id)
            if not meta:
                continue

            seen_ids.add(item_id)

            created_ts = meta.get("time")
            score = meta.get("score", 0)
            comment_count = meta.get("descendants", 0)
            author = meta.get("by", "unknown")
            post_text = meta.get("text", "")

            parsed = urlparse(link)
            domain = parsed.netloc if parsed.netloc else "news.ycombinator.com"

            posts.append({
                "id": item_id,
                "title": title,
                "link": link,
                "domain": domain,
                "author": author,
                "score": score,
                "comment_count": comment_count,
                "created_ts": created_ts,
                "is_internal": is_internal,
                "post_text": post_text,
                "is_ask_hn": is_ask_hn(title)
            })

        # Check for more pages
        if len(posts) < limit:
            more = soup.select_one("a.morelink")
            if not more:
                break
            url = "https://news.ycombinator.com/" + more.get("href")
        else:
            break

    return posts


def filter_nontech_posts(posts: list[dict]) -> list[dict]:
    """Filter posts to only include non-tech career/workplace topics."""
    filtered = []
    for post in posts:
        is_match, keywords = is_nontech_topic(post["title"], post.get("post_text", ""))
        if is_match or post["is_ask_hn"]:
            post["matched_keywords"] = keywords
            filtered.append(post)
    return filtered


def enrich_with_comments(posts: list[dict], max_posts: int = 20) -> list[dict]:
    """Add comment threads to posts (limited to avoid rate limiting)."""
    enriched = []
    for i, post in enumerate(posts[:max_posts]):
        print(f"  [{i+1}/{min(len(posts), max_posts)}] Fetching comments for: {post['title'][:50]}...")
        post["comments"] = get_comment_threads(post["id"])
        enriched.append(post)
        time.sleep(0.5)  # Be nice to HN servers
    return enriched


def main():
    """Main scraping function."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    seen_ids = set()

    print("=== HN Non-Tech Scraper for Beyond the Code ===\n")

    # Scrape from Best page
    print("Scraping HN Best...")
    best_posts = scrape_hn_page(HN_BEST_URL, seen_ids, limit=100)
    print(f"  Found {len(best_posts)} posts on Best page")

    # Scrape from Ask HN page
    print("\nScraping Ask HN...")
    ask_posts = scrape_hn_page(HN_ASK_URL, seen_ids, limit=50)
    print(f"  Found {len(ask_posts)} posts on Ask HN page")

    # Combine and filter
    all_posts = best_posts + ask_posts
    print(f"\nTotal posts scraped: {len(all_posts)}")

    nontech_posts = filter_nontech_posts(all_posts)
    print(f"Non-tech/career posts after filtering: {len(nontech_posts)}")

    # Sort by score (engagement proxy)
    nontech_posts.sort(key=lambda x: x["score"], reverse=True)

    # Enrich top posts with comments
    print("\nFetching comments for top posts...")
    enriched_posts = enrich_with_comments(nontech_posts, max_posts=20)

    # Prepare output
    output = {
        "scraped_date": today,
        "source": "hacker_news",
        "total_scraped": len(all_posts),
        "nontech_count": len(nontech_posts),
        "posts": enriched_posts
    }

    # Save to data directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "..", "data")
    os.makedirs(data_dir, exist_ok=True)

    output_path = os.path.join(data_dir, f"hn_nontech_{today}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nSaved {len(enriched_posts)} posts to {output_path}")

    # Print summary
    print("\n=== Top 5 Posts ===")
    for i, post in enumerate(enriched_posts[:5], 1):
        print(f"{i}. [{post['score']} pts] {post['title'][:60]}...")
        if post.get("matched_keywords"):
            print(f"   Keywords: {', '.join(post['matched_keywords'][:5])}")


if __name__ == "__main__":
    main()
