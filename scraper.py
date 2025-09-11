from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import csv
import time
import random
import os

# ---------------- ChromeDriver Setup ----------------
service = Service('/opt/homebrew/bin/chromedriver')
driver = webdriver.Chrome(service=service)

# ---------------- URL & Files ----------------
base_url = "https://www.onefc.com/athletes/martial-art/muay-thai/page/{}/"
csv_file = "fighters.csv"
error_file = "errors.log"

# ---------------- Resume Mode ----------------
existing_names = set()
if os.path.exists(csv_file):
    with open(csv_file, "r", encoding="utf-8") as f:
        existing_names = {line.split(",")[0] for line in f.readlines()[1:]}  # skip header

# ---------------- Open CSV ----------------
with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    if os.stat(csv_file).st_size == 0:
        writer.writerow(['Name', 'Wins', 'Losses', 'Finishes', 'Country', 'Age', 'Team', 'Height'])

    page = 1
    while True:
        driver.get(base_url.format(page))
        

        fighter_cards = driver.find_elements(By.CLASS_NAME, 'simple-post-card')
        if not fighter_cards:
            break  # no more fighters

        # Collect links from current page
        fighter_links = [card.find_element(By.TAG_NAME, 'a').get_attribute('href') for card in fighter_cards]

        # ---------------- Scrape each fighter ----------------
        for link in fighter_links:
            try:
                driver.get(link)
                

                # Name
                try:
                    name = driver.find_element(By.CLASS_NAME, 'use-letter-spacing-hint').text.strip()
                except:
                    name = 'N/A'

                if name in existing_names:
                    print(f"Skipping already scraped fighter: {name}")
                    continue

                # ---------------- Fight Records ----------------
                fight_rows = driver.find_elements(By.CLASS_NAME, 'is-data-row')
                win_count, loss_count, ko_count = 0, 0, 0

                for row in fight_rows:
                    try:
                        # Result text (WIN / LOSS)
                        result_text = row.find_element(By.CLASS_NAME, 'result').text.upper()

                        if 'WIN' in result_text:
                            win_count += 1

                            # KO/TKO check with fallback
                            method_text = ""
                            try:
                                # Small-screen responsive span
                                method_span = row.find_element(By.CSS_SELECTOR,
                                                               'div.result-method-and-round span.d-sm-none')
                                method_text = method_span.text.strip().upper()
                            except:
                                pass

                            if not method_text:
                                try:
                                    # Desktop td.method fallback
                                    method_td = row.find_element(By.CSS_SELECTOR, 'td.method')
                                    method_text = method_td.text.strip().upper()
                                except:
                                    method_text = ""

                            if 'KO' in method_text or 'TKO' in method_text or 'KNOCKOUT' in method_text:
                                ko_count += 1

                        elif 'LOSS' in result_text:
                            loss_count += 1

                    except Exception as e:
                        print("Error parsing fight row:", e)
                        continue

                wins, losses, finishes = win_count, loss_count, ko_count

                # ---------------- Attributes (Height, Country, Age, Team) ----------------
                height, country, age, team = "N/A", "N/A", "N/A", "N/A"
                try:
                    attributes = driver.find_element(By.CLASS_NAME, "attributes")
                    attrs = attributes.find_elements(By.CLASS_NAME, "attr")

                    for attr in attrs:
                        title = attr.find_element(By.TAG_NAME, "h5").text.strip().lower()
                        value_elem = attr.find_element(By.CLASS_NAME, "value")
                        raw_value = value_elem.text.strip()

                        if title == "height":
                            if "/" in raw_value and "cm" in raw_value.lower():
                                height = raw_value.split("/")[-1].replace("CM", "").strip()
                            else:
                                height = raw_value

                        elif title == "country":
                            countries = [c.text.strip() for c in value_elem.find_elements(By.TAG_NAME, "a")]
                            country = ", ".join(countries) if countries else raw_value

                        elif title == "age":
                            age = raw_value.replace("Y", "").strip()

                        elif title == "team":
                            team = raw_value

                except Exception as e:
                    print("Error scraping attributes:", e)

                # ---------------- Write to CSV ----------------
                writer.writerow([name, wins, losses, finishes, country, age, team, height])
                existing_names.add(name)
                print(f"✅ Saved: {name} | Wins: {wins}, Losses: {losses}, Finishes: {finishes}")

            except Exception as e:
                print(f"❌ Failed on {link}: {e}")
                with open(error_file, "a", encoding="utf-8") as log:
                    log.write(link + "\n")

        page += 1  # next page

driver.quit()
