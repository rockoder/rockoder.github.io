#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import trafilatura
import os
from datetime import datetime, timezone
import time
import sys
from urllib.parse import urlparse

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding="utf-8")

HN_API_ITEM = "https://hacker-news.firebaseio.com/v0/item/{}.json"
HN_BEST_URL = "https://news.ycombinator.com/best?h=24"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/537.36"
}

# -----------------------------
# HN API helpers
# -----------------------------

def get_item_metadata(item_id):
    try:
        r = requests.get(HN_API_ITEM.format(item_id), timeout=10)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None


# -----------------------------
# Fetch HN Best posts
# -----------------------------

def get_best_posts(limit=30):
    url = HN_BEST_URL
    posts = []

    while len(posts) < limit:
        resp = requests.get(url, headers=HEADERS)
        if resp.status_code != 200:
            break

        soup = BeautifulSoup(resp.text, "html.parser")
        rows = soup.select("tr.athing")

        for row in rows:
            if len(posts) >= limit:
                break

            item_id = row.get("id")
            title_el = row.select_one("span.titleline > a")
            if not title_el:
                continue

            title = title_el.text.strip()
            link = title_el.get("href")

            is_internal = False
            if link.startswith("item?id="):
                link = f"https://news.ycombinator.com/{link}"
                is_internal = True
            elif link.startswith("https://news.ycombinator.com/item?id="):
                is_internal = True

            meta = get_item_metadata(item_id)
            if not meta:
                continue

            created_ts = meta.get("time")
            score = meta.get("score", 0)
            comment_count = meta.get("descendants", 0)
            author = meta.get("by", "unknown")

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
                "is_internal": is_internal
            })

        if len(posts) < limit:
            more = soup.select_one("a.morelink")
            if not more:
                break
            url = "https://news.ycombinator.com/" + more.get("href")

    return posts


# -----------------------------
# Article content
# -----------------------------

def get_article_content(url, is_internal):
    try:
        if is_internal:
            r = requests.get(url, headers=HEADERS, timeout=15)
            if r.status_code != 200:
                return "Failed to fetch internal post."
            soup = BeautifulSoup(r.text, "html.parser")
            toptext = soup.select_one("div.toptext")
            return toptext.get_text(separator="\n").strip() if toptext else "No post text."
        else:
            downloaded = trafilatura.fetch_url(url)
            if downloaded:
                extracted = trafilatura.extract(downloaded)
                if extracted:
                    return extracted

            r = requests.get(url, headers=HEADERS, timeout=15)
            if r.status_code != 200:
                return "Failed to fetch article."

            soup = BeautifulSoup(r.text, "html.parser")
            for s in soup(["script", "style"]):
                s.decompose()
            return soup.get_text(separator="\n").strip()[:5000]
    except Exception as e:
        return f"Error fetching article: {e}"


# -----------------------------
# Comments (sampled, adversarial)
# -----------------------------

def get_comments(item_id):
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

            for reply in text_el.select("div.reply"):
                reply.decompose()

            text = text_el.get_text(separator="\n").strip()

            if depth == 0:
                if len(threads) >= 5:
                    break
                current = {"top": text, "replies": []}
                threads.append(current)
            else:
                if current and len(current["replies"]) < 5:
                    current["replies"].append(text)

        return threads
    except Exception:
        return []


# -----------------------------
# Main
# -----------------------------

def main():
    posts = get_best_posts(30)
    if len(posts) < 30:
        print("ERROR: Fewer than 30 posts fetched.")
        sys.exit(1)

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_dir = f"hn_posts_{today}"
    os.makedirs(out_dir, exist_ok=True)

    for idx, post in enumerate(posts, 1):
        print(f"[{idx:02d}/30] {post['title']}")

        article = get_article_content(post["link"], post["is_internal"])
        comments = get_comments(post["id"])

        created_dt = datetime.fromtimestamp(
            post["created_ts"], tz=timezone.utc
        ).isoformat()

        path = os.path.join(out_dir, f"post{idx:02d}.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"Post ID: {post['id']}\n")
            f.write(f"Title: {post['title']}\n")
            f.write(f"Author: {post['author']}\n")
            f.write(f"Score: {post['score']}\n")
            f.write(f"Total Comments: {post['comment_count']}\n")
            f.write(f"Created At (UTC): {created_dt}\n")
            f.write(f"Domain: {post['domain']}\n")
            f.write(f"Link: {post['link']}\n\n")

            f.write("Article Content:\n")
            f.write("-" * 20 + "\n")
            f.write(article or "No content found.")
            f.write("\n\nComments:\n")
            f.write("-" * 20 + "\n")

            if not comments:
                f.write("No comments found.\n")
            else:
                for i, thread in enumerate(comments, 1):
                    f.write(f"Thread {i}:\n")
                    f.write(thread["top"] + "\n")
                    for j, reply in enumerate(thread["replies"], 1):
                        f.write(f"  Reply {j}: {reply}\n")
                    f.write("\n")

        time.sleep(1)

    print(f"\nDone. Posts saved to {out_dir}/")


if __name__ == "__main__":
    main()
