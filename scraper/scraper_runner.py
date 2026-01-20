from concurrent.futures import ThreadPoolExecutor, as_completed
from scraper.browser_manager import get_browser
from scraper.twitter_scraper import extract_tweets
from utils.logger import get_logger

logger = get_logger(__name__)

def scrape_hashtag(hashtag: str) -> list[dict]:
    """
    Scrape tweets for a single hashtag using its own browser instance.
    """
    driver = get_browser()
    try:
        tweets = extract_tweets(driver, hashtag)
        return tweets
    except Exception as e:
        logger.error(f"Error scraping {hashtag}: {e}")
        return []
    finally:
        driver.quit()

def scrape_all_hashtags(
    hashtags: list[str],
    max_workers: int = 4
) -> list[dict]:
    """
    Concurrently scrape multiple hashtags.
    """
    all_tweets = []

    with ThreadPoolExecutor(
        max_workers=min(max_workers, len(hashtags))
    ) as executor:

        futures = {
            executor.submit(scrape_hashtag, tag): tag
            for tag in hashtags
        }

        for future in as_completed(futures):
            tag = futures[future]
            try:
                tweets = future.result()
                logger.info(f"{len(tweets)} tweets scraped for {tag}")
                all_tweets.extend(tweets)
            except Exception as e:
                logger.error(f"Failed scraping {tag}: {e}")

    return all_tweets
