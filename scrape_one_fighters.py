import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import pandas as pd

# Initialize Chrome (headless mode for efficiency)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in background (remove if debugging)
driver = webdriver.Chrome(options=options)
url = "https://www.onefc.com/athletes/"
driver.get(url)

# Wait for initial fighters to load
time.sleep(3)  # Allow JavaScript to render

# Keep clicking "Show More" until it disappears
while True:
    try:
        # Find the button and scroll into view
        show_more = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.load-more"))
        )
        ActionChains(driver).move_to_element(show_more).perform()  # Scroll to button
        time.sleep(1)  # Small delay to avoid detection
        
        # Click using JavaScript (bypasses some anti-bot checks)
        driver.execute_script("arguments[0].click();", show_more)
        
        # Wait for new fighters to load (adjust timeout as needed)
        time.sleep(3)  
        
        # Optional: Check if the button still exists
        if not driver.find_elements(By.CSS_SELECTOR, "a.load-more"):
            break
    except Exception as e:
        print(f"Stopped clicking: {e}")
        break

# Parse all fighters
soup = BeautifulSoup(driver.page_source, "html.parser")
fighters = []
for fighter in soup.select("div.simple-post-card.is-athlete"):
    name = fighter.select_one("h3").text.strip()
    country = fighter.select_one("div.country").text.strip()
    link = fighter.select_one("a.image")["href"]
    img = fighter.select_one("img")["src"]
    
    fighters.append({
        "Name": name,
        "Country": country,
        "Link": link,
        "Image": img
    })

# Save to CSV
pd.DataFrame(fighters).to_csv("one_fighters_all.csv", index=False)
print(f"Scraped {len(fighters)} fighters!")
driver.quit()