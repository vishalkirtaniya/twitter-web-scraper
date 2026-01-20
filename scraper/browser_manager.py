from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import random

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (X11; Linux x86_64)"
]

def get_browser(headless: bool = True) -> webdriver.Chrome:
    options = Options()

    if headless:
        options.add_argument("--headless=new")

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    user_agent = random.choice(USER_AGENTS)
    options.add_argument(f"user-agent={user_agent}")

    service = Service()
    driver = webdriver.Chrome(service=service, options=options)

    driver.set_window_size(1400, 900)
    return driver
