from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import csv
import time

# Set up ChromeDriver service
service = Service('/opt/homebrew/bin/chromedriver')

# Create the driver using the service
driver = webdriver.Chrome(service=service)

# Navigate to the page
driver.get('https://www.onefc.com/athletes/martial-art/muay-thai/')

fighter_cards = driver.find_elements(By.CLASS_NAME, 'simple-post-card')

csv_file = open('fighters.csv', mode='w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Name', 'Wins', 'Losses', 'Finishes'])

for card in fighter_cards:
    link = card.find_element(By.TAG_NAME, 'a').get_attribute('href')
    driver.get(link)
     # Wait for the page to load

    try:
        name = driver.find_element(By.CLASS_NAME, 'use-letter-spacing-hint').text
    except:
        name = 'N/A'
    try:
        wins = driver.find_element(By.CLASS_NAME, 'wins').text
        wins = wins.split("-")[-1].strip()  # Extract only the number
    except:
        wins = 'N/A'
    try:
        losses = driver.find_element(By.CLASS_NAME, 'losses').text
        losses = losses.split("-")[-1].strip()  # Extract only the number
    except:
        losses = 'N/A'
    try:
        value = driver.find_element(By.CSS_SELECTOR,
                                    '#site-main > div:nth-child(3) > div > div > div > div:nth-child(3) > div > div > div.simple-stats-list > div:nth-child(1) > div.value').text
    except:
        value = 'N/A'

    csv_writer.writerow([name, wins, losses, value])

    driver.back()
      # Wait for the page to load

csv_file.close()
driver.quit()

    








# Close the browser
driver.quit()
