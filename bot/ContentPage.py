
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os
import re
import requests

def download_file_with_progress(url, save_path):
    # Ensure save directory exists
    os.makedirs(save_path, exist_ok=True)

    # Extract clean file name (remove query parameters)
    file_name = url.split("/")[-1].split("?")[0]  # File name without query parameters
    local_filename = os.path.join(save_path, file_name)

    try:
        # Download file with requests
        with requests.get(url, stream=True) as response:
            response.raise_for_status()  # Raise error for HTTP issues
            total_size = int(response.headers.get('content-length', 0))  # Get total file size
            chunk_size = 1024  # 1 KB chunks
            downloaded_size = 0

            with open(local_filename, "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    downloaded_size += len(data)
                    percent = (downloaded_size / total_size) * 100
                    print(f"\rDownload progress: {percent:.2f}%", end="")

        print(f"\nFile downloaded successfully and saved at: {local_filename}")
    except Exception as e:
        print(f"Error during file download: {e}")

def download_from_streamtape(driver, url):
    print("download_from_streamtape is working")
    driver.get(url)  # Navigate to the download URL
    time.sleep(5)  # Adjust time as needed for loading

def download_from_vidtube(driver, url):
    print("download_from_vidtube is working")
    driver.get(url)  # Navigate to the download URL
    time.sleep(5)  # Adjust time as needed for loading


def download_from_indishare(driver, url):
    print("download_from_streamtape is working")
    driver.get(url)  # Navigate to the download URL
    time.sleep(5)  # Adjust time as needed for loading

def download_from_dropgalaxy(driver, url):
    print("download_from_dropgalaxy is working")
    driver.get(url)
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.NAME, "method_premium"))
    )
    time.sleep(10)
    try:
        # Make the Free Download button visible via JavaScript
        overlay = driver.find_element(By.CLASS_NAME, "ra-overlay")

        # Remove the overlay using JavaScript
        driver.execute_script("""
                var overlay = arguments[0];
                overlay.parentNode.removeChild(overlay);
            """, overlay)
        print("Overlay removed successfully.")
        driver.execute_script("document.getElementById('method_free').style.display = 'block';")
        print("Made Free Download button visible.")
        # Locate and click the "Free Download" button
        free_download_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "method_free"))
        )
        free_download_button.click()
        # download_file = free_download_button.get_attribute('href')
        print("Clicked on Free Download button.",)

        time.sleep(1000)
    except Exception as e:
        print(f"Error clicking Free Download button: {e}")


def download_from_hubdrive(driver, url):
    global download_url_hubcloud_link
    print("Starting download_from_hubdrive...")
    driver.get(url)
    time.sleep(20)  # Initial wait for the page to load

    try:
        # Wait for any obscuring element to disappear
        WebDriverWait(driver, 20).until(
            EC.invisibility_of_element_located((By.XPATH, "//a[@id='lkkis']"))
        )

        # Wait for the HubCloud link to be visible
        hubcloud_link = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//h5/a[contains(@href, 'hubcloud')]"))
        )

        # Click on HubCloud download link
        driver.execute_script("arguments[0].click();", hubcloud_link)
        print(f"Clicked on HubCloud download link: {hubcloud_link.get_attribute('href')}")
        download_url_hubcloud_link = hubcloud_link.get_attribute('href')
        time.sleep(20)

        result = fetch_dynamic_url(hubcloud_link.get_attribute('href'))
        print(f"The search URL found is: '{result}'")
        match = re.search(r'https?://[^\s]+', result)
        if match:
            result = match.group(0)
            print(f"Extracted URL: '{result}'")
            result = result.strip("'")
            result = result.rstrip()
            print(f"Cleaned URL: '{result}'")
        else:
            print("Error: No valid URL found in the result.")
            return  # Exit if no valid URL was found

        if result and result.endswith('='):
            print(f"Navigated to the dynamic URL: {result}")
            original_tab = driver.current_window_handle
            driver.switch_to.window(driver.window_handles[-1])  # Focus on the latest tab
            print("Switched to the new tab.")

            # Close all other tabs except the original HubCloud tab
            for handle in driver.window_handles:
                if handle != original_tab:
                    driver.switch_to.window(handle)
                    driver.close()
                    print(f"Closed tab: {handle}")

            # Switch back to the original HubCloud tab
            driver.switch_to.window(original_tab)
            driver.get(result)
            time.sleep(10)

        try:
            fsl_server_link = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Download [FSL Server]')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", fsl_server_link)
            time.sleep(5)  # Allow the browser to stabilize
            download_url = fsl_server_link.get_attribute("href")
            print(f"Clicked on download link: {download_url}")
            download_file_with_progress(download_url, "D:\\testing")
            print("Download completed")
            time.sleep(10)
            print(f"Returning URL: {hubcloud_link.get_attribute('href')}")
            # Return the required value
            return 1, download_url_hubcloud_link

        except Exception as e:
            print(f"Error clicking the download link: {e}")
            return 1, download_url_hubcloud_link
    except Exception as e:
        print(f"An error occurred: {e}")


