from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Set up ChromeDriver service
service = Service('/opt/homebrew/bin/chromedriver')

# Create the driver using the service
driver = webdriver.Chrome(service=service)

# Navigate to the page
driver.get('https://www.onefc.com/athletes/jonathan-haggerty/')
name = driver.find_element(By.CLASS_NAME, 'use-letter-spacing-hint')
wins = driver.find_element(By.CLASS_NAME, 'wins')
losses = driver.find_element(By.CLASS_NAME, 'losses')

# Navigating class by class
stats_section = driver.find_element(By.CLASS_NAME, 'simple-stats-list')
value = stats_section.find_element(By.CLASS_NAME, 'value')


print(name.text)
print(wins.text)
print(losses.text)
print("Finishes: ",value.text)








# Close the browser
driver.quit()
