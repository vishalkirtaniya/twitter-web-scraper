from scraper.browser_manager import get_browser
from scraper.twitter_scraper import extract_tweets

driver = get_browser()

all_tweets = []
for tag in ["#nifty50", "#sensex", "#banknifty", "#intraday"]:
    all_tweets.extend(extract_tweets(driver, tag))

driver.quit()
