from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import requests  # Import requests for file download

# Define the download function first


# Set up the Selenium WebDriver with Chrome
tor_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
options = Options()
options.binary_location = tor_path

driver = webdriver.Chrome(options=options)
driver.get("https://gamerxyt.com/hubcloud.php?host=hubcloud&id=0zyw0cu3wsihico&token=R2QvNittcnA0Q0hwWjI0d1JUWEN1b1ZWaUJzZzdlNTJEV1A0WjVjN3Jhbz0=")

# Wait for the page to load completely
time.sleep(30)

try:
    # Wait until the "Download [FSL Server]" link is clickable
    fsl_server_link = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Download [FSL Server]')]"))
    )
    # driver.execute_script("arguments[0].scrollIntoView(true);", fsl_server_link)
    # time.sleep(5)
    file_download_url = fsl_server_link.get_attribute("href")  # Get the href of the download link
    download_file_with_progress(file_download_url, 'D:\\testing')  # Start file download with progress logging
    # driver.execute_script("arguments[0].click();", fsl_server_link)
    print("Clicked on Download [FSL Server] link.")
    print(f"File download URL: {file_download_url}")

except Exception as e:
    print(f"An error occurred while clicking on Download [FSL Server] link: {e}")

# Keep the page open for 10 minutes
time.sleep(600)

# Close the driver after 10 minutes
driver.quit()
