import time
import random
import string
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Generate random string (for email & password)
def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

# Get OTP from 1secmail inbox
def get_otp(email_prefix, domain="1secmail.com"):
    print("[*] Waiting for OTP email...")
    for i in range(20):  # Wait for up to ~60 seconds
        inbox = requests.get(f"https://www.1secmail.com/api/v1/?action=getMessages&login={email_prefix}&domain={domain}").json()
        if inbox:
            msg_id = inbox[0]['id']
            msg = requests.get(f"https://www.1secmail.com/api/v1/?action=readMessage&login={email_prefix}&domain={domain}&id={msg_id}").json()
            body = msg.get("body", "")
            otp = ''.join(filter(str.isdigit, body))[:6]
            return otp
        time.sleep(3)
    return None

# Set up headless browser options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Setup Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Generate email and password
email_prefix = generate_random_string()
email = f"{email_prefix}@1secmail.com"
password = generate_random_string(12)

# Open Twitter signup page
driver.get("https://twitter.com/i/flow/signup")
time.sleep(5)

# Fill in the signup form
inputs = driver.find_elements(By.TAG_NAME, "input")
inputs[0].send_keys("John Test")  # Name
driver.find_element(By.XPATH, '//span[text()="Use email instead"]').click()
time.sleep(1)
inputs = driver.find_elements(By.TAG_NAME, "input")
inputs[1].send_keys(email)  # Email

# Set birth date
driver.find_element(By.XPATH, '//select[@id="SELECTOR_1"]').send_keys("May")
driver.find_element(By.XPATH, '//select[@id="SELECTOR_2"]').send_keys("13")
driver.find_element(By.XPATH, '//select[@id="SELECTOR_3"]').send_keys("2000")

# Click Next buttons
driver.find_element(By.XPATH, '//span[text()="Next"]').click()
time.sleep(1)
driver.find_element(By.XPATH, '//span[text()="Next"]').click()
time.sleep(1)
driver.find_element(By.XPATH, '//span[text()="Sign up"]').click()

# Wait for OTP
otp = get_otp(email_prefix)
if otp:
    print(f"\n[+] OTP Received: {otp}")
    driver.find_element(By.TAG_NAME, "input").send_keys(otp)
    driver.find_element(By.XPATH, '//span[text()="Next"]').click()
else:
    print("[!] OTP not received in time. Try again.")
    driver.quit()
    exit()

# Set password
time.sleep(3)
inputs = driver.find_elements(By.TAG_NAME, "input")
inputs[0].send_keys(password)
driver.find_element(By.XPATH, '//span[text()="Next"]').click()

# Done
print("\n[+] Account Created!")
print(f"Email: {email}")
print(f"Password: {password}")

# Close the browser
time.sleep(10)
driver.quit()
