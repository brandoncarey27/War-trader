import os
import requests
from app.ai_news import score_headline

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# swap this later for Benzinga or your preferred feed
HEADLINES_TO_TEST = [
    "Missile strike disrupts oil shipping routes in the Middle East",
    "Ceasefire talks reduce fears of broader regional conflict",
    "NATO members discuss increased defense procurement plans",
    "Oil prices steady as production resumes at major facility"
]

def send_discord(msg: str):
    if DISCORD_WEBHOOK_URL:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": msg}, timeout=10)

def main():
    for headline in HEADLINES_TO_TEST:
        result = score_headline(headline)

        if not result.get("relevant"):
            continue

        msg = (
            f"🧠 AI HEADLINE ALERT\n"
            f"Headline: {headline}\n"
            f"Category: {result.get('category')}\n"
            f"Bias: {result.get('bias')}\n"
            f"Tickers: {', '.join(result.get('tickers', []))}\n"
            f"Confidence: {result.get('confidence')}\n"
            f"Reason: {result.get('reason')}"
        )
        send_discord(msg)

if __name__ == "__main__":
    main()
