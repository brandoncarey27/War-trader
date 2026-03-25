import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a trading-news classifier for short-term oil, defense, and war-related moves.

Return strict JSON with these keys:
{
  "relevant": true or false,
  "category": "oil" | "defense" | "macro" | "ignore",
  "bias": "bullish" | "bearish" | "neutral",
  "tickers": ["USO", "XLE", "LMT"],
  "confidence": 0-100,
  "reason": "short explanation"
}

Rules:
- Oil bullish: supply disruption, sanctions tightening, pipeline/refinery attacks, shipping disruption, escalation in major producing regions
- Oil bearish: ceasefire, restored production, sanctions relief, de-escalation
- Defense bullish: weapons orders, escalation, new defense spending
- Ignore vague politics with no direct market relevance
- Be conservative
"""

def score_headline(headline: str) -> dict:
    response = client.responses.create(
        model="gpt-5-mini",
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Headline: {headline}"}
        ]
    )

    text = getattr(response, "output_text", "") or ""
    try:
        return json.loads(text)
    except Exception:
        return {
            "relevant": False,
            "category": "ignore",
            "bias": "neutral",
            "tickers": [],
            "confidence": 0,
            "reason": "Could not parse model output"
        }
