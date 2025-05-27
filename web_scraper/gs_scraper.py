from bs4 import BeautifulSoup
from verification import valid_researcher
import selenium
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
import time
import random
from multiprocessing import Process, Queue
from gs_links import GS_LINKS, ABBR_TO_NAME, NAME_TO_ABBR
from get_email import get_email
from supabase_client import insert_professor, insert_embedding_text
from pinecone_client import upsert_professor
from sentence_transformers import SentenceTransformer
from pprint import pprint


MAIN_URL = "https://scholar.google.com"
model = SentenceTransformer("all-MiniLM-L6-v2")

VECTOR_BATCH_SIZE = 10

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
        item = gs_url_queue.get()
        if item is None:
            break
        school, url = item
        results = {}
        
        # Add delay before processing each school
        delay = random.uniform(30, 180)  # 30 seconds to 3 minutes
        print(f"[Main]: Waiting {delay:.1f} seconds before processing {school}")
        time.sleep(delay)
        
        # Protected WebDriver setup
        driver = None
        try:
            proxy = get_random_proxy()
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')  # Run in headless mode
            if proxy:
                options.add_argument(f'--proxy-server={proxy}')
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            print(f"[Main]: Set up web driver for {school}")
        except WebDriverException as e:
            print(f"[Main]: Failed to set up WebDriver for {school}: {str(e)}")
            if driver:
                driver.quit()
            continue
        except Exception as e:
            print(f"[Main]: Unexpected error setting up WebDriver for {school}: {str(e)}")
            if driver:
                driver.quit()
            continue
        
        try:
            while True:
                # Protected page load wait
                try:
                    # Add delay between page requests
                    page_delay = random.uniform(30, 120)  # 30 seconds to 2 minutes for pages
                    print(f"[Main]: Waiting {page_delay:.1f} seconds before loading page")
                    time.sleep(page_delay)
                    
                    h3_elements = driver.find_elements(By.CSS_SELECTOR, 'h3.gs_ai_name')
                except WebDriverException as e:
                    print(f"[Main]: Error finding professor elements for {school}: {str(e)}")
                    break
                except Exception as e:
                    print(f"[Main]: Unexpected error finding professor elements for {school}: {str(e)}")
                    break

                # if no h3_elements, break, usually means captcha
                if len(h3_elements) == 0:
                    print(f"[Main]: No professor elements found for {school} - possible CAPTCHA or blocking")
                    break
                
                # Protected professor data extraction
                for h3 in h3_elements:
                    try:
                        a_tag = h3.find_element(By.TAG_NAME, 'a')
                        name = a_tag.text.strip()
                        href = a_tag.get_attribute('href')
                        
                        if name and href:
                            results[name] = href
                            print(f"[Main] Found {name} at {href}")
                            print(f"[Main] Putting {name} at {href} in profile queue")
                            profile_queue.put((school, name, f"{href}&view_op=list_works&sortby=pubdate"))
                            
                            # Add small delay between processing professors on same page
                            prof_delay = random.uniform(5, 15)  # 5-15 seconds between professors
                            print(f"[Main]: Waiting {prof_delay:.1f} seconds before next professor")
                            time.sleep(prof_delay)
                        else:
                            print(f"[Main]: Skipping professor with missing name or href")
                            
                    except NoSuchElementException:
                        print(f"[Main]: Skipping malformed professor entry - no link found")
                        continue
                    except Exception as e:
                        print(f"[Main]: Error processing professor element: {str(e)}")
                        continue
                
                # Protected pagination
                try:
                    next_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Next"]')
                    if not next_button.is_enabled():
                        print(f"[Main]: No more pages for {school}")
                        break
                    
                    # Add delay before clicking next page
                    next_delay = random.uniform(45, 180)  # 45 seconds to 3 minutes before next page
                    print(f"[Main]: Waiting {next_delay:.1f} seconds before next page")
                    time.sleep(next_delay)
                    
                    next_button.click()
                    print(f"[Main]: Clicked next page for {school}")
                except NoSuchElementException:
                    print(f"[Main]: No next button found for {school} - end of results")
                    break
                except WebDriverException as e:
                    print(f"[Main]: Error clicking next button for {school}: {str(e)}")
                    break
                except Exception as e:
                    print(f"[Main]: Unexpected error with pagination for {school}: {str(e)}")
                    break
                    
        except Exception as e:
            print(f"[Main]: Critical error processing {school}: {str(e)}")
        finally:
            if driver:
                try:
                    driver.quit()
                except Exception as e:
                    print(f"[Main]: Error closing driver for {school}: {str(e)}")

    # Signal end of queue
    profile_queue.put(None)
    print(f"[Main]: Finished processing all schools")

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
        
        # Add delay before processing each professor
        delay = random.uniform(30, 180)  # 30 seconds to 3 minutes
        print(f"[Profile]: Waiting {delay:.1f} seconds before processing {name}")
        time.sleep(delay)
        
        print(f"[Profile] Processing {name} at {href}")
        
        # Protected WebDriver setup
        driver = None
        try:
            proxy = get_random_proxy()
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')  # Run in headless mode
            if proxy:
                options.add_argument(f'--proxy-server={proxy}')
            driver = webdriver.Chrome(options=options)
            driver.get(href)
        except WebDriverException as e:
            print(f"[Profile] Failed to set up WebDriver for {name}: {str(e)}")
            if driver:
                driver.quit()
            continue
        except Exception as e:
            print(f"[Profile] Unexpected error setting up WebDriver for {name}: {str(e)}")
            if driver:
                driver.quit()
            continue
        
        try:
            # Wait for page to load with additional delay
            load_delay = random.uniform(10, 30)  # 10-30 seconds for page load
            print(f"[Profile]: Waiting {load_delay:.1f} seconds for page to load")
            time.sleep(load_delay)
            
            # Protected publication date extraction
            try:
                date_elements = driver.find_elements(By.CSS_SELECTOR, 'span.gsc_a_h.gsc_a_hc.gs_ibl')
                dates = [elem.text.strip() for elem in date_elements if elem.text.strip()]
            except WebDriverException as e:
                print(f"[Profile] Error finding publication dates for {name}: {str(e)}")
                continue
            except Exception as e:
                print(f"[Profile] Unexpected error finding publication dates for {name}: {str(e)}")
                continue

            if len(date_elements) == 0:
                print(f"[Profile] {name} has no publications, skipping.")
                continue
            
            # Protected publication title and URL extraction
            try:
                title_elements = driver.find_elements(By.CSS_SELECTOR, 'a.gsc_a_at')
                titles = [elem.text.strip() for elem in title_elements if elem.text.strip()]
                urls = [elem.get_attribute('href') for elem in title_elements if elem.get_attribute('href')]
            except WebDriverException as e:
                print(f"[Profile] Error finding publication titles/URLs for {name}: {str(e)}")
                continue
            except Exception as e:
                print(f"[Profile] Unexpected error finding publication titles/URLs for {name}: {str(e)}")
                continue
            
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
                    
                    # Protected email lookup
                    try:
                        email_found, email = get_email(name, ABBR_TO_NAME[school])
                        if email_found:
                            print(f"[Profile] {name} has email {email}")
                        else:
                            print(f"[Profile] {name} does not have email")
                            continue
                    except Exception as e:
                        print(f"[Profile] Error getting email for {name}: {str(e)}")
                        continue

                    # Protected database insertion
                    try:
                        postgres_insert_queue.put(("basic_info", ABBR_TO_NAME[school], name, email, href))
                    except Exception as e:
                        print(f"[Profile] Error queuing basic info for {name}: {str(e)}")
                        continue
                    
                    # Protected publication data preparation
                    try:
                        publications = list(zip(titles, urls, dates))
                        current_year_publications = [(title, url, date) for title, url, date in publications if date == current_year]
                        
                        if current_year_publications:
                            publication_queue.put([(school, name), current_year_publications])
                            print(f"[Profile] Queued {len(current_year_publications)} publications for {name}")
                        else:
                            print(f"[Profile] No current year publications found for {name}")
                    except Exception as e:
                        print(f"[Profile] Error preparing publication data for {name}: {str(e)}")
                        continue
                else:
                    print(f"[Profile] {name} has no publications from {current_year}, skipping.")
            else:
                print(f"[Profile] Could not find publication data for {name}, skipping.")
                
        except Exception as e:
            print(f"[Profile] Critical error processing {name}: {str(e)}")
        finally:
            if driver:
                try:
                    driver.quit()
                except Exception as e:
                    print(f"[Profile] Error closing driver for {name}: {str(e)}")
            
    # Signal end of queue
    publication_queue.put(None)
    print("[Profile] Finished processing all professors")

