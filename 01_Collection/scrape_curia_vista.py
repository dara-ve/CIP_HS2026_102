"""
Scrape completed "Anfragen" (questions) from Curia Vista (parlament.ch) with Selenium.

Steps:
1. Open the Curia Vista search page.
2. Select the filters "ANFRAGE" (business type) and "ERLEDIGT" (business state).
3. Collect all business items from the result list (page by page).
4. Open each business detail page and extract the metadata.
5. Save the result as CSV in 01_Collection/data/.
"""

import html
import re
import time
from pathlib import Path
from urllib.parse import unquote

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# --- Configuration -----------------------------------------------------------

BASE_URL = "https://www.parlament.ch"
SEARCH_URL = BASE_URL + "/de/ratsbetrieb/suche-curia-vista"

# Number of result pages to scrape (10 items per page). None = all pages.
MAX_PAGES = 2
HEADLESS = False
FILTER_WAIT = 5        # seconds to wait after selecting a filter
DETAIL_DELAY = 1       # seconds to wait between detail pages (be polite to the server)

OUTPUT_DIR = Path(__file__).parent / "data"
OUTPUT_FILE = OUTPUT_DIR / "curia_vista_anfragen_erledigt.csv"

# Filter checkboxes, identified by their onclick attribute.
# The business type value is hex-encoded: 416e6672616765 = "Anfrage".
FILTER_ANFRAGE = ("//label[contains(@onclick, 'PdAffairTypeName') "
                  "and contains(@onclick, '416e6672616765')]")
FILTER_ERLEDIGT = ("//label[contains(@onclick, 'PdBusinessStateType') "
                   "and contains(@onclick, '33\\')]")

# Pd.Search.InsertItemInPickedAffairsList('26.4265','Title','Type','Submitter','State','/de/...')
ONCLICK_PATTERN = re.compile(r"InsertItemInPickedAffairsList\((.*)\)")


# --- Browser -----------------------------------------------------------------

def create_driver():
    options = webdriver.ChromeOptions()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1400,1000")
    return webdriver.Chrome(options=options)


def js_click(driver, element):
    """Click via JavaScript, because some elements are covered (e.g. 'back to top' button)."""
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    driver.execute_script("arguments[0].click();", element)


# --- Search result list ------------------------------------------------------

def apply_filters(driver):
    driver.get(SEARCH_URL)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, FILTER_ANFRAGE)))

    for xpath in (FILTER_ANFRAGE, FILTER_ERLEDIGT):
        checkbox = driver.find_element(By.XPATH, xpath)
        print(f"Selecting filter: {checkbox.text}")
        js_click(driver, checkbox)
        time.sleep(FILTER_WAIT)

    print(driver.find_element(By.ID, "ResultCount").text.strip())


def parse_result_items(driver):
    """Read all business items on the current result page from their export links."""
    items = []
    for link in driver.find_elements(By.CSS_SELECTOR, "a.add-business-item-to-exportlist"):
        match = ONCLICK_PATTERN.search(link.get_attribute("onclick") or "")
        if not match:
            continue
        args = [html.unescape(unquote(arg)) for arg in re.findall(r"'([^']*)'", match.group(1))]
        if len(args) < 6:
            continue
        number, title, business_type, submitter, state, url = args[:6]
        items.append({
            "business_number": number,
            "title": title,
            "business_type": business_type,
            "submitter_list": submitter,
            "state_list": state,
            "url": BASE_URL + url,
        })
    return items


def go_to_next_page(driver, first_number):
    """Click 'next page' and wait until the result list has changed."""
    try:
        next_link = driver.find_element(By.ID, "PageLinkNext")
    except NoSuchElementException:
        return False

    js_click(driver, next_link)
    try:
        WebDriverWait(driver, 30).until(
            lambda d: parse_result_items(d) and parse_result_items(d)[0]["business_number"] != first_number
        )
    except TimeoutException:
        return False
    return True


def collect_result_list(driver):
    all_items = []
    page = 1
    while True:
        items = parse_result_items(driver)
        print(f"Page {page}: {len(items)} items")
        all_items.extend(items)

        if not items or (MAX_PAGES is not None and page >= MAX_PAGES):
            break
        if not go_to_next_page(driver, items[0]["business_number"]):
            break
        page += 1
    return all_items


