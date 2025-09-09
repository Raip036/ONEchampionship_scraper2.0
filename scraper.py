from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import csv
import time

# Set up ChromeDriver service
service = Service('/opt/homebrew/bin/chromedriver')
driver = webdriver.Chrome(service=service)

# Base URL with pagination
base_url = "https://www.onefc.com/athletes/martial-art/muay-thai/page/{}/"

# Open CSV file
with open('fighters.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Name', 'Wins', 'Losses', 'Finishes','Country','Age','Team','Height'])

    page = 1
    while True:
        driver.get(base_url.format(page))
          # wait for page to load

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
            driver.get(link)
           

            try:
                name = driver.find_element(By.CLASS_NAME, 'use-letter-spacing-hint').text
            except:
                name = 'N/A'

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
                        
                    wins,value = win_count, ko_count
                except:
                    wins = 'N/A'

            try:
                losses = driver.find_element(By.CLASS_NAME, 'losses').text
                losses = losses.split("-")[-1].strip()
            except:
                try:
                    fight_rows = driver.find_elements(By.CLASS_NAME, 'is-data-row')
                    loss_count = 0

                    for row in fight_rows:
                        result = row.text.upper()
                        if 'LOSS' in result:
                            loss_count += 1
                        
                    losses = loss_count
                except:
                    losses = 'N/A'

            try:
                value = driver.find_element(By.CSS_SELECTOR,
                                            '#site-main > div:nth-child(3) > div > div > div > div:nth-child(3) > div > div > div.simple-stats-list > div:nth-child(1) > div.value').text

            except:
                finishes = 'N/A'

            try:
                attributes = driver.find_element(By.CLASS_NAME, "attributes")
                attrs = attributes.find_elements(By.CLASS_NAME, "attr")

                # Defaults
                height, country, age, team = "N/A", "N/A", "N/A", "N/A"

                for attr in attrs:
                    try:
                        title = attr.find_element(By.TAG_NAME, "h5").text.strip().lower()
                        value_elem = attr.find_element(By.CLASS_NAME, "value")
                        raw_value = value_elem.text.strip()

                        #print(f"Found attribute: {title} | Value: {raw_value}")  # debug

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

                    except Exception as inner_e:
                        print("Error parsing single attribute:", inner_e)

            except Exception as e:
                print("Error scraping attributes:", e)
                height, country, age, team = "N/A", "N/A", "N/A", "N/A"

# ⬇️ Now these should have real values, not N/A
            csv_writer.writerow([name, wins, losses, value, country, age, team, height])


           



           

            page += 1  # go to next page

driver.quit()
