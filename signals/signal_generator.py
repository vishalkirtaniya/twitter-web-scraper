class SignalGenerator:
    def __init__(self, buy_threshold=0.2, sell_threshold=-0.2):
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold

    def generate_signal(self, sentiment: float) -> str:
        if sentiment >= self.buy_threshold:
            return "BUY"
        elif sentiment <= self.sell_threshold:
            return "SELL"
        return "HOLD"

    def apply(self, tweets: list[dict]) -> list[dict]:
        for tweet in tweets:
            tweet["signal"] = self.generate_signal(
                tweet.get("sentiment", 0.0)
            )
        return tweets
