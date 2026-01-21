# visualization/streaming_plots.py

import pandas as pd
import matplotlib.pyplot as plt
from utils.logger import get_logger

logger = get_logger(__name__)


def plot_rolling_sentiment(
    tweets: list[dict],
    window: int = 50,
    sample_size: int = 2000
):
    """
    Memory-efficient rolling sentiment plot.
    Uses sampling to avoid large memory usage.
    """

    if not tweets:
        logger.warning("No tweets available for visualization")
        return

    # Convert to DataFrame
    df = pd.DataFrame(tweets)

    # Ensure required columns exist
    if "timestamp" not in df or "sentiment" not in df:
        logger.error("Required columns missing for visualization")
        return

    # Sort by time
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    # Sample if dataset is large
    if len(df) > sample_size:
        df = df.sample(sample_size, random_state=42)
        df = df.sort_values("timestamp")
        logger.info(f"Sampled {sample_size} tweets for plotting")

    # Rolling sentiment
    df["rolling_sentiment"] = df["sentiment"].rolling(
        window=window,
        min_periods=1
    ).mean()

    # Plot
    plt.figure(figsize=(10, 4))
    plt.plot(
        df["timestamp"],
        df["rolling_sentiment"],
        label="Rolling Sentiment"
    )

    plt.axhline(0, linestyle="--")
    plt.title("Rolling Market Sentiment (Twitter)")
    plt.xlabel("Time")
    plt.ylabel("Sentiment")
    plt.legend()
    plt.tight_layout()

    plt.show()

    logger.info("Sentiment visualization generated")
