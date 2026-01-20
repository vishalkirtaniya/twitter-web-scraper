import random
import time

def human_sleep(min_s=1.5, max_s=4.0):
    time.sleep(random.uniform(min_s, max_s))

def scroll_page(driver, scrolls=5):
    last_height = driver.execute_script("return document.body.scrollHeight")

    for _ in range(scrolls):
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        human_sleep()

        new_height = driver.execute_script(
            "return document.body.scrollHeight"
        )

        if new_height == last_height:
            break

        last_height = new_height
