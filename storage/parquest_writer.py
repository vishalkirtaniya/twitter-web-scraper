import os
import pandas as pd
from utils.logger import get_logger

logger = get_logger(__name__)

def write_parquet(
    tweets: list[dict],
    base_path: str = "data/processed"
):
    if not tweets:
        logger.warning("No tweets to write to Parquet")
        return

    df = pd.DataFrame(tweets)

    # Ensure timestamp column is datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Partition columns
    df["date"] = df["timestamp"].dt.date
    df["hashtag"] = df["hashtags"].apply(
        lambda x: x[0] if isinstance(x, list) and x else "unknown"
    )

    for (date, hashtag), group in df.groupby(["date", "hashtag"]):
        path = os.path.join(
            base_path,
            f"date={date}",
            f"hashtag={hashtag.replace('#', '')}"
        )
        os.makedirs(path, exist_ok=True)

        file_path = os.path.join(path, "tweets.parquet")

        group.drop(columns=["date", "hashtag"]).to_parquet(
            file_path,
            engine="pyarrow",
            index=False
        )

        logger.info(
            f"Wrote {len(group)} tweets → {file_path}"
        )
