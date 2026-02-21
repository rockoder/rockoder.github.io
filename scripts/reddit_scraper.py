#!/usr/bin/env python3
"""
Reddit scraper for Beyond the Code content pipeline.
Scrapes career-focused subreddits for Sr+ engineer discussions.
"""

import requests
import json
import os
import sys
import time
from datetime import datetime, timezone
from typing import Optional

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding="utf-8")

# Target subreddits for career/workplace content
SUBREDDITS = [
    "experienceddevs",      # Primary - Sr+ engineer discussions
    "cscareerquestions",    # Broader career topics
    "managers",             # Management perspective
]

# User-Agent must identify the app (Reddit requirement)
USER_AGENT = "BeyondTheCode/1.0 (by /u/beyond_the_code_bot)"

# OAuth credentials from environment
REDDIT_CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.environ.get("REDDIT_CLIENT_SECRET")

# OAuth endpoint
OAUTH_URL = "https://oauth.reddit.com/r/{subreddit}/top"
TOKEN_URL = "https://www.reddit.com/api/v1/access_token"

# Global access token
_access_token = None


def get_access_token() -> Optional[str]:
    """Get OAuth access token using client credentials flow."""
    global _access_token
    if _access_token:
        return _access_token

    if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
        print("Warning: Reddit OAuth credentials not set, scraping will likely fail")
        return None

    auth = requests.auth.HTTPBasicAuth(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET)
    headers = {"User-Agent": USER_AGENT}
    data = {"grant_type": "client_credentials"}

    try:
        resp = requests.post(TOKEN_URL, auth=auth, headers=headers, data=data, timeout=15)
        if resp.status_code == 200:
            _access_token = resp.json().get("access_token")
            print("Successfully authenticated with Reddit OAuth")
            return _access_token
        else:
            print(f"OAuth authentication failed: {resp.status_code}")
            return None
    except Exception as e:
        print(f"OAuth error: {e}")
        return None


def get_subreddit_posts(subreddit: str, time_filter: str = "day", limit: int = 25) -> list[dict]:
    """
    Fetch top posts from a subreddit using OAuth API.

    Args:
        subreddit: Subreddit name (without r/)
        time_filter: 'hour', 'day', 'week', 'month', 'year', 'all'
        limit: Max posts to fetch (max 100)

    Returns:
        List of post data dicts
    """
    token = get_access_token()
    if not token:
        print(f"  Skipping r/{subreddit}: No OAuth token available")
        return []

    url = OAUTH_URL.format(subreddit=subreddit)
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": USER_AGENT,
    }
    params = {
        "t": time_filter,
        "limit": min(limit, 100)
    }

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=15)
        if resp.status_code == 429:
            print(f"  Rate limited on r/{subreddit}, waiting...")
            time.sleep(60)
            resp = requests.get(url, headers=headers, params=params, timeout=15)

        if resp.status_code != 200:
            print(f"  Failed to fetch r/{subreddit}: {resp.status_code}")
            return []

        data = resp.json()
        posts = []

        for child in data.get("data", {}).get("children", []):
            post_data = child.get("data", {})

            # Skip stickied posts (usually rules/megathreads)
            if post_data.get("stickied"):
                continue

            posts.append({
                "id": post_data.get("id"),
                "subreddit": subreddit,
                "title": post_data.get("title"),
                "author": post_data.get("author"),
                "score": post_data.get("score", 0),
                "upvote_ratio": post_data.get("upvote_ratio", 0),
                "comment_count": post_data.get("num_comments", 0),
                "created_utc": post_data.get("created_utc"),
                "selftext": post_data.get("selftext", ""),
                "url": f"https://reddit.com{post_data.get('permalink')}",
                "is_self": post_data.get("is_self", True),
                "link_flair_text": post_data.get("link_flair_text"),
            })

        return posts

    except Exception as e:
        print(f"  Error fetching r/{subreddit}: {e}")
        return []


def get_post_comments(subreddit: str, post_id: str, limit: int = 10) -> list[dict]:
    """
    Fetch top comments for a post using OAuth API.

    Args:
        subreddit: Subreddit name
        post_id: Reddit post ID
        limit: Max comments to fetch

    Returns:
        List of comment dicts with text, author, score
    """
    token = get_access_token()
    if not token:
        return []

    url = f"https://oauth.reddit.com/r/{subreddit}/comments/{post_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": USER_AGENT,
    }
    params = {"limit": limit, "sort": "top"}

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=15)
        if resp.status_code != 200:
            return []

        data = resp.json()
        if len(data) < 2:
            return []

        comments = []
        comment_listing = data[1].get("data", {}).get("children", [])

        for child in comment_listing[:limit]:
            if child.get("kind") != "t1":  # t1 = comment
                continue

            comment_data = child.get("data", {})
            if comment_data.get("author") == "AutoModerator":
                continue

            comments.append({
                "id": comment_data.get("id"),
                "author": comment_data.get("author"),
                "score": comment_data.get("score", 0),
                "body": comment_data.get("body", ""),
                "depth": comment_data.get("depth", 0),
            })

        return comments

    except Exception as e:
        print(f"  Error fetching comments for {post_id}: {e}")
        return []


def calculate_engagement_score(post: dict) -> float:
    """
    Calculate an engagement score for ranking posts.
    Weights comments more heavily than upvotes for discussion quality.
    """
    score = post.get("score", 0)
    comments = post.get("comment_count", 0)
    ratio = post.get("upvote_ratio", 0.5)

    # Formula: emphasize discussion (comments) and controversy (ratio near 0.5)
    controversy_bonus = 1.0 + (0.5 - abs(ratio - 0.5))
    return (score * 0.3 + comments * 2.0) * controversy_bonus


def main():
    """Main scraping function."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    print("=== Reddit Scraper for Beyond the Code ===\n")

    all_posts = []

    for subreddit in SUBREDDITS:
        print(f"Scraping r/{subreddit}...")
        posts = get_subreddit_posts(subreddit, time_filter="day", limit=25)
        print(f"  Found {len(posts)} posts")
        all_posts.extend(posts)
        time.sleep(2)  # Be nice to Reddit servers

    print(f"\nTotal posts: {len(all_posts)}")

    # Calculate engagement scores and sort
    for post in all_posts:
        post["engagement_score"] = calculate_engagement_score(post)

    all_posts.sort(key=lambda x: x["engagement_score"], reverse=True)

    # Fetch comments for top posts
    print("\nFetching comments for top posts...")
    top_posts = all_posts[:20]

    for i, post in enumerate(top_posts):
        print(f"  [{i+1}/{len(top_posts)}] r/{post['subreddit']}: {post['title'][:40]}...")
        post["comments"] = get_post_comments(post["subreddit"], post["id"], limit=10)
        time.sleep(1)

    # Prepare output
    output = {
        "scraped_date": today,
        "source": "reddit",
        "subreddits": SUBREDDITS,
        "total_posts": len(all_posts),
        "posts": top_posts
    }

    # Save to data directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "..", "data")
    os.makedirs(data_dir, exist_ok=True)

    output_path = os.path.join(data_dir, f"reddit_{today}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nSaved {len(top_posts)} posts to {output_path}")

    # Print summary
    print("\n=== Top 5 Posts by Engagement ===")
    for i, post in enumerate(top_posts[:5], 1):
        print(f"{i}. [r/{post['subreddit']}] {post['title'][:50]}...")
        print(f"   Score: {post['score']} | Comments: {post['comment_count']} | Engagement: {post['engagement_score']:.1f}")


if __name__ == "__main__":
    main()
