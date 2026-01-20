import hashlib

class TweetDeduplicator:
    def __init__(self):
        self._seen_hashes = set()

    def _hash_tweet(self, tweet: dict) -> str:
        raw = f"{tweet['tweet_id']}|{tweet['content']}|{tweet['timestamp']}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def is_duplicate(self, tweet: dict) -> bool:
        h = self._hash_tweet(tweet)
        if h in self._seen_hashes:
            return True
        self._seen_hashes.add(h)
        return False

    def filter_unique(self, tweets: list[dict]) -> list[dict]:
        unique = []
        for tweet in tweets:
            if not self.is_duplicate(tweet):
                unique.append(tweet)
        return unique
