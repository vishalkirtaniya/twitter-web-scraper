import re
import unicodedata

URL_PATTERN = re.compile(r"http[s]?://\\S+")

def clean_text(text: str) -> str:
    if not text:
        return ""

    # Normalize Unicode (Hindi / Hinglish safe)
    text = unicodedata.normalize("NFKC", text)

    # Remove URLs
    text = URL_PATTERN.sub("", text)

    # Normalize whitespace
    text = re.sub(r"\\s+", " ", text)

    return text.strip()

def clean_tweet(tweet: dict) -> dict:
    tweet["content"] = clean_text(tweet.get("content", ""))
    return tweet

def clean_batch(tweets: list[dict]) -> list[dict]:
    return [clean_tweet(t) for t in tweets]
