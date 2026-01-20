import math
from collections import defaultdict

class SignalAggregator:
    def aggregate(self, tweets: list[dict]) -> dict:
        if not tweets:
            return {
                "signal": "HOLD",
                "confidence": 0.0
            }

        sentiments = [t["sentiment"] for t in tweets]
        mean_sentiment = sum(sentiments) / len(sentiments)

        confidence = abs(mean_sentiment) * math.log(len(tweets) + 1)

        if mean_sentiment > 0.2:
            signal = "BUY"
        elif mean_sentiment < -0.2:
            signal = "SELL"
        else:
            signal = "HOLD"

        return {
            "signal": signal,
            "mean_sentiment": mean_sentiment,
            "confidence": round(confidence, 3),
            "tweet_volume": len(tweets)
        }
