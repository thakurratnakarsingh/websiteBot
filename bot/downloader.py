import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
from selenium.webdriver.chrome.options import Options
from DatabaseQuery import DatabaseQuery  # Import the class
from downloadFuction import downloadNewFileAndUpload
from uploaderFile import uploadDownloadFile


def run_program():
    # Firefox/Tor settings
    tor_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    options = Options()
    options.binary_location = tor_path
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://skybap.com")

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

        db_query = DatabaseQuery()
        res = db_query.fetch_latest_entry()
        print("The Database latest entry is", res)

        if res:
            if res[2] == 1:  # Everything is completed download as well as upload
                print("Initiating file download...")
                downloadNewFileAndUpload(driver, res, db_query)
            if res[4] == 0:  # Condition for uploading
                print("Initiating file upload...")
                uploadDownloadFile(driver, res, db_query)
        else:
            print("No result found in the database.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    while True:
        print("Starting program execution...")
        run_program()
        print("Execution completed. Waiting for 30 minutes...")
        time.sleep(1 * 30)  # Wait for 30 minutes before the next execution
