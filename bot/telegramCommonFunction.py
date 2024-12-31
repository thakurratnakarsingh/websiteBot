from selenium.webdriver.common.by import By
import psutil
import pyperclip
import os
import time
import pyautogui
import pygetwindow as gw
import subprocess
import shutil
import ctypes

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

def close_telegram():
    """Closes Telegram Desktop if it is running."""
    for process in psutil.process_iter(attrs=['name']):
        if process.info['name'] == "Telegram.exe":
            process.terminate()
            print("Telegram Desktop has been closed.")
            return True
    print("Telegram Desktop is not running.")
    return False

def send_message_to_channel(channel_name, message, image_path):
    try:
        # Focus on the Telegram window
        focus_telegram_window()
        time.sleep(1)
        print(f"Searching for '{channel_name}'...")
        pyautogui.hotkey("ctrl", "k")  # Open the search bar
        time.sleep(1)
        pyautogui.typewrite(channel_name)
        time.sleep(2)
        pyautogui.press("enter")
        time.sleep(2)
        print(f"Attaching the image for '{channel_name}'...")
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at {image_path}")

        pyautogui.hotkey("ctrl", "o")  # Open the file attachment dialog
        time.sleep(2)
        pyautogui.typewrite(image_path)  # Enter the file path
        pyautogui.press("enter")  # Confirm attachment
        time.sleep(5)  # Wait for the image to attach


        # Paste the message as a caption
        print(f"Sending the message to '{channel_name}'...")
        pyperclip.copy(message)  # Copy the message to clipboard
        pyautogui.hotkey("ctrl", "v")  # Paste the message
        time.sleep(2)
        pyautogui.press("enter")  # Send the message with the image
        print(f"Message sent successfully to '{channel_name}'.")
        print(f"Ensuring focus is reset for Telegram after sending message to '{channel_name}'...")
        time.sleep(10)
        close_telegram()

    except Exception as e:
        print(f"An error occurred while sending message to '{channel_name}': {e}")

def openTelegramInPC():
    """
    Opens Telegram Desktop if it is not already active. Verifies the active window title
    to ensure Telegram is running.
    """
    telegram_title_found = False

    # Check if Telegram is already active
    for attempt in range(10):  # Retry for up to 10 seconds
        active_window = pyautogui.getActiveWindowTitle()
        if active_window and "Telegram" in active_window:
            telegram_title_found = True
            print("Telegram Desktop is already active.")
            break
        time.sleep(1)

    if not telegram_title_found:
        print("Launching Telegram Desktop...")
        telegram_path = r'C:\Users\Ratnakar Singh PC\AppData\Roaming\Telegram Desktop\Telegram.exe'

        # Verify if Telegram exists at the specified path
        if not os.path.exists(telegram_path):
            raise FileNotFoundError(f"Telegram.exe not found at {telegram_path}")

        subprocess.Popen(telegram_path, shell=True)

        # Wait for Telegram to launch
        for attempt in range(10):
            focus_telegram_window()
            active_window = pyautogui.getActiveWindowTitle()
            if active_window and "Telegram" in active_window:
                print("Telegram Desktop is now active.")
                break
            time.sleep(1)
        else:
            raise TimeoutError("Telegram Desktop did not open.")

def focus_telegram_window():
    """Bring the Telegram Desktop window to the foreground."""
    telegram_windows = [win for win in gw.getWindowsWithTitle("Telegram") if not win.isMinimized]
    if telegram_windows:
        telegram_windows[0].activate()
        print("Telegram window activated.")
    else:
        print("Telegram window not found. Please ensure Telegram is running.")

