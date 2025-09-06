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
    csv_writer.writerow(['Name', 'Wins', 'Losses', 'Finishes'])

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

            # Write row into CSV
            csv_writer.writerow([name, wins, losses, value])

        page += 1  # go to next page

driver.quit()
