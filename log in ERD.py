import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


# Setup Chrome WebDriver
chrome_service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=chrome_service)

driver.get("https://portal.pec.org.pk/")
driver.maximize_window()

element_signin = driver.find_element(By.LINK_TEXT, "Sign In")
element_signin.click()

element_username = driver.find_element(By.ID, "username")
element_username.send_keys("pectesting12345@gmail.com")

element_password = driver.find_element(By.ID, "password")
element_password.send_keys("pec123")

# driver.find_element(By.ID, "btn-login").click()

element_signin_button = driver.find_element(By.ID, "btn-login")
element_signin_button.click()
time.sleep(5)
# driver.minimize_window()

driver.quit()

