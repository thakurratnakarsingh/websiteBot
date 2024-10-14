from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Path to the Tor browser's executable
tor_path = r'C:\Program Files\Mozilla Firefox\firefox.exe'  # Modify if using Tor
options = Options()
options.binary_location = tor_path

# Create a webdriver instance using the Tor browser or Firefox
driver = webdriver.Firefox(options=options)

# Open the website
driver.get("https://skybap.com")

# Wait for the page to load and the link to appear
try:
    # Wait for the link to 'https://skymovieshd.chat/'
    link = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'https://skymovieshd')]"))
    )

    # Scroll the element into view and click it using JavaScript
    driver.execute_script("arguments[0].scrollIntoView(true);", link)
    driver.execute_script("arguments[0].click();", link)
    print("Clicked the link successfully using JavaScript.")

    # Wait for the "All Web Series" link to appear
    all_web_series_link = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Hot Short Film"))
    )

    all_web_series_link.click()
    print("Navigated to 'Hot Short Film'.")

except Exception as e:
    print(f"An error occurred: {e}")

# Keep the browser open for a longer time before closing it
time.sleep(1000)

# Close the browser
driver.quit()
