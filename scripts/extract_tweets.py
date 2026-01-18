import os
import csv
import time
import pandas as pd
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()

CSV_FILE = 'tweets_inventory.csv'
USERNAME = 'rockoder'
BASE_URL = f'https://x.com/{USERNAME}'

def extract_tweet_data(tweet_element):
    try:
        # Get Tweet Link and ID
        link_element = tweet_element.query_selector('a[href*="/status/"]')
        if not link_element:
            return None

        href = link_element.get_attribute('href')
        tweet_link = f"https://x.com{href}"
        tweet_id = href.split('/')[-1]

        # Get Timestamp
        time_element = tweet_element.query_selector('time')
        timestamp = time_element.get_attribute('datetime') if time_element else ""

        # Get Content
        content_element = tweet_element.query_selector('[data-testid="tweetText"]')
        content = content_element.inner_text() if content_element else ""

        return {
            'Link': tweet_link,
            'ID': tweet_id,
            'Date/Time': timestamp,
            'Content': content,
            'ok_to_upload': ''
        }
    except Exception as e:
        print(f"Error extracting tweet: {e}")
        return None

def main():
    auth_token = '7764ce3c856ecd1a35e7f8e59a9adecba0893905' #os.getenv('X_AUTH_TOKEN')
    csrf_token = '50318be40b65ab8791aef604f5c56b02c37291a4c7f7d5d8314607adc2bbfed4a61001ad55405308465780e6df162504ea5b0b8855a2d828f0f01c3ab5f6968cfd538f657c0d2491c2088c5fd40d8a92' #os.getenv('X_CSRF_TOKEN')

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )

        if auth_token and csrf_token:
            print("Using session cookies for authentication...")
            context.add_cookies([
                {'name': 'auth_token', 'value': auth_token, 'domain': '.x.com', 'path': '/'},
                {'name': 'ct0', 'value': csrf_token, 'domain': '.x.com', 'path': '/'}
            ])

        page = context.new_page()
        print(f"Navigating to {BASE_URL}...")
        page.goto(BASE_URL)

        # Wait for tweets to load
        page.wait_for_selector('[data-testid="tweet"]', timeout=30000)

        tweets_data = []
        tweet_ids_seen = set()

        # Incremental update: load existing data if it exists
        if os.path.exists(CSV_FILE):
            existing_df = pd.read_csv(CSV_FILE)
            # Ensure required columns exist
            for col in ['Link', 'Date/Time', 'Content', 'ok_to_upload']:
                if col not in existing_df.columns:
                    existing_df[col] = ""

            existing_tweets = existing_df.to_dict('records')
            for t in existing_tweets:
                # Use Link as a unique identifier if ID isn't there
                tweet_ids_seen.add(t['Link'])
            tweets_data = existing_tweets

        print("Scrolling and collecting tweets...")
        last_height = page.evaluate("document.body.scrollHeight")
        scroll_attempts = 0
        max_scrolls = 10 # For trial/test, we can limit this. In full run, maybe more.

        while scroll_attempts < max_scrolls:
            tweet_elements = page.query_selector_all('[data-testid="tweet"]')
            for el in tweet_elements:
                data = extract_tweet_data(el)
                if data and data['Link'] not in tweet_ids_seen:
                    print(f"Found new tweet: {data['Link']}")
                    tweets_data.append(data)
                    tweet_ids_seen.add(data['Link'])

            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(2)
            new_height = page.evaluate("document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            scroll_attempts += 1

        # Save to CSV
        df = pd.DataFrame(tweets_data)
        # Reorder columns to match requirement: Link, Date/Time, Content, and a blank column ok_to_upload
        cols = ['Link', 'Date/Time', 'Content', 'ok_to_upload']
        # If ID was added for internal use, we can keep it or drop it.
        # Requirement says: Link, Date/Time, Content, and ok_to_upload.
        df = df[cols]
        df.to_csv(CSV_FILE, index=False)
        print(f"Saved {len(df)} tweets to {CSV_FILE}")

        browser.close()

if __name__ == "__main__":
    main()
