# signals/aggregator.py

import math

class SignalAggregator:
    def aggregate(self, tweets: list[dict]) -> dict:
        tweet_volume = len(tweets)

        if tweet_volume == 0:
            return {
                "signal": "HOLD",
                "mean_sentiment": 0.0,
                "confidence": 0.0,
                "tweet_volume": 0
            }

        sentiments = [t["sentiment"] for t in tweets]
        mean_sentiment = sum(sentiments) / tweet_volume

        confidence = abs(mean_sentiment) * math.log(tweet_volume + 1)

        if mean_sentiment > 0.2:
            signal = "BUY"
        elif mean_sentiment < -0.2:
            signal = "SELL"
        else:
            signal = "HOLD"

        return {
            "signal": signal,
            "mean_sentiment": round(mean_sentiment, 4),
            "confidence": round(confidence, 4),
            "tweet_volume": tweet_volume
        }