# --- Detail page -------------------------------------------------------------

def text_of(element):
    # textContent also works for elements inside collapsed accordions
    return " ".join((element.get_attribute("textContent") or "").split())


def text_after_heading(driver, heading):
    """Return the text of the paragraph that follows an <h3> heading, e.g. 'Zuständige Behörde'."""
    elements = driver.find_elements(
        By.XPATH, f"//h3[normalize-space()='{heading}']/following-sibling::p[1]"
    )
    return text_of(elements[0]) if elements else None


def scrape_detail(driver, url):
    driver.get(url)
    # The page is rendered by Angular: wait until the last metadata row is there
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[@id='wsAffairPage']//span[contains(@class, 'meta-key') "
                       "and contains(., 'Stand der Beratungen')]")
        )
    )
    # The submitter link is rendered a bit later (missing if the submitter is e.g. a committee)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#wsAffairPage div.meta-desc-group a.person-name"))
        )
    except TimeoutException:
        pass
    time.sleep(1)

    data = {
        "affair_id": url.split("AffairId=")[-1],
        "submitted_by": None,
        "councillor_id": None,
        "parliamentary_group": None,
        "party": None,
    }

    # Metadata rows: "Eingereicht von", "Einreichungsdatum", "Eingereicht im", "Stand der Beratungen"
    for row in driver.find_elements(By.CSS_SELECTOR, "#wsAffairPage div.pd-description.meta-desc-group"):
        key = text_of(row.find_element(By.CSS_SELECTOR, ".meta-key")).rstrip(":")

        if key == "Eingereicht von":
            names = row.find_elements(By.CSS_SELECTOR, "a.person-name")
            if names:
                data["submitted_by"] = text_of(names[0])
                data["councillor_id"] = names[0].get_attribute("href").split("CouncillorId=")[-1]
            else:
                # Submitter is not a person (e.g. a committee)
                data["submitted_by"] = text_of(row).replace("Eingereicht von:", "").strip()
            paragraphs = [text_of(p) for p in row.find_elements(By.CSS_SELECTOR, ".col-sm-8 p")]
            paragraphs = [p for p in paragraphs if p]
            if len(paragraphs) >= 1:
                data["parliamentary_group"] = paragraphs[0]
            if len(paragraphs) >= 2:
                data["party"] = paragraphs[1]
        elif key == "Einreichungsdatum":
            data["submission_date"] = text_of(row.find_element(By.CSS_SELECTOR, ".meta-value"))
        elif key == "Eingereicht im":
            data["submitted_in"] = text_of(row.find_element(By.CSS_SELECTOR, ".meta-value"))
        elif key == "Stand der Beratungen":
            data["state"] = text_of(row.find_element(By.CSS_SELECTOR, ".meta-value"))

    data["responsible_authority"] = text_after_heading(driver, "Zuständige Behörde")
    data["first_council"] = text_after_heading(driver, "Erstbehandelnder Rat")

    cosigners = driver.find_elements(By.CSS_SELECTOR, "div.block-284 a.person-name")
    data["cosigners"] = "; ".join(text_of(c) for c in cosigners)
    data["cosigner_count"] = len(cosigners)

    topics = driver.find_elements(By.CSS_SELECTOR, "div.block-285 p span")
    data["topics"] = "; ".join(text_of(t) for t in topics if text_of(t))

    return data


# --- Main --------------------------------------------------------------------

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    driver = create_driver()
    try:
        apply_filters(driver)
        items = collect_result_list(driver)
        print(f"Collected {len(items)} items from the result list")

        rows = []
        for i, item in enumerate(items, start=1):
            print(f"[{i}/{len(items)}] {item['business_number']} {item['title'][:60]}")
            try:
                details = scrape_detail(driver, item["url"])
            except (TimeoutException, NoSuchElementException) as e:
                print(f"  -> detail page could not be read, skipped ({type(e).__name__})")
                details = {}
            rows.append({**item, **details})
            time.sleep(DETAIL_DELAY)
    finally:
        driver.quit()

    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
    print(f"Saved {len(df)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