def scrape_publications_page(publication_queue, postgres_insert_queue):
    """
    Consumes (school, name, title, url, date) from publication_queue, processes publications, writes to DB.
    """
    while True:
        item = publication_queue.get()
        if item is None:
            break
    
        try:
            school, name, publications = item[0][0], item[0][1], item[1]
        except (IndexError, TypeError) as e:
            print(f"[Publications] Error unpacking publication data: {str(e)}")
            continue
        except Exception as e:
            print(f"[Publications] Unexpected error unpacking publication data: {str(e)}")
            continue

        # Add delay before processing each professor's publications
        delay = random.uniform(30, 180)  # 30 seconds to 3 minutes
        print(f"[Publications]: Waiting {delay:.1f} seconds before processing publications for {name}")
        time.sleep(delay)

        # Protected WebDriver setup
        driver = None
        try:
            print(f"[Publications] Setting up driver for {name}")
            proxy = get_random_proxy()
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')  # Run in headless mode
            if proxy:
                options.add_argument(f'--proxy-server={proxy}')
            driver = webdriver.Chrome(options=options)
            print(f"[Publications] Processing Publications of {name} at {school}:")
        except WebDriverException as e:
            print(f"[Publications] Failed to set up WebDriver for {name}: {str(e)}")
            if driver:
                driver.quit()
            continue
        except Exception as e:
            print(f"[Publications] Unexpected error setting up WebDriver for {name}: {str(e)}")
            if driver:
                driver.quit()
            continue

        try:
            embedding_text = ""
            successful_publications = 0
            
            for title, url, date in publications:
                try:
                    # Add delay between processing each publication
                    pub_delay = random.uniform(45, 180)  # 45 seconds to 3 minutes between publications
                    print(f"[Publications]: Waiting {pub_delay:.1f} seconds before processing publication: {title}")
                    time.sleep(pub_delay)
                    
                    print(f"[Publications] Processing publication: {title}")
                    driver.get(url)
                    print("[Publications] Got Driver")

                    wait = WebDriverWait(driver, 10)
                    print("[Publications] Set Up Wait")

                    # Protected publication body extraction
                    try:
                        publication_body_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.gsh_csp')))
                        publication_text = publication_body_div.text
                    except TimeoutException:
                        print(f"[Publications] Timeout waiting for publication body for {title}")
                        continue
                    except Exception as e:
                        print(f"[Publications] Error finding publication body for {title}: {str(e)}")
                        continue

                    # Protected title extraction
                    try:
                        title_a = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.gsc_oci_title_link')))
                        title_text = title_a.text
                    except TimeoutException:
                        print(f"[Publications] Timeout waiting for title link for {title}")
                        title_text = title  # Use the original title as fallback
                    except Exception as e:
                        print(f"[Publications] Error finding title link for {title}: {str(e)}")
                        title_text = title  # Use the original title as fallback
                    
                    # Protected text processing
                    try:
                        if publication_text and title_text:
                            embedding_text += f"Title: {title_text}\n\nDescription:\n\n{publication_text}\n\n"
                            successful_publications += 1
                            print("-"*50)
                            print("[Publications] Reading Publication")
                            print(f"Title: {title_text} with {len(publication_text)} character long description")
                            print("-"*50)
                        else:
                            print(f"[Publications] Empty content for {title}, skipping")
                    except Exception as e:
                        print(f"[Publications] Error processing text for {title}: {str(e)}")
                        continue
                        
                except WebDriverException as e:
                    print(f"[Publications] WebDriver error processing {title}: {str(e)}")
                    continue
                except Exception as e:
                    print(f"[Publications] Unexpected error processing {title}: {str(e)}")
                    continue
            
            # Protected final processing
            try:
                if embedding_text and successful_publications > 0:
                    print("="*50)
                    print(f"[Publications] Got Embedding Text for {name} ({successful_publications} publications):\n{embedding_text[:200]}...")
                    print("="*50)
                    postgres_insert_queue.put(("email_info", ABBR_TO_NAME[school], name, embedding_text))
                else:
                    print(f"[Publications] No valid embedding text collected for {name}")
            except Exception as e:
                print(f"[Publications] Error queuing embedding text for {name}: {str(e)}")

        except Exception as e:
            print(f"[Publications] Critical error processing {name}: {str(e)}")
        finally:
            if driver:
                try:
                    driver.quit()
                except Exception as e:
                    print(f"[Publications] Error closing driver for {name}: {str(e)}")
                    
    postgres_insert_queue.put(None)
    print("[Publications] Finished processing all publications")

