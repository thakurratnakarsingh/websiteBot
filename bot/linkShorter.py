import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException



def LinkShorterMaking(driver, full_url):
    try:
        # return "https://adrinolinks.com/XeuY5"
        print("Download function working with input:", full_url)
        # Close all tabs except the original one
        original_tab = driver.current_window_handle
        for handle in driver.window_handles:
            if handle != original_tab:
                driver.switch_to.window(handle)
                driver.close()
                print(f"Closed tab: {handle}")
        driver.switch_to.window(original_tab)
        # Navigate to the target URL Login
        driver.get("https://adrinolinks.in/auth/signin")
        time.sleep(5)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        username_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_field.send_keys("thakursingh294r")
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys("Newy@rk2963")
        remember_me = driver.find_element(By.ID, "remember-me")
        if not remember_me.is_selected():
            remember_me.click()
        try:
             WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "cookie-message"))
            )
        except TimeoutException:
            print("Cookie message still visible. Attempting to close it...")
            cookie_accept_button = driver.find_element(By.XPATH, "//button[text()='Got it!']")
            cookie_accept_button.click()
        login_button = driver.find_element(By.ID, "invisibleCaptchaSignin")
        driver.execute_script("arguments[0].scrollIntoView();", login_button)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "invisibleCaptchaSignin")))
        login_button.click()
        print("Waiting for '+ New Shorten Link' button to be clickable...")
        new_shorten_link_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@class='btn btn-block btn-social btn-github btn-lg shorten-button']")
            )
        )
        driver.execute_script("arguments[0].scrollIntoView();", new_shorten_link_button)
        new_shorten_link_button.click()
        print("Clicked the '+ New Shorten Link' button successfully!")
        print("Entering URL into the input field...")
        url_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "url"))
        )
        url_input.send_keys(full_url)
        print("URL entered successfully.")
        print("Waiting for the 'Shorten' button to be clickable...")
        shorten_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@class='btn btn-submit btn-primary btn-xs']")
            )
        )
        shorten_button.click()
        print("Clicked the 'Shorten' button successfully!")
        copy_icon = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "copy-it"))
        )
        shortened_url = copy_icon.get_attribute("data-clipboard-text")
        print(f"Shortened URL: {shortened_url}")
        print("Login successful!")
        return shortened_url
    except TimeoutException as e:
        print("TimeoutException: Element not found within the wait time:", str(e))
    except Exception as e:
        print("An unexpected error occurred:", str(e))
