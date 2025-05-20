from bs4 import BeautifulSoup
from verification import valid_researcher
import selenium
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

MAIN_URL = "https://scholar.google.com"

# Placeholder for proxy rotation
PROXIES = [
    # 'http://proxy1:port',
    # 'http://proxy2:port',
]

def get_random_proxy():
    if not PROXIES:
        return None
    return random.choice(PROXIES)

def scrape_main_page(url):
    """
    Scrape all <h3 class='gs_ai_name'> elements, extract <a> text and href, and paginate using Selenium.
    Returns: dict {name: href}
    """
    results = {}
    proxy = get_random_proxy()
    options = webdriver.ChromeOptions()
    if proxy:
        options.add_argument(f'--proxy-server={proxy}')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    try:
        while True:
            # Wait for h3 elements to load
            time.sleep(random.uniform(2, 4))  # Random delay to avoid detection
            h3_elements = driver.find_elements(By.CSS_SELECTOR, 'h3.gs_ai_name')
            if not h3_elements:
                break
            for h3 in h3_elements:
                a_tag = h3.find_element(By.TAG_NAME, 'a')
                name = a_tag.text.strip()
                href = a_tag.get_attribute('href')
                if name and href:
                    results[name] = href
            # Try to find and click the Next button
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Next"]')
                if not next_button.is_enabled():
                    break
                time.sleep(random.uniform(1, 2))  # Delay before clicking next
                next_button.click()
                # Optionally rotate proxy here for each page
                # driver.quit()
                # proxy = get_random_proxy()
                # options = webdriver.ChromeOptions()
                # if proxy:
                #     options.add_argument(f'--proxy-server={proxy}')
                # driver = webdriver.Chrome(options=options)
                # driver.get(url)
            except Exception:
                break  # No more Next button
    finally:
        driver.quit()
    return results

def scrape_profile_page(url):
    pass

def scrape_publications_page(url):
    pass

