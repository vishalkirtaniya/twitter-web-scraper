# Technical Documentation — Twitter Web Scrapping System

## 1. Introduction

This document describes the technical design, architecture, and implementation approach for the **Twitter Market Intelligence System**, built as part of a technical assignment to demonstrate real‑world data engineering, system design, and financial market understanding.

The system collects real‑time discussions from Twitter/X related to the Indian stock market, processes unstructured textual data, and converts it into quantitative trading signals suitable for algorithmic analysis.

Key constraints addressed:

* No paid APIs or official Twitter API usage
* Real‑time, scalable data ingestion
* Memory‑efficient processing and storage
* Production‑ready engineering practices

---

## 2. System Objectives

The primary objectives of the system are:

1. Collect at least **2000 tweets from the last 24 hours** related to Indian stock markets
2. Extract structured information from unstructured social media content
3. Convert textual sentiment into **numerical trading signals**
4. Store processed data efficiently for scalable analysis
5. Demonstrate robustness, scalability, and maintainability

---

## 3. High‑Level Architecture

### End‑to‑End Workflow

```
Scraping → Deduplication → Cleaning → Feature Engineering
        → Signal Generation → Aggregation → Storage → Visualization
```

Each stage is implemented as a **loosely coupled module**, allowing independent scaling, testing, and replacement.

### Design Principles

* Separation of concerns
* Streaming‑friendly pipelines
* Low memory footprint
* Explicit data contracts

---

## 4. Module Architecture & Responsibilities

### 4.1 Scraper Layer (`scraper/`)

**Purpose:** Collect raw tweets from Twitter/X without using paid APIs.

#### `browser_manager.py`

* Manages Selenium WebDriver lifecycle
* Configures headless browser
* Rotates user agents
* Handles browser‑level errors

**Output:**

* Configured Selenium WebDriver instance

---

#### `anti_bot.py`

* Introduces randomized delays
* Simulates human‑like scrolling
* Adds jitter to scroll patterns

**Rationale:**
Reduces bot detection risk while scraping public content.

---

#### `twitter_scraper.py`

* Searches predefined market hashtags
* Scrolls timelines dynamically
* Parses tweet DOM elements

**Extracted Fields:**

* `tweet_id`
* `username`
* `timestamp`
* `content`
* `likes`, `retweets`, `replies`
* `hashtags`, `mentions`

**Design Rule:**
This layer performs **no data cleaning, deduplication, or analysis**.

---

### 4.2 Processing Layer (`processing/`)

**Purpose:** Convert raw tweets into clean, structured data.

#### `deduplicator.py`

* Eliminates duplicate tweets across scrolls and hashtags

**Deduplication Strategy:**

```
hash(tweet_id + normalized_content + timestamp)
```

---

#### `cleaner.py`

* Unicode normalization (Hindi / Hinglish support)
* URL and noise removal
* Whitespace normalization

**Assignment Requirement Covered:**
Handling Indian language Unicode and special characters.

---

#### `feature_engineering.py`

* Converts text into numerical features

**Features Implemented:**

* TF‑IDF vectors
* Market keyword polarity scores
* Engagement‑weighted sentiment features

---

### 4.3 Signal Layer (`signals/`)

**Purpose:** Translate numeric features into actionable trading signals.

#### `sentiment_model.py`

* Computes sentiment score per tweet
* Lightweight and interpretable

**Output Range:**

```
-1.0 (bearish) → +1.0 (bullish)
```

---

#### `signal_generator.py`

* Converts sentiment into discrete signals

**Logic:**

* BUY → sentiment above positive threshold
* SELL → sentiment below negative threshold
* HOLD → neutral sentiment

---

#### `aggregator.py`

* Aggregates signals over rolling time windows
* Computes confidence intervals

**Confidence Formula:**

```
confidence = |mean_sentiment| × log(tweet_volume)
```

This aggregation reduces noise and improves signal reliability.

---

### 4.4 Storage Layer (`storage/`)

**Purpose:** Efficient and scalable persistence.

#### `schema.py`

Defines explicit schemas for processed datasets.

**Core Fields:**

* tweet_id
* timestamp
* content
* sentiment
* signal
* confidence

---

#### `parquet_writer.py`

* Writes chunked Parquet files
* Uses partitioning for fast reads

**Partition Strategy:**

```
/date=YYYY‑MM‑DD/hashtag=banknifty/
```

**Why Parquet:**

* Columnar storage
* Low memory usage
* Optimized for analytics

---

### 4.5 Visualization Layer (`visualization/`)

**Purpose:** Memory‑efficient analytics and plotting.

#### `streaming_plots.py`

* Rolling window plots
* Sampling‑based visualization
* Avoids loading full datasets into memory

---

### 4.6 Utilities (`utils/`)

Shared infrastructure utilities.

* `logger.py` — structured logging
* `config.py` — system configuration and thresholds
* `time_utils.py` — time filtering and session logic

---

## 5. Orchestration (`main.py`)

`main.py` acts as the system orchestrator.

**Responsibilities:**

* Initialize components
* Coordinate data flow between modules
* Handle runtime exceptions

**Pipeline:**

```
Scrape → Clean → Deduplicate → Feature Engineer → Signal → Store
```

No heavy business logic resides here.

---

## 6. Performance & Scalability Considerations

### Concurrency

* Parallel scraping across hashtags
* Background processing pipelines

### Memory Efficiency

* Generator‑based ingestion
* Chunked Parquet writes
* Sampled visualization

### Scalability (10× Data)

* Add more scraper workers
* Increase partitions
* Horizontal processing expansion

---

## 7. Assignment Requirement Mapping

| Requirement          | Implementation                   |
| -------------------- | -------------------------------- |
| No paid APIs         | Selenium‑based scraping          |
| 2000 tweets / 24h    | Scroll‑based ingestion           |
| Deduplication        | `deduplicator.py`                |
| Parquet storage      | `parquet_writer.py`              |
| Unicode handling     | `cleaner.py`                     |
| Quant signals        | `signals/`                       |
| Confidence intervals | `aggregator.py`                  |
| Concurrency          | Threaded scraping                |
| Production readiness | Logging, schemas, modular design |

---

## 8. Limitations & Future Improvements

* Sentiment models can be improved using transformer‑based embeddings
* Real‑time streaming frameworks (Kafka) can replace in‑memory buffers
* Market price correlation can be added for validation

---

## 9. Conclusion

This system demonstrates a production‑oriented approach to real‑time market intelligence using social media data. It balances practical constraints with scalable engineering practices and provides a foundation for sentiment‑driven trading research.
