# Twitter Market Intelligence System

## Overview

This project implements an end-to-end data collection, processing, and analysis pipeline to generate **real-time market intelligence for the Indian stock market** using public Twitter/X discussions.

The system is designed to be **robust, scalable, and production-oriented**, handling real-world constraints such as rate limits, bot protection, and restricted access, while still producing reproducible analytical results.

---

## Key Features

* **Automated Data Collection**

  * Scrapes public Twitter/X discussions related to Indian markets
  * Focus keywords: `nifty50`, `sensex`, `banknifty`, `intraday`
  * Uses Selenium with anti-bot techniques
  * Attempts live scraping via public Twitter mirrors (Nitter)

* **Graceful Failure Handling**

  * Explicit detection of access restrictions (Cloudflare / bot protection)
  * Automatic fallback to cached sample data
  * Ensures pipeline reproducibility even when live scraping is blocked

* **Data Processing**

  * Deduplication of tweets
  * Unicode-safe text cleaning (supports Indian language content)
  * Feature engineering for market relevance

* **Signal Generation**

  * Sentiment analysis of tweets
  * Per-tweet BUY / SELL / HOLD signals
  * Aggregated market-level signal with confidence score

* **Efficient Storage**

  * Partitioned Parquet storage (date + hashtag)
  * Optimized for large-scale data processing

* **Visualization**

  * Memory-efficient rolling sentiment visualization
  * Sampling-based plotting for large datasets

---

## Project Structure

```
twitter-market-intelligence/
├── scraper/                # Selenium scraping logic
├── processing/             # Cleaning, deduplication, features
├── signals/                # Sentiment & trading signals
├── storage/                # Parquet writers & schema
├── visualization/          # Low-memory plots
├── utils/                  # Logging, config utilities
├── data/
│   ├── raw/
│   ├── processed/
│   ├── signals/
│   └── sample_tweets.json
├── main.py                 # Pipeline orchestrator
├── requirements.txt
├── README.md
└── TECHNICAL_DOC.md
```

---

## System Workflow

```
Scraping
   ↓
Deduplication
   ↓
Cleaning & Normalization
   ↓
Feature Engineering
   ↓
Sentiment Analysis
   ↓
Signal Generation
   ↓
Market Signal Aggregation
   ↓
Parquet Storage + Visualization
```

---

## Data Collection Strategy

### Live Scraping

* Uses Selenium to scrape public Twitter mirrors (Nitter)
* No paid APIs or official Twitter APIs are used
* Anti-bot measures:

  * Randomized delays
  * Controlled scrolling
  * Restriction detection via page content inspection

### Graceful Fallback

Twitter/X frequently restricts unauthenticated scraping. When:

* No tweets are returned, or
* Bot protection / Cloudflare pages are detected

The system:

1. Logs the restriction explicitly
2. Automatically loads `data/sample_tweets.json`
3. Continues downstream processing without failure

This design ensures **reliability and reproducibility**.

---

## Signal Methodology (High-Level)

* Tweets are converted into numerical representations using:

  * Keyword relevance scores
  * Sentiment polarity
* Per-tweet signals are generated:

  * BUY / SELL / HOLD
* Market-level signal is computed by:

  * Aggregating sentiment
  * Weighting by tweet volume
  * Producing a confidence score

> Signals are intended for **market intelligence and research**, not direct automated trading.

---

## Storage Design

* Data is stored in **Parquet format** using PyArrow
* Partitioning:

  * `date=YYYY-MM-DD`
  * `hashtag=<topic>`

Example:

```
data/processed/
└── date=2026-01-21/
    ├── hashtag=nifty50/
    │   └── tweets.parquet
    ├── hashtag=banknifty/
    │   └── tweets.parquet
```

This structure supports scalable analytics and fast reads.

---

## Visualization

* Rolling average sentiment over time
* Sampling-based plotting to reduce memory usage
* Designed to work with large datasets

---

## Setup Instructions

### 1. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the pipeline

```bash
python main.py
```

---

## Requirements

* Python 3.10+
* Selenium
* Pandas
* PyArrow
* Scikit-learn
* Matplotlib

---

## Notes on Real-World Constraints

* Twitter/X aggressively restricts scraping
* Public mirrors may be rate-limited or blocked
* This system is intentionally designed to **degrade gracefully**

Such constraints are common in real-world data engineering systems, and handling them robustly is part of the design.

---

## Author

**Vishal Aditya Kirtaniya**

This project was built as part of a technical assignment to demonstrate:

* Python proficiency
* Market domain understanding
* Robust, production-ready engineering practices