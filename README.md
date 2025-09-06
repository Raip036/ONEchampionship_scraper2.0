# ONE Championship Fighter Scraper

This project is a **web scraper** built with [Selenium](https://www.selenium.dev/) to collect fighter statistics from the [ONE Championship website](https://www.onefc.com/athletes/).  
It navigates through paginated fighter listings, follows each fighter profile, and extracts stats like:

- **Name**
- **Wins**
- **Losses**
- **KO Wins** (from fight history if standard records are missing)

The scraped data is stored in a CSV file (`fighters.csv`) for analysis or integration into other projects (e.g., predictive analytics, dashboards, data science projects).

---

## 🚀 Features
- Scrapes all fighters across multiple pages automatically.
- Extracts records from both:
  - Fighter profile stats (when available).
  - Fight history table (fallback when profile stats missing).
- Tallies KO wins by scanning fight history rows.
- Saves clean structured data into a CSV file.

---

## 🛠️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/one_scraper.git
cd one_scraper
2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows
3. Install dependencies
Install all required Python packages from requirements.txt:
pip install -r requirements.txt
4. Install ChromeDriver
This project requires Google Chrome and ChromeDriver.
On macOS with Homebrew:
brew install chromedriver
Or download manually from: https://chromedriver.chromium.org/
Make sure the chromedriver binary is available in /opt/homebrew/bin/ or update the path in your Python script:
service = Service('/opt/homebrew/bin/chromedriver')
▶️ Running the Scraper
From inside the virtual environment, run:
python scraper.py
The script will:
Visit each fighter listing page.
Collect profile links.
Scrape name, wins, losses, and KO wins.
Save everything to fighters.csv.
