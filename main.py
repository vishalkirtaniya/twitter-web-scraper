from scraper.scraper_runner import scrape_all_hashtags
from processing.deduplicator import TweetDeduplicator
from processing.cleaner import clean_batch
from utils.logger import get_logger

HASHTAGS = ["#nifty50", "#sensex", "#banknifty", "#intraday"]

logger = get_logger(__name__)

def main():
    logger.info("Starting Twitter Market Intelligence Pipeline")

    # 1. Scrape
    raw_tweets = scrape_all_hashtags(HASHTAGS)
    logger.info(f"Total raw tweets collected: {len(raw_tweets)}")

    # 2. Deduplicate
    deduplicator = TweetDeduplicator()
    unique_tweets = deduplicator.filter_unique(raw_tweets)
    logger.info(f"Unique tweets after deduplication: {len(unique_tweets)}")

    # 3. Clean
    cleaned_tweets = clean_batch(unique_tweets)
    logger.info("Cleaning completed")

    # Next steps:
    # Feature engineering
    # Signal generation
    # Storage

    logger.info("Pipeline Step 3 completed")

if __name__ == "__main__":
    main()
