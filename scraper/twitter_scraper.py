from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from scraper.anti_bot import scroll_page, human_sleep
from utils.logger import get_logger

logger = get_logger(__name__)

# Nitter search URL
SEARCH_URL = "https://nitter.net/search?f=tweets&q={query}"

def extract_tweets(driver, hashtag: str, max_scrolls: int = 15) -> list[dict]:
    tweets = []
    cutoff_time = datetime.utcnow() - timedelta(hours=24)

    # Remove '#' for Nitter query
    query = hashtag.replace("#", "")
    url = SEARCH_URL.format(query=query)

    logger.info(f"Fetching URL: {url}")
    driver.get(url)
    human_sleep(3, 5)

    # Scroll page to load more tweets
    scroll_page(driver, scrolls=max_scrolls)

    # Each tweet is a timeline-item
    tweet_elements = driver.find_elements(
        By.CSS_SELECTOR, ".timeline-item"
    )

    for tweet in tweet_elements:
        try:
            # Content
            content_el = tweet.find_element(
                By.CSS_SELECTOR, ".tweet-content"
            )
            content = content_el.text.strip()

            if not content or len(content.split()) < 4:
                continue

            # Username
            username = tweet.find_element(
                By.CSS_SELECTOR, ".username"
            ).text.strip()

            # Timestamp
            time_el = tweet.find_element(By.TAG_NAME, "time")
            timestamp_raw = time_el.get_attribute("datetime")

            timestamp = datetime.fromisoformat(
                timestamp_raw.replace("Z", "")
            )

            # Filter last 24 hours
            if timestamp < cutoff_time:
                continue

            tweets.append({
                "tweet_id": f"{username}_{int(timestamp.timestamp())}",
                "username": username,
                "timestamp": timestamp,
                "content": content,
                "likes": 0,       # Nitter hides engagement
                "retweets": 0,
                "replies": 0,
                "hashtags": [hashtag],
                "mentions": [
                    word for word in content.split()
                    if word.startswith("@")
                ]
            })

        except Exception as e:
            logger.debug(f"Tweet parse skipped: {e}")
            continue

    logger.info(f"{len(tweets)} tweets scraped for {hashtag}")
    return tweets
