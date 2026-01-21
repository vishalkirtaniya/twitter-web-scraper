from typing import TypedDict
from datetime import datetime

class TweetSchema(TypedDict):
    tweet_id: str
    username: str
    timestamp: datetime
    content: str
    likes: int
    retweets: int
    replies: int
    engagement: int
    keyword_score: int
    sentiment: float
    signal: str
    hashtags: list[str]
