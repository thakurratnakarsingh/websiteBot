import os
import time
import pyautogui
import subprocess
from selenium.webdriver.common.by import By
import pyperclip

def get_dynamic_data(driver):
    try:
        # Extract film name
        film_name_element = driver.find_element(By.CSS_SELECTOR, "div.Robiul b")
        film_name = film_name_element.text.split(' (')[0]  # This will get the part before the year

        # Extract stars (correct extraction of the artist name)
        stars_element = driver.find_element(By.XPATH, "//div[@class='Let'][b[contains(text(),'Stars :')]]/b")
        stars = stars_element.text.replace("Stars : ", "").strip()  # Get only the artist names without "Stars : "

        return film_name, stars
    except Exception as e:
        print(f"Error extracting dynamic data: {e}")
        return None, None


def fileIsDownloadedNowUpload(driver, full_url, short_url):
    try:
        # Close any extra tabs and switch back to the main one
        original_tab = driver.current_window_handle
        for handle in driver.window_handles:
            if handle != original_tab:
                driver.switch_to.window(handle)
                driver.close()
                print(f"Closed tab: {handle}")
        driver.switch_to.window(original_tab)

        # Open the full URL and extract data
        driver.get(full_url)
        print("Opening the full URL:", short_url)
        film_name, stars = get_dynamic_data(driver)
        if not film_name or not stars:
            print("Failed to extract dynamic data.")
            return

        # Construct the dynamic message
        message = f"""
🔞🚱{film_name} 🎥📹
💽🔴N/A
______
💽🔴Stars : {stars}
______
Download Link
{short_url}
______
Demo Link

______
Monthly : 70 Rs,
Six month : 300 Rs,
Yearly : 500 Rs,
Lifetime : 800 Rs,

➖➖➖➖➖➖➖➖➖➖➖➖
Admin : @moons_fans
"""
        print("Generated message:\n", message)

        # Check if Telegram Desktop is already running
        telegram_title_found = False
        for attempt in range(10):  # Retry for up to 10 seconds
            active_window = pyautogui.getActiveWindowTitle()
            if active_window and "Telegram" in active_window:
                telegram_title_found = True
                print("Telegram Desktop is already active.")
                break
            time.sleep(1)

        # If Telegram Desktop is not open, launch it
        if not telegram_title_found:
            print("Launching Telegram Desktop...")
            telegram_path = r'C:\Users\Ratnakar Singh PC\AppData\Roaming\Telegram Desktop\Telegram.exe'
            if not os.path.exists(telegram_path):
                raise FileNotFoundError(f"Telegram.exe not found at {telegram_path}")
            subprocess.Popen(telegram_path)

            # Wait for Telegram Desktop to open
            for attempt in range(10):
                active_window = pyautogui.getActiveWindowTitle()
                if active_window and "Telegram" in active_window:
                    print("Telegram Desktop is now active.")
                    break
                time.sleep(1)
            else:
                raise TimeoutError("Telegram Desktop did not open.")

        # Focus on Telegram and search for the contact/channel
        print("Searching for 'testing material'...")
        pyautogui.hotkey("ctrl", "k")  # Open the search bar
        time.sleep(1)
        pyautogui.typewrite("testing material")
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)

        # Attach the image
        print("Attaching the image...")
        image_path = r"D:\testing\poster.jpg"
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at {image_path}")

        pyautogui.hotkey("ctrl", "o")  # Open the file attachment dialog
        time.sleep(2)
        pyautogui.typewrite(image_path)  # Enter the file path
        pyautogui.press("enter")  # Confirm attachment
        time.sleep(5)  # Wait for the image to attach

        # Paste the message as a caption
        print("Sending the message with the image...")
        pyperclip.copy(message)  # Copy the message to clipboard
        pyautogui.hotkey("ctrl", "v")  # Paste the message
        time.sleep(2)
        pyautogui.press("enter")  # Send the message with the image
        print("Image and message sent successfully.")
        return 1
    except FileNotFoundError as fnf:
        print("File not found:", str(fnf))
        return 0
    except TimeoutError as te:
        print("Timeout error:", str(te))
        return 0
    except Exception as e:
        print("An unexpected error occurred:", str(e))
        return 0