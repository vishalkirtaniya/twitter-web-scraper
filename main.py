from scraper.scraper_runner import scrape_all_hashtags
from processing.deduplicator import TweetDeduplicator
from processing.cleaner import clean_batch
from processing.feature_engineering import FeatureEngineer
from signals.sentiment_model import SentimentModel
from signals.signal_generator import SignalGenerator
from signals.aggregator import SignalAggregator
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

    # 4.1 Feature Engineering
    feature_engineer = FeatureEngineer()
    feature_engineer.add_features(cleaned_tweets)
    logger.info("Feature engineering completed")

    # 4.2 Sentimental Computation
    sentiment_model = SentimentModel()
    sentiment_model.apply(cleaned_tweets)
    logger.info("Sentiment scores computed")

    # 4.3 Per-Tweet Signal Generation
    signal_generator = SignalGenerator()
    signal_generator.apply(cleaned_tweets)
    logger.info("Per-tweet trading signals generated")

    # 4.3 Agregte Market-Level Signal
    aggregator = SignalAggregator()
    market_signal = aggregator.aggregate(cleaned_tweets)

    logger.info(
        f"Market Signal: {market_signal['signal']} | "
        f"Confidence: {market_signal['confidence']} | "
        f"Tweet Volume: {market_signal['tweet_volume']}"
    )

    # NEXT STEPS:
    # STEP 5: Parquet storage
    # STEP 6: Visualization

    logger.info("Pipeline Step 3 completed")

if __name__ == "__main__":
    main()
