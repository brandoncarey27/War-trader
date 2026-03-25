from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/webhook")
async def webhook(req: Request):
    data = await req.json()

    ticker = data.get("ticker")
    price = data.get("price")
    event = data.get("event")

    message = f"🚨 {ticker} ALERT\nEvent: {event}\nPrice: {price}"

    if DISCORD_WEBHOOK_URL:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": message})

    return {"ok": True}