def send_pre_message_to_channel(channel_name, message, image_path, video_message, film_name):
    try:
        focus_telegram_window()
        time.sleep(1)
        print(f"Searching for '{channel_name}'...")
        pyautogui.hotkey("ctrl", "k")  # Open the search bar
        time.sleep(10)
        pyautogui.typewrite(channel_name)
        time.sleep(10)
        pyautogui.press("enter")
        time.sleep(2)
        print(f"Attaching the image for '{channel_name}'...")
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at {image_path}")

        pyautogui.hotkey("ctrl", "o")  # Open the file attachment dialog
        time.sleep(2)
        pyautogui.typewrite(image_path)  # Enter the file path
        pyautogui.press("enter")  # Confirm attachment
        time.sleep(5)  # Wait for the image to attach

        # Paste the message as a caption
        print(f"Sending the message to '{channel_name}'...")
        pyperclip.copy(message)  # Copy the message to clipboard
        pyautogui.hotkey("ctrl", "v")  # Paste the message
        time.sleep(2)
        pyautogui.press("enter")  # Send the message with the image
        print(f"Message sent successfully to '{channel_name}'.")
        print(f"Ensuring focus is reset for Telegram after sending message to '{channel_name}'...")

        # Focus on the Telegram window
        image_folder_path = r"D:\testing"
        # Attach multiple images
        print(f"Attaching images for '{channel_name}'...")
        image_files = ["image4.jpg", "image5.jpg", "image6.jpg", "image7.jpg"]
        for image_file in image_files:
            image_path = os.path.join(image_folder_path, image_file)
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image not found at {image_path}")
            # Attach the image
            pyautogui.hotkey("ctrl", "o")  # Open the file attachment dialog
            time.sleep(2)
            pyautogui.typewrite(image_path)  # Enter the file path
            pyautogui.press("enter")  # Confirm attachment
            time.sleep(3)  # Wait for the image to attach
        print(f"All images attached successfully for '{channel_name}'.")
        pyautogui.press("enter")
        print(f"Message and all images sent successfully to '{channel_name}'.")
        time.sleep(5)

        # Find the video file and rename it
        video_extensions = [".mp4", ".avi", ".mov", ".mkv"]
        video_file = None
        for file in os.listdir(image_folder_path):
            if any(file.lower().endswith(ext) for ext in video_extensions):
                video_file = os.path.join(image_folder_path, file)
                break

        if video_file:
            # Get the original extension of the video file
            original_extension = os.path.splitext(video_file)[1]
            # Construct the new video file name with the original extension
            new_video_path = os.path.join(image_folder_path, film_name + original_extension)
            os.rename(video_file, new_video_path)
            print(f"Renamed video file from '{video_file}' to '{new_video_path}'.")

            # Attach and send the renamed video
            print(f"Attaching the video '{new_video_path}'...")
            pyautogui.hotkey("ctrl", "o")  # Open the file attachment dialog
            time.sleep(2)
            pyautogui.typewrite(new_video_path)  # Enter the file path
            pyautogui.press("enter")  # Confirm attachment
            time.sleep(5)  # Wait for the video to attach
            # Paste the message as a caption
            pyperclip.copy(video_message)  # Copy the message to clipboard
            pyautogui.hotkey("ctrl", "v")  # Paste the message
            time.sleep(2)
            pyautogui.press("enter")
            time.sleep(300)
            close_telegram()

            # try:
            #     res = is_video_uploaded()
            #     if res:
            #         close_telegram()
            #         print("Video and message sent successfully.")
            # except Exception as e:
            #     print(f"An error occurred: {e}")
        else:
            print("No video file found in the specified folder.")

        # Finalize by pressing Enter to send the message with all attachments
        pyautogui.press("enter")
        print(f"Message, images, and video sent successfully to '{channel_name}'.")
        time.sleep(10)

    except Exception as e:
        print(f"An error occurred while sending message to '{channel_name}': {e}")

def clear_directory_and_recycle_bin(path):
    try:
        if not os.path.exists(path):
            print(f"The path {path} does not exist.")
            return

        # Delete all files and folders in the directory
        print(f"Clearing all files and folders from {path}...")
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)  # Delete files and symbolic links
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Delete directories

        print(f"All files and folders in {path} have been deleted.")

        # Clear the Recycle Bin
        print("Clearing the Recycle Bin...")
        result = ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 3)
        if result == 0:
            print("Recycle Bin cleared successfully.")
        else:
            print(f"An error occurred while clearing the Recycle Bin. Error code: {result}")
    except Exception as e:
        print(f"An error occurred: {e}")

def is_video_uploaded():
    while True:
        region = pyautogui.locateOnScreen('uploading_indicator.png', confidence=0.8)
        if not region:
            print("Upload complete!")
            return True
        else:
            print("Video is still uploading...")
        time.sleep(5)



