import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# 1. Anti-bot configurations to stay under the radar in headless mode
options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument(
    "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# Spin up Chrome driver with auto-managed driver binaries
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Extra sneaky step: strip out the default navigator.webdriver property
driver.execute_script(
    "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
)

wait = WebDriverWait(driver, 15)
base_url = "https://www.audible.com/search"

all_books_data = []

try:
    # First, let's hit the landing page and figure out how many total pages we're dealing with
    driver.get(base_url)

    pagination = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, '//ul[contains(@class, "pagingElements")]')
        )
    )
    pages = pagination.find_elements(By.TAG_NAME, "li")
    page_numbers = [p.text.strip() for p in pages if p.text.strip() != ""]

    # Check if a "Next" button exists in the pagination bar to grab the right last page index
    if "Go forward a page" in page_numbers:
        last_page = int(page_numbers[-2])
    else:
        last_page = int(page_numbers[-1])

    print(f"Total Pages Found: {last_page}\n")

    # 2. Loop through each page directly using URL query parameters (far more reliable than clicking 'Next')
    for current_page in range(1, last_page + 1):
        page_url = f"{base_url}?page={current_page}"
        print(f"Scraping Page {current_page} of {last_page} -> {page_url}")

        driver.get(page_url)

        # Make sure the container holding all the book listings is present
        container = wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "adbl-impression-container")
            )
        )

        # Brief pause to give AJAX/JavaScript content enough room to fully render
        time.sleep(1)

        products = container.find_elements(
            By.XPATH, './/li[contains(@class, "productListItem")]'
        )

        page_books_count = 0

        # Parse details for every single book on the page safely
        for product in products:
            try:
                title_elem = product.find_element(
                    By.XPATH,
                    './/*[contains(@class, "bc-heading")]//a | .//h3//a | .//h3',
                )
                title = title_elem.text.strip()
            except Exception:
                title = None

            try:
                author_elem = product.find_element(
                    By.XPATH, './/*[contains(@class, "authorLabel")]'
                )
                author = (
                    author_elem.text.replace("By:", "")
                    .replace("By", "")
                    .strip()
                )
            except Exception:
                author = None

            try:
                length_elem = product.find_element(
                    By.XPATH, './/*[contains(@class, "runtimeLabel")]'
                )
                length = length_elem.text.replace("Length:", "").strip()
            except Exception:
                length = None

            try:
                ratings = product.find_element(
                    By.XPATH, './/*[contains(@class, "bc-size-callout")]'
                ).text.strip()
            except Exception:
                ratings = None

            if title:
                all_books_data.append(
                    {
                        "page": current_page,
                        "title": title,
                        "author": author,
                        "length": length,
                        "ratings": ratings,
                    }
                )
                page_books_count += 1

        print(
            f"Done Page {current_page} (Added {page_books_count} books). Total collected: {len(all_books_data)}\n"
        )

    # 3. Dump all the scraped dataset into a clean CSV file
    csv_file = "audible_books.csv"
    fieldnames = ["page", "title", "author", "length", "ratings"]

    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_books_data)

    print(
        f"All done! Successfully scraped {len(all_books_data)} books and saved into '{csv_file}'."
    )

finally:
    # Always clean up and close the browser session
    driver.quit()