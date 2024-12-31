import time
from telegramCommonFunction import get_dynamic_data ,send_message_to_channel, openTelegramInPC,send_pre_message_to_channel

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
https://t.me/+VCMVDx-ijxFlODdl
______
Monthly : 50 Rs,
Three month : 100 Rs,
Six month : 150 Rs,
Yearly : 200 Rs,
Lifetime : 300 Rs,

➖➖➖➖➖➖➖➖➖➖➖➖
Admin : @johnny_fans
"""
        messagePre = f"""
🔞🚱{film_name} 🎥📹
💽🔴N/A
______
💽🔴Stars : {stars}
______
Download Now 👇👇
"""

        messageContent = f"""
🔞🚱{film_name} 🎥📹
💽🔴N/A
        """
        print("Generated message:\n", message)
        openTelegramInPC()
        image_path = r"D:\testing\poster.jpg"
        send_message_to_channel("Feni | Dugru | Ullu", message, image_path)
        time.sleep(5)
        openTelegramInPC()
        time.sleep(10)
        send_message_to_channel("Prime Xtream | CineOn | Jalsa Tv", message, image_path)
        time.sleep(5)
        openTelegramInPC()
        time.sleep(10)
        send_message_to_channel("NeonX | LookEnt | IBAMovies", message, image_path)
        time.sleep(5)
        openTelegramInPC()
        time.sleep(10)
        send_message_to_channel("MeetX | NavaRasa| MakhanApp", message, image_path)
        time.sleep(5)
        openTelegramInPC()
        time.sleep(10)
        send_message_to_channel("Resmi Nair | Poonam Panday | LavaOTT", message, image_path)
        time.sleep(10)
        openTelegramInPC()
        send_message_to_channel("Show Hit | WebSX | Sigma", message, image_path)
        time.sleep(5)
        openTelegramInPC()
        time.sleep(10)
        send_message_to_channel("MoodX | RioPlus | HulChul", message, image_path)
        time.sleep(5)
        openTelegramInPC()
        time.sleep(10)
        send_message_to_channel("Xtreme | Triflicks | BoomEX", message, image_path)
        time.sleep(10)
        # openTelegramInPC()
        # send_message_to_channel("MeetX | NavaRasa| MakhanApp", message, image_path)
        # time.sleep(10)
        openTelegramInPC()
        send_pre_message_to_channel("Adult Webseries Premium" ,messagePre, image_path, messageContent,film_name)
        time.sleep(10)
        print("All messages sent successfully.")
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




