import math

class SentimentModel:
    def compute_sentiment(self, tweet: dict) -> float:
        keyword_score = tweet.get("keyword_score", 0)
        engagement = tweet.get("engagement", 0)

        sentiment = keyword_score * math.log1p(engagement + 1)

        # Normalize to [-1, 1] range (soft normalization)
        if sentiment > 0:
            return min(sentiment / 5, 1.0)
        elif sentiment < 0:
            return max(sentiment / 5, -1.0)
        return 0.0

    def apply(self, tweets: list[dict]) -> list[dict]:
        for tweet in tweets:
            tweet["sentiment"] = self.compute_sentiment(tweet)
        return tweets