def fetch_dynamic_url(url):
    driver = webdriver.Chrome()  # Ensure ki ChromeDriver properly configured hai
    driver.get(url)

    # Thodi der rukna, takki page completely load ho jaye
    time.sleep(20)  # Isse adjust karein based on page load time

    source_code = driver.page_source
    # Specific dynamic URL ko extract karne ke liye updated regular expression
    # pattern = r"var url = '(https://gamerxyt\.com/hubcloud\.php\?host=hubcloud&id=.*?&token=.*?);"
    pattern = r"var url = '(https://shetkaritoday\.in/hubcloud\.php\?host=hubcloud&id=.*?&token=.*?);"
    search_result = re.search(pattern, source_code)
    driver.quit()  # Driver ko band karein

    if search_result:
        dynamic_url = search_result.group(1)  # Group 1 se poora URL extract karna
        return f"Dynamic URL: {dynamic_url}"
    else:
        return "'var url' mein expected pattern nahi mila."

def download_images(driver, full_url):
    try:
        # Open the provided URL
        # return 1 , 'https://hubcloud.art/drive/11kjdffuiviahqi'
        driver.get(full_url)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        save_path = 'D:\\testing'
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        images = soup.find_all('img')
        for idx, img in enumerate(images, start=1):
            img_url = img.get('src')
            if img_url.startswith('/'):
                img_url = full_url + img_url
            try:
                img_data = requests.get(img_url).content
                if idx == 3:
                    file_name = 'poster.jpg'
                else:
                    file_name = f'image{idx}.jpg'
                with open(os.path.join(save_path, file_name), 'wb') as f:
                    f.write(img_data)
                    print(f"Downloaded {file_name} from {img_url}")
            except Exception as e:
                print(f"Failed to download {img_url}: {e}")

        # Wait for the first link to load
        link = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'https://howblogs')]"))
        )
        url = link.get_attribute('href')
        print(f"The URL is new and the things are: {url}")

        # Navigate to the new URL
        driver.get(url)

        # Try to find download links in a specific order: Streamtape, Indishare, Vidtube, Hubdrive
        try:
            # Check for streamtape link
            download_content = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'https://streamtape')]"))
            )
            download_url = download_content.get_attribute('href')
            print("Found link: streamtape")

        except Exception:
            print("Streamtape not found, checking Indishare...")

            try:
                # Check for Indishare link
                download_content = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'https://indishare')]"))
                )
                download_url = download_content.get_attribute('href')
                print("Found link: Indishare")

            except Exception:
                print("Indishare not found, checking Vidtube...")

                try:
                    # Check for Vidtube link
                    download_content = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'https://vidtube')]"))
                    )
                    download_url = download_content.get_attribute('href')
                    print("Found link: Vidtube")

                except Exception:
                    print("Vidtube not found, checking Hubdrive...")

                    try:
                        # Check for Hubdrive link
                        download_content = WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'https://hubdrive')]"))
                        )
                        download_url = download_content.get_attribute('href')
                        print("Found link: Hubdrive")

                    except Exception:
                        print("None of the expected links were found.")
                        download_url = None

        if download_url:
            print(f"Download link found: {download_url}")
            # Match based on the download service
            if "streamtape" in download_url:
             return   download_from_streamtape(driver, download_url)
            elif "vidtube" in download_url:
              return  download_from_vidtube(driver, download_url)
            elif "indishare" in download_url:
              return  download_from_indishare(driver, download_url)
            elif "hubdrive" in download_url:
              return  download_from_hubdrive(driver, download_url)
            else:
                print("Download link is from an unsupported service.")
        else:
            print("No valid download link found.")

    except Exception as e:
        print(f"An error occurred while processing the URL: {e}")


def download_images1_steemtape_downloads(driver, full_url):
    try:
        # Open the provided URL
        driver.get(full_url)

        # Parse the page and download images
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        save_path = 'D:\\testing'
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        images = soup.find_all('img')
        for idx, img in enumerate(images, start=1):
            img_url = img.get('src')
            if img_url.startswith('/'):
                img_url = full_url + img_url
            try:
                img_data = requests.get(img_url).content
                file_name = 'poster.jpg' if idx == 3 else f'image{idx}.jpg'
                with open(os.path.join(save_path, file_name), 'wb') as f:
                    f.write(img_data)
                    print(f"Downloaded {file_name} from {img_url}")
            except Exception as e:
                print(f"Failed to download {img_url}: {e}")

        # Extract and modify the video URL
        link = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'https://streamtape')]"))
        )
        original_url = link.get_attribute('href')
        print(f"Original URL: {original_url}")

        # Modify the URL to replace "v" with "e" and ensure domain suffix is ".com"
        modified_url = original_url.replace('.site', '.com').replace('/v/', '/e/')
        print(f"Modified URL: {modified_url}")

        # Navigate to the modified URL
        driver.get(modified_url)

        # Extract the direct video URL from the video tag
        time.sleep(5)  # Allow the page to load fully
        video_element = driver.find_element(By.TAG_NAME, 'video')
        video_url = video_element.get_attribute('src')
        print(f"Direct video URL: {video_url}")

        # Download the video
        video_response = requests.get(video_url, stream=True)
        video_path = os.path.join(save_path, 'downloaded_video.mp4')
        with open(video_path, 'wb') as video_file:
            for chunk in video_response.iter_content(chunk_size=1024):
                if chunk:
                    video_file.write(chunk)
        print(f"Video downloaded successfully as {video_path}")

    except Exception as e:
        print(f"An error occurred: {e}")
















