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
from multiprocessing import Process, Queue
from gs_links import GS_LINKS, ABBR_TO_NAME
from get_email import get_email
from supabase_client import insert_professor
from pprint import pprint

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

def scrape_main_page(gs_url_queue, profile_queue):
    """
    Consumes Google Scholar URLs from gs_url_queue, scrapes <h3 class='gs_ai_name'> elements, sends (name, href) to profile_queue.
    """
    while True:
        school, url = gs_url_queue.get()
        if url is None:
            break
        results = {}
        proxy = get_random_proxy()
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run in headless mode
        if proxy:
            options.add_argument(f'--proxy-server={proxy}')
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        try:
            while True:
                time.sleep(random.uniform(2, 4))
                h3_elements = driver.find_elements(By.CSS_SELECTOR, 'h3.gs_ai_name')
                if not h3_elements:
                    break
                for h3 in h3_elements:
                    a_tag = h3.find_element(By.TAG_NAME, 'a')
                    name = a_tag.text.strip()
                    href = a_tag.get_attribute('href')
                    if name and href:
                        results[name] = href
                        print(f"Found {name} at {href}")
                        print(f"Putting {name} at {href} in profile queue")
                        profile_queue.put((school, name, f"{href}&view_op=list_works&sortby=pubdate"))
                try:
                    next_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Next"]')
                    if not next_button.is_enabled():
                        break
                    time.sleep(random.uniform(1, 2))
                    next_button.click()
                except Exception:
                    break
        finally:
            driver.quit()

    # Signal end of queue
    profile_queue.put(None)

def scrape_profile_page(profile_queue, publication_queue, postgres_insert_queue):
    """
    Consumes (school, name, href) from profile_queue, processes profile, sends publication data to publication_queue.
    Only processes professors with publications in the current year.
    """
    while True:
        item = profile_queue.get()
        if item is None:
            break
        school, name, href = item
        print(f"[Profile] Processing {name} at {href}")
        
        try:
            # Set up WebDriver for the profile page
            proxy = get_random_proxy()
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')  # Run in headless mode
            if proxy:
                options.add_argument(f'--proxy-server={proxy}')
            driver = webdriver.Chrome(options=options)
            driver.get(href)
            
            # Wait for page to load
            time.sleep(random.uniform(1, 3))
            
            # Extract publication dates
            date_elements = driver.find_elements(By.CSS_SELECTOR, 'span.gsc_a_h.gsc_a_hc.gs_ibl')
            dates = [elem.text.strip() for elem in date_elements]
            
            # Extract publication titles and URLs
            title_elements = driver.find_elements(By.CSS_SELECTOR, 'a.gsc_a_at')
            titles = [elem.text.strip() for elem in title_elements]
            urls = [elem.get_attribute('href') for elem in title_elements]
            
            # Get current year
            current_year = time.strftime("%Y")  # Returns "2025" in 2025
            
            # Check if we have publications and if the first one is from current year
            if dates and titles and urls and len(dates) > 0 and len(titles) > 0:
                # Some dates might be empty or non-numeric, so handle those cases
                first_date = dates[0]
                if first_date and first_date.isdigit() and first_date == current_year:
                    print(f"[Profile] {name} has publications from {current_year}, processing...")

                    if not valid_researcher(name, ABBR_TO_NAME[school]):
                        print(f"[Profile] {name} is not a valid researcher, skipping.")
                        continue

                    print(f"[Profile] {name} is a valid researcher, getting email...")
                    
                    email_found, email = get_email(name, ABBR_TO_NAME[school])
                    if email_found:
                        print(f"[Profile] {name} has email {email}")
                    else:
                        print(f"[Profile] {name} does not have email")
                        continue

                    postgres_insert_queue.put((ABBR_TO_NAME[school], name, email, href))
                    
                    # Zip all data together
                    publications = list(zip(titles, urls, dates))
                    
                    # Send to publication queue
                    publication_queue.put({(school, name): [(title, url, date) for title, url, date in publications if date == current_year]})
                else:
                    print(f"[Profile] {name} has no publications from {current_year}, skipping.")
            else:
                print(f"[Profile] Could not find publication data for {name}, skipping.")
                
        except Exception as e:
            print(f"[Profile] Error processing {name}: {str(e)}")
        finally:
            driver.quit()
            
    # Signal end of queue
    publication_queue.put(None)
    postgres_insert_queue.put(None)

def postgres_insert(postgres_insert_queue):
    """
    Inserts the publication data into the PostgreSQL database.
    """
    while True:
        item = postgres_insert_queue.get()
        if item is None:
            break
        school, name, email, href = item
        print(f"[Postgres] Inserting professor {name} into DB")
        
        insert_professor(school, name, email, href)

        print(f"[Postgres] Professor {name} inserted into DB")

def scrape_publications_page(publication_queue):
    """
    Consumes (school, name, title, url, date) from publication_queue, processes publications, writes to DB.
    """
    while True:
        item = publication_queue.get()
        if item is None:
            break
        
        print(f"[Publications] Processing:")
        pprint(item)

if __name__ == "__main__":
    # main_url = GS_LINKS["umd"]
    gs_url_queue = Queue()
    profile_queue = Queue()
    publication_queue = Queue()
    postgres_insert_queue = Queue()

    # Example: add multiple URLs to the queue
    for school in GS_LINKS:
        gs_url_queue.put((school, GS_LINKS[school]))
    gs_url_queue.put(None)  # Sentinel value

    p_main = Process(target=scrape_main_page, args=(gs_url_queue, profile_queue))
    p_profile = Process(target=scrape_profile_page, args=(profile_queue, publication_queue, postgres_insert_queue))
    p_publications = Process(target=scrape_publications_page, args=(publication_queue,))
    p_postgres_insert = Process(target=postgres_insert, args=(postgres_insert_queue,))

    p_main.start()
    p_profile.start()
    p_publications.start()
    p_postgres_insert.start()

    p_main.join()
    p_profile.join()
    p_publications.join()
    p_postgres_insert.join()
