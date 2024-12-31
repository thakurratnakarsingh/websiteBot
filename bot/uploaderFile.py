import time
from selenium.webdriver.common.by import By
from downloadUpload import fileIsDownloadedNowUpload
from linkShorter import  LinkShorterMaking
from telegramCommonFunction import clear_directory_and_recycle_bin

def uploadDownloadFile(driver, res ,db_query):
    try:
        global previous_element
        global full_url
        print("Uploader file working with input:", res)
        if res:
            name = res[1]  # This is the name from the database
            print(f"Looking for series name: {name}")
            # Find the matching series
            web_series_elements = driver.find_elements(By.TAG_NAME, 'a')
            for i, element in enumerate(web_series_elements):
                if name in element.text:
                    print(f"Found matching series: {element.text}")
                    if i > 0:
                        previous_element = web_series_elements[i]
                        previous_element_text = previous_element.text  # Store the text immediately
                        print(f"Clicking the series above: {previous_element_text}")
                        previous_href = previous_element.get_attribute('href')
                        if previous_href:
                            full_url = previous_href
                            print(f"Passing URL to ContentPage: {full_url}")
                            if res[6]:
                               print(f"This pressing of the short url is new {res[0]}")
                               response = fileIsDownloadedNowUpload(driver,full_url,res[6])
                               if response == 1 :
                                   print("Image and message sent successfully.")
                                   db_query.updateIsCompleted(res[0],1)
                                   clear_directory_and_recycle_bin(r"D:\testing")
                                   return
                            else:
                              getShortUrl = LinkShorterMaking(driver ,res[5])
                              print(f"Short URL to Linkshorter: {getShortUrl}")
                              db_query.updateShortUrl(res[0],getShortUrl)
                              response = fileIsDownloadedNowUpload(driver, full_url, res[6])
                              if response == 1:
                                  print("Image and message sent successfully.")
                                  db_query.updateIsCompleted(res[0], 1)
                                  clear_directory_and_recycle_bin(r"D:\testing")

                                  return
                              print(f"After Short URL to full url: {full_url}")
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
        print("An error occurred in uploadDownloadFile:", str(e))
