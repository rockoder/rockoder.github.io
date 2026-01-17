# X (Twitter) Sync Setup Guide

To sync your tweets to your blog, the extraction script needs authentication to view your profile and bypass basic scraping protections. You can choose one of the following two methods.

## Method 1: Session Cookies (Recommended for Personal Archive)
This method uses your existing browser session. It is the most reliable way to fetch older tweets without a paid API plan.

### Steps to get Session Cookies:
1. Open [x.com](https://x.com) in your browser and ensure you are logged in.
2. Open **Developer Tools** (F12 or Right-click > Inspect).
3. Go to the **Application** tab (Chrome/Edge) or **Storage** tab (Firefox).
4. In the left sidebar, expand **Cookies** and select `https://x.com`.
5. Find and copy the values for:
   - `auth_token`
   - `ct0` (This is your CSRF token)
6. Create a file named `.env` in the root of this repository and add them:
   ```env
   X_AUTH_TOKEN=your_auth_token_here
   X_CSRF_TOKEN=your_ct0_here
   ```

## Method 2: Official X API
If you have an X Developer account, you can use the official API. Note that the Free tier has significant limitations.

### Steps:
1. Go to the [X Developer Portal](https://developer.x.com/en/portal/dashboard).
2. Create a new Project and App.
3. Generate your **API Key**, **API Key Secret**, **Access Token**, and **Access Token Secret**.
4. Add them to your `.env` file:
   ```env
   X_API_KEY=your_api_key
   X_API_SECRET=your_api_secret
   X_ACCESS_TOKEN=your_access_token
   X_ACCESS_TOKEN_SECRET=your_access_token_secret
   ```

---

## Next Steps
Once you have configured your `.env` file, you can run the extraction script:
```bash
python3 scripts/extract_tweets.py
```
This will generate `tweets_inventory.csv`. Mark the ones you want to upload with `y` in the `ok_to_upload` column, then run:
```bash
python3 scripts/sync_tweets.py
```
