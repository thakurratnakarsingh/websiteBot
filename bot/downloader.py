from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
from selenium.webdriver.chrome.options import Options
from DatabaseQuery import DatabaseQuery  # Import the class
from ContentPage import download_images  # Import the function
import time  # Import time module for delay

# Firefox/Tor settings
tor_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
# tor_path = r'C:\Program Files\Mozilla Firefox\firefox.exe'
options = Options()
options.binary_location = tor_path
# driver = webdriver.Firefox(options=options)
driver = webdriver.Chrome(options=options)
driver.get("https://skybap.com")

try:
    # Wait for the link to 'https://skymovieshd.chat/'
    link = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'https://skymovieshd')]"))
    )
    url = link.get_attribute('href')
    parsed_url = urlparse(url)
    domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
    print(f"The URL is new and the things are: {domain}")
    driver.execute_script("arguments[0].scrollIntoView(true);", link)
    driver.execute_script("arguments[0].click();", link)
    print("Clicked the link successfully using JavaScript.")

    all_web_series_link = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Hot Short Film"))
    )
    all_web_series_link.click()
    print("Navigated to 'Hot Short Film'.")

    # Fetch the latest entry from the database
    db_query = DatabaseQuery()  # Create an instance of DatabaseQuery
    res = db_query.fetch_latest_entry()  # Call the method to get the latest entry
    print("The Database latest entry is",res)

    if res:
        name = res[1]  # This is the name from the database
        print(f"Looking for series name: {name}")

        # Find the matching series
        web_series_elements = driver.find_elements(By.TAG_NAME, 'a')

        for i, element in enumerate(web_series_elements):
            if name in element.text:
                print(f"Found matching series: {element.text}")

                # Find the element above it
                if i > 0:
                    previous_element = web_series_elements[i - 1]
                    print(f"Clicking the series above: {previous_element.text}")

                    # Extract the href from the previous element
                    previous_href = previous_element.get_attribute('href')
                    if previous_href:
                        full_url = previous_href
                        print(f"Passing URL to ContentPage: {full_url}")
                       #download_Done = download_images(driver, full_url)
                        download_Done = (1, 'https://f1.fastdl.lol/Achamka.2024.720p.HEVC.WeB-DL.Bengali.AAC2.0.H.265-SkymoviesHD.mkv')
                        print(f"Download completed with status: {download_Done}")
                        print("Keeping the browser open for 10 minutes...")
                        db_query.insert_entry(previous_element.text, 0, download_Done[0], 0)
                        time.sleep(600)  # 600 seconds = 10 minutes
                        db_query.close_connection()
                    else:
                        print("No href found for the previous element.")
                else:
                    print("This is the first element, no element above to click.")
                break
        else:
            print("No matching series found.")
    else:
        print("No result found in the database.")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the browser after the delay
    driver.quit()
