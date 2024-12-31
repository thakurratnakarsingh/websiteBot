from selenium import webdriver
import os
from dotenv import load_dotenv
import time
import requests


load_dotenv()

username = "ratnakarsingh@yopmail.com"
password = "Newy@rk2963"
apiKey = os.getenv('apiKey')
print("the credental is")
driver = webdriver.Chrome()
driver.get('https://thedataextractors.com/fast-captcha/')

user_field = driver.find_element('id', 'username')
pass_field = driver.find_element('id', 'password')

user_field.send_keys(username)
pass_field.send_keys(password);

url = "https://thedataextractors.com/fast-captcha/api/solve/recaptcha"
payload='webUrl=https://thedataextractors.com&websiteKey=6Lfur74oAAAAAHCXU97MyH0kgg0sx1uFnfJjs-B5'
headers = {
      'apiSecretKey': apiKey,
      'Content-Type': 'application/x-www-form-urlencoded'
}
response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)


solution = response.json()['solution'];
captcha_solution_element = driver.find_element('id', "g-recaptcha-response");
driver.execute_script("arguments[0].style.height = 'auto'; arguments[0].style.display = 'block';", captcha_solution_element);
captcha_solution_element.send_keys(solution);


pass_field.submit()

time.sleep(5)
driver.quit()



