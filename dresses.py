from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv
import time

# ✅ Chrome setup
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service("/usr/lib/chromium-browser/chromedriver")
driver = webdriver.Chrome(service=service, options=options)

print("🌐 Opening M&S dresses page...")
driver.get("https://www.marksandspencer.com/l/women/dresses")
time.sleep(5)

# ✅ Scroll to load all products
for i in range(8):
    driver.execute_script("window.scrollBy(0, 1000);")
    time.sleep(2)

print("✅ Page loaded… extracting data")

# ✅ UPDATED SELECTORS (as of Nov 2025)
titles = driver.find_elements(By.CSS_SELECTOR, "a[data-test='product-tile-link'] h2")
prices = driver.find_elements(By.CSS_SELECTOR, "span[data-test='product-tile-price']")

print(f"🛍 Found {len(titles)} titles and {len(prices)} prices")

data = []
for t, p in zip(titles, prices):
    title = t.text.strip()
    price = p.text.strip()
    data.append([title, price])
    print(f"{title} — {price}")

# ✅ Save data to CSV
if data:
    with open("/home/sheba/Desktop/data.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Price"])
        writer.writerows(data)
    print("💾 Data saved successfully to Desktop/data.csv ✅")
else:
    print("⚠️ Still empty. Try increasing scroll count or checking site structure.")

driver.quit()