def postgres_insert(postgres_insert_queue):
    """
    Inserts the publication data into the PostgreSQL database.
    """
    vectors = []
    while True:
        item = postgres_insert_queue.get()
        if item is None:
            break
            
        try:
            job = item[0]
        except (IndexError, TypeError) as e:
            print(f"[Postgres] Error unpacking job data: {str(e)}")
            continue
        except Exception as e:
            print(f"[Postgres] Unexpected error unpacking job data: {str(e)}")
            continue
            
        if job == "basic_info":
            try:
                job, school, name, email, href = item
                print(f"[Postgres] Inserting professor {name} into DB")
                print(f"[Postgres] Job type is {job}")
                
                insert_professor(school, name, email, href)
                print(f"[Postgres] Professor {name} inserted into DB")
                
            except ValueError as e:
                print(f"[Postgres] Error unpacking basic_info data: {str(e)}")
                continue
            except Exception as e:
                print(f"[Postgres] Error inserting professor: {str(e)}")
                continue
                
        elif job == "email_info":
            try:
                job, school, name, embedding_text = item
                print(f"[Postgres] Adding email information for {name} into DB")
                print(f"[Postgres] Job type is {job}")

                uuid = insert_embedding_text(school, name, embedding_text)
                print(f"[Postgres] Professor {name}'s email info inserted into DB")
                
            except ValueError as e:
                print(f"[Postgres] Error unpacking email_info data: {str(e)}")
                continue
            except Exception as e:
                print(f"[Postgres] Error inserting embedding text: {str(e)}")
                continue
        else:
            print(f"[Postgres] Unknown job type: {job}")
            continue

    print("[Postgres] Finished processing all database insertions")

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
    p_publications = Process(target=scrape_publications_page, args=(publication_queue, postgres_insert_queue))
    p_postgres_insert = Process(target=postgres_insert, args=(postgres_insert_queue,))

    print("Init Setup Done")

    p_main.start()
    p_profile.start()
    p_publications.start()
    p_postgres_insert.start()

    p_main.join()
    p_profile.join()
    p_publications.join()
    p_postgres_insert.join()

    print("All processes completed successfully")
