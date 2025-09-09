from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import csv
import time
import random
import os

# Set up ChromeDriver service
service = Service('/opt/homebrew/bin/chromedriver')
driver = webdriver.Chrome(service=service)

# Base URL with pagination
base_url = "https://www.onefc.com/athletes/martial-art/muay-thai/page/{}/"

csv_file = "fighters.csv"
error_file = "errors.log"

# Check if CSV already exists (resume mode)
existing_names = set()
if os.path.exists(csv_file):
    with open(csv_file, "r", encoding="utf-8") as f:
        existing_names = {line.split(",")[0] for line in f.readlines()[1:]}  # skip header

# Open CSV file in append mode
with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)

    # Write header only if file was new
    if os.stat(csv_file).st_size == 0:
        writer.writerow(['Name', 'Wins', 'Losses', 'Finishes', 'Country', 'Age', 'Team', 'Height'])

    page = 1
    while True:
        driver.get(base_url.format(page))
        time.sleep(2)  # let page load

        fighter_cards = driver.find_elements(By.CLASS_NAME, 'simple-post-card')
        if not fighter_cards:
            break  # stop if no more fighters

        # collect links from current page
        fighter_links = [
            card.find_element(By.TAG_NAME, 'a').get_attribute('href')
            for card in fighter_cards
        ]

        # scrape each fighter page
        for link in fighter_links:
            try:
                driver.get(link)
                time.sleep(random.uniform(1, 2))  # polite delay

                try:
                    name = driver.find_element(By.CLASS_NAME, 'use-letter-spacing-hint').text
                except:
                    name = 'N/A'

                # Skip if already scraped
                if name in existing_names:
                    print(f"Skipping already scraped fighter: {name}")
                    continue

                # Wins
                try:
                    wins = driver.find_element(By.CLASS_NAME, 'wins').text
                    wins = wins.split("-")[-1].strip()
                except:
                    try:
                        fight_rows = driver.find_elements(By.CLASS_NAME, 'is-data-row')
                        win_count, ko_count = 0, 0
                        for row in fight_rows:
                            result = row.text.upper()
                            if 'WIN' in result:
                                win_count += 1
                                if 'KO' in result or 'TKO' in result:
                                    ko_count += 1
                        wins, value = win_count, ko_count
                    except:
                        wins, value = 'N/A', 'N/A'

                # Losses
                try:
                    losses = driver.find_element(By.CLASS_NAME, 'losses').text
                    losses = losses.split("-")[-1].strip()
                except:
                    try:
                        fight_rows = driver.find_elements(By.CLASS_NAME, 'is-data-row')
                        loss_count = 0
                        for row in fight_rows:
                            if 'LOSS' in row.text.upper():
                                loss_count += 1
                        losses = loss_count
                    except:
                        losses = 'N/A'

                # Finishes (KO/TKO etc.)
                try:
                    value = driver.find_element(By.CSS_SELECTOR,
                        '#site-main > div:nth-child(3) > div > div > div > div:nth-child(3) > div > div > div.simple-stats-list > div:nth-child(1) > div.value'
                    ).text
                except:
                    value = 'N/A'

                # Attributes (height, country, age, team)
                try:
                    attributes = driver.find_element(By.CLASS_NAME, "attributes")
                    attrs = attributes.find_elements(By.CLASS_NAME, "attr")
                    height, country, age, team = "N/A", "N/A", "N/A", "N/A"

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
                    height, country, age, team = "N/A", "N/A", "N/A", "N/A"

                # Write to CSV
                writer.writerow([name, wins, losses, value, country, age, team, height])
                existing_names.add(name)
                print(f"✅ Saved: {name}")

            except Exception as e:
                print(f"❌ Failed on {link}: {e}")
                with open(error_file, "a", encoding="utf-8") as log:
                    log.write(link + "\n")

        page += 1  # go to next page

driver.quit()
