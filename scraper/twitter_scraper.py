from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from scraper.anti_bot import scroll_page, human_sleep
from utils.logger import get_logger

logger = get_logger(__name__)

SEARCH_URL = "https://twitter.com/search?q={query}&src=typed_query&f=live"

def parse_int(text):
    if not text:
        return 0
    text = text.replace(",", "")
    if "K" in text:
        return int(float(text.replace("K", "")) * 1000)
    return int(text)

def extract_tweets(driver, hashtag: str, max_scrolls=20):
    tweets = []
    cutoff_time = datetime.utcnow() - timedelta(hours=24)

    url = SEARCH_URL.format(query=hashtag)
    driver.get(url)
    human_sleep(3, 6)

    scroll_page(driver, scrolls=max_scrolls)

    tweet_elements = driver.find_elements(By.XPATH, "//article")

    for tweet in tweet_elements:
        try:
            content = tweet.text
            if not content:
                continue

            timestamp_el = tweet.find_element(By.TAG_NAME, "time")
            timestamp = datetime.fromisoformat(
                timestamp_el.get_attribute("datetime").replace("Z", "")
            )

            if timestamp < cutoff_time:
                continue

            username = tweet.find_element(
                By.XPATH, ".//span[contains(text(),'@')]"
            ).text

            metrics = tweet.find_elements(
                By.XPATH, ".//div[@data-testid='like' or @data-testid='retweet' or @data-testid='reply']//span"
            )

            likes = parse_int(metrics[0].text) if len(metrics) > 0 else 0
            retweets = parse_int(metrics[1].text) if len(metrics) > 1 else 0
            replies = parse_int(metrics[2].text) if len(metrics) > 2 else 0

            tweets.append({
                "tweet_id": f"{username}_{timestamp.timestamp()}",
                "username": username,
                "timestamp": timestamp,
                "content": content,
                "likes": likes,
                "retweets": retweets,
                "replies": replies,
                "hashtags": [hashtag],
                "mentions": [w for w in content.split() if w.startswith("@")]
            })

        except Exception as e:
            logger.warning(f"Tweet parse failed: {e}")
            continue

    logger.info(f"{len(tweets)} tweets scraped for {hashtag}")
    return tweets
