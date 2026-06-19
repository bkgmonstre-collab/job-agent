import os
import requests

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

jobs = [
    {
        "title": "Python Developer Needed for SaaS Project",
        "description": "Need an experienced Python developer to build API integrations and automation."
    }
]

for job in jobs:
    title = job["title"]
    text = job["description"]

    prompt = f"""
Score this freelance opportunity from 1-10.
Return ONLY a number.

Title: {title}

Description:
{text}
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

    print("Gemini Response:")
    print(gemini)

    if "candidates" not in gemini:
        raise Exception(f"Gemini Error: {gemini}")

    score = gemini["candidates"][0]["content"]["parts"][0]["text"].strip()

    if int(score) >= 7:
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

print("Agent finished successfully.")
