import os
import pandas as pd
from playwright.sync_api import sync_playwright
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

CSV_FILE = 'tweets_inventory.csv'
POSTS_DIR = '_posts'
IMAGES_DIR = 'assets/images/tweets'

os.makedirs(POSTS_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

def capture_tweet_screenshot(page, tweet_url, output_path):
    print(f"Capturing screenshot for {tweet_url}...")
    try:
        page.goto(tweet_url, wait_until="networkidle")
        # Wait for the tweet to be visible
        tweet_selector = '[data-testid="tweet"]'
        page.wait_for_selector(tweet_selector, timeout=20000)

        # Hide some annoying elements if possible (like login banners)
        page.evaluate("""
            () => {
                const selectors = [
                    '#layers', // Banners
                    '[data-testid="BottomBar"]'
                ];
                selectors.forEach(s => {
                    const el = document.querySelector(s);
                    if (el) el.style.display = 'none';
                });
            }
        """)

        tweet_element = page.query_selector(tweet_selector)
        if tweet_element:
            tweet_element.screenshot(path=output_path)
            return True
    except Exception as e:
        print(f"Failed to capture screenshot for {tweet_url}: {e}")
        return False
    return False

def generate_post(tweet_data, screenshot_path):
    link = tweet_data['Link']
    tweet_id = link.split('/')[-1]
    raw_date = tweet_data['Date/Time']
    content = tweet_data['Content']

    # Parse date
    try:
        dt = datetime.fromisoformat(raw_date.replace('Z', '+00:00'))
    except:
        dt = datetime.now()

    date_str = dt.strftime('%Y-%m-%d')
    post_filename = f"{date_str}-tweet-{tweet_id}.md"
    post_path = os.path.join(POSTS_DIR, post_filename)

    if os.path.exists(post_path):
        print(f"Post {post_filename} already exists. Skipping.")
        return

    title = f"Tweet from {date_str}"

    front_matter = f"""---
layout: tweet
title: "{title}"
date: {dt.isoformat()}
tweet_url: {link}
tweet_id: {tweet_id}
screenshot: /{screenshot_path}
---

{content}
"""
    with open(post_path, 'w') as f:
        f.write(front_matter)
    print(f"Generated post: {post_path}")

def main():
    if not os.path.exists(CSV_FILE):
        print(f"{CSV_FILE} not found.")
        return

    df = pd.read_csv(CSV_FILE)
    approved_tweets = df[df['ok_to_upload'] == 'y']

    if approved_tweets.empty:
        print("No tweets approved for upload.")
        return

    auth_token = os.getenv('X_AUTH_TOKEN')
    csrf_token = os.getenv('X_CSRF_TOKEN')

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            viewport={'width': 1280, 'height': 800}
        )

        if auth_token and csrf_token:
            context.add_cookies([
                {'name': 'auth_token', 'value': auth_token, 'domain': '.x.com', 'path': '/'},
                {'name': 'ct0', 'value': csrf_token, 'domain': '.x.com', 'path': '/'}
            ])

        page = context.new_page()

        for _, row in approved_tweets.iterrows():
            tweet_id = row['Link'].split('/')[-1]
            screenshot_path = os.path.join(IMAGES_DIR, f"{tweet_id}.png")
            # Ensure forward slashes for the Jekyll front matter path
            web_screenshot_path = screenshot_path.replace(os.sep, '/')

            success = True
            if not os.path.exists(screenshot_path):
                success = capture_tweet_screenshot(page, row['Link'], screenshot_path)

            if success or os.path.exists(screenshot_path):
                generate_post(row, web_screenshot_path)
            else:
                print(f"Skipping post generation for {row['Link']} due to screenshot failure.")

        browser.close()

if __name__ == "__main__":
    main()
