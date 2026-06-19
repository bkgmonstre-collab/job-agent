import os
import requests

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

# Get latest jobs from Reddit
reddit_response = requests.get(
    "https://www.reddit.com/r/forhire/new.json?limit=5",
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30
)

print("STATUS:", reddit_response.status_code)
print(reddit_response.text[:500])

reddit = reddit_response.json()

posts = reddit["data"]["children"][:5]

for post in posts:
    title = post["data"]["title"]
    text = post["data"].get("selftext", "")

    prompt = f"""
Score this freelance opportunity from 1-10.
Return ONLY a number.

Title: {title}

Description:
{text[:1000]}
"""

    gemini = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}",
        json={
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }
    ).json()

    score = gemini["candidates"][0]["content"]["parts"][0]["text"]

    if int(score.strip()) >= 7:
        message = f"""
🔥 New Opportunity

Title:
{title}

Score:
{score}/10
"""

        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message
            }
        )
