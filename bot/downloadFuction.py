from selenium.webdriver.common.by import By
from ContentPage import download_images
from downloadUpload import fileIsDownloadedNowUpload
from linkShorter import  LinkShorterMaking
from telegramCommonFunction import clear_directory_and_recycle_bin

def downloadNewFileAndUpload(driver, res, db_query):
    try:
        global previous_element

        if res:
            name = res[1]  # This is the name from the database
            print(f"Looking for series name: {name}")
            web_series_elements = driver.find_elements(By.TAG_NAME, 'a')

            for i, element in enumerate(web_series_elements):
                if name in element.text:
                    print(f"Found matching series: {element.text}")

                    # Find the element above it
                    if i > 0:
                        previous_element = web_series_elements[i - 1]
                        previous_element_text = previous_element.text  # Store the text immediately
                        print(f"Clicking the series above: {previous_element_text}")

                        # Extract the href from the previous element
                        previous_href = previous_element.get_attribute('href')
                        if previous_href:
                            full_url = previous_href
                            print(f"Passing URL to ContentPage: {full_url}")
                            download_Done = download_images(driver, full_url)
                            print(f"Download completed with status: {download_Done}  new data is  {download_Done[1]}")
                            print("Keeping the browser open for 10 minutes...", previous_element_text)
                            db_query.insert_entry(previous_element_text, 0, download_Done[0], 0,download_Done[1])
                            getShortUrl = LinkShorterMaking(driver, download_Done[1])
                            print(f"Short URL to Linkshorter: {getShortUrl}")
                            response = db_query.fetch_latest_entry()
                            print("The Database latest entry is response", response)
                            db_query.updateShortUrl(response[0], getShortUrl)
                            responses = fileIsDownloadedNowUpload(driver, full_url, getShortUrl)
                            if responses == 1:
                                print("Image and message sent successfully.")
                                db_query.updateIsCompleted(response[0], 1)
                                clear_directory_and_recycle_bin(r"D:\testing")
                                return
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
        driver.quit()
