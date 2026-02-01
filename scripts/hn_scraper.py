#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import trafilatura
import os
from datetime import datetime, timezone
import time
import sys

# Set encoding for output to handle special characters
sys.stdout.reconfigure(encoding='utf-8')

def get_best_posts(limit=30):
    url = "https://news.ycombinator.com/best?h=24"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    posts = []
    while len(posts) < limit:
        print(f"Fetching posts from {url}...")
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch HN: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        athings = soup.select('tr.athing')

        for tr in athings:
            if len(posts) >= limit:
                break

            post_id = tr.get('id')
            title_line = tr.select_one('span.titleline > a')
            if not title_line:
                continue

            title = title_line.text
            link = title_line.get('href')

            # Internal links
            is_internal = False
            if link.startswith('item?id='):
                link = f"https://news.ycombinator.com/{link}"
                is_internal = True
            elif link.startswith('https://news.ycombinator.com/item?id='):
                is_internal = True

            # Metadata tr
            metadata_tr = tr.find_next_sibling('tr')
            score_el = metadata_tr.select_one('span.score')
            score = score_el.text if score_el else "0 points"
            author_el = metadata_tr.select_one('a.hnuser')
            author = author_el.text if author_el else "None"

            posts.append({
                'id': post_id,
                'title': title,
                'link': link,
                'score': score,
                'author': author,
                'is_internal': is_internal
            })

        if len(posts) < limit:
            more_link = soup.select_one('a.morelink')
            if more_link:
                url = "https://news.ycombinator.com/" + more_link.get('href')
            else:
                break

    return posts

def get_article_content(url, is_internal):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    if is_internal:
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                toptext = soup.select_one('div.toptext')
                return toptext.get_text(separator='\n').strip() if toptext else "No post text content."
            return f"Failed to fetch internal post: {response.status_code}"
        except Exception as e:
            return f"Error fetching internal post: {e}"
    else:
        try:
            # First try trafilatura as it is good for "clean version"
            downloaded = trafilatura.fetch_url(url)
            if downloaded:
                content = trafilatura.extract(downloaded)
                if content:
                    return content

            # Fallback to simple requests + bs4 if trafilatura fails or returns nothing
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                # Basic cleaning if trafilatura failed
                soup = BeautifulSoup(response.text, 'html.parser')
                for script in soup(["script", "style"]):
                    script.decompose()
                return soup.get_text(separator='\n').strip()[:5000] # Limit size

            return f"Failed to fetch article: {response.status_code}"
        except Exception as e:
            return f"Error fetching article: {e}"

def get_comments(item_id):
    url = f"https://news.ycombinator.com/item?id={item_id}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        comment_rows = soup.select('tr.comtr')

        threads = []
        current_thread = None

        for row in comment_rows:
            indent_td = row.select_one('td.ind')
            if indent_td and indent_td.has_attr('indent'):
                depth = int(indent_td.get('indent', 0))
            else:
                indent_img = row.select_one('td.ind img')
                width = int(indent_img.get('width', 0)) if indent_img else 0
                depth = width // 40

            comment_text_el = row.select_one('.commtext')
            if not comment_text_el:
                continue

            # Clean up: remove reply link
            for reply_link in comment_text_el.select('div.reply'):
                reply_link.decompose()

            text = comment_text_el.get_text(separator='\n').strip()

            if depth == 0:
                if len(threads) >= 5:
                    break
                current_thread = {'top': text, 'replies': []}
                threads.append(current_thread)
            else:
                if current_thread and len(current_thread['replies']) < 5:
                    current_thread['replies'].append(text)

        return threads
    except Exception as e:
        print(f"Error fetching comments: {e}")
        return []

def main():
    posts = get_best_posts(30)
    print(f"Found {len(posts)} posts.")

    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    dir_name = f"hn_posts_{today}"
    os.makedirs(dir_name, exist_ok=True)

    for i, post in enumerate(posts, 1):
        filename = f"post{i:02d}.txt"
        filepath = os.path.join(dir_name, filename)
        print(f"[{i:02d}/30] Processing: {post['title']}")

        # Article Content
        content = get_article_content(post['link'], post['is_internal'])

        # Comments
        threads = get_comments(post['id'])

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Title: {post['title']}\n")
            f.write(f"Author: {post['author']}\n")
            f.write(f"Score: {post['score']}\n")
            f.write(f"Link: {post['link']}\n\n")
            f.write("Article Content:\n")
            f.write("-" * 20 + "\n")
            f.write(content if content else "No content found.")
            f.write("\n\nComments:\n")
            f.write("-" * 20 + "\n")

            if not threads:
                f.write("No comments found.\n")
            else:
                for t_idx, thread in enumerate(threads, 1):
                    f.write(f"Thread {t_idx}:\n")
                    f.write(f"{thread['top']}\n")
                    for r_idx, reply in enumerate(thread['replies'], 1):
                        f.write(f"  Reply {r_idx}: {reply}\n")
                    f.write("\n")

        # Be polite to servers
        time.sleep(1)

    print(f"Done! Posts saved to {dir_name}/")

if __name__ == "__main__":
    main()
