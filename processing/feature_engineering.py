from sklearn.feature_extraction.text import TfidfVectorizer

# Market-specific keywords
BULLISH_KEYWORDS = [
    "buy", "bullish", "breakout", "strong", "uptrend",
    "long", "support", "accumulate", "positive"
]

BEARISH_KEYWORDS = [
    "sell", "bearish", "breakdown", "weak", "downtrend",
    "short", "resistance", "negative"
]

class FeatureEngineer:
    def __init__(self, max_features: int = 5000):
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=(1, 2),
            stop_words="english"
        )

    def fit_transform(self, tweets: list[dict]):
        texts = [t["content"] for t in tweets]
        tfidf_matrix = self.vectorizer.fit_transform(texts)
        return tfidf_matrix

    def keyword_score(self, text: str) -> int:
        text_lower = text.lower()
        bullish = sum(word in text_lower for word in BULLISH_KEYWORDS)
        bearish = sum(word in text_lower for word in BEARISH_KEYWORDS)
        return bullish - bearish

    def add_features(self, tweets: list[dict]) -> list[dict]:
        for tweet in tweets:
            tweet["keyword_score"] = self.keyword_score(tweet["content"])
            tweet["engagement"] = (
                tweet.get("likes", 0) + tweet.get("retweets", 0)
            )
        return tweets
