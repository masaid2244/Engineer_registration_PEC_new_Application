import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException, WebDriverException, NoAlertPresentException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager

# Setup Chrome WebDriver
chrome_service = ChromeService(ChromeDriverManager().install())
chrome_options = Options()
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Function to capture screenshots
def capture_screenshot(filename):
    try:
        driver.get_screenshot_as_file(filename)
        print(f"Screenshot saved as {filename}")
    except Exception as e:
        print(f"Error capturing screenshot: {e}")

# Function to scroll to the element and click
def scroll_and_click(locator):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(locator)
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(locator)).click()
        print(f"Successfully clicked element with locator {locator}.")
        capture_screenshot(f"clicked_{locator[1]}.png")
    except ElementClickInterceptedException:
        print(f"Element click intercepted for locator {locator}.")
        driver.execute_script("arguments[0].click();", driver.find_element(*locator))
        print(f"Successfully clicked element with locator {locator} using JavaScript.")
        capture_screenshot(f"clicked_{locator[1]}_js.png")
    except Exception as e:
        print(f"Error clicking element with locator {locator}: {e}")
        capture_screenshot(f"click_error_{locator[1]}.png")

# Function to retry clicking an element
def retry_click(locator, attempts=3):
    for i in range(attempts):
        try:
            scroll_and_click(locator)
            break
        except Exception as e:
            print(f"Retry {i+1}/{attempts} failed: {e}")
            time.sleep(1)

def safe_click(locator):
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(locator)).click()
    except (ElementNotInteractableException, NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
        print(f"Error interacting with element: {e}")
        driver.save_screenshot(f"error_{locator[1]}.png")

# Start the browser and navigate to the page
driver.get("http://10.0.32.90:8012/")
driver.maximize_window()

# Perform login
element_signin = driver.find_element(By.LINK_TEXT, "Sign In")
element_signin.click()

element_username = driver.find_element(By.ID, "username")
element_username.send_keys("pectesting12345@gmail.com")

element_password = driver.find_element(By.ID, "password")
element_password.send_keys("pec123")

element_signin_button = driver.find_element(By.ID, "btn-login")
element_signin_button.click()

# Ensure 'wizstep2' is clicked before proceeding
safe_click((By.ID, "wizstep2"))

# Dropdown selection function
def select_first_value(element_id, value):
    try:
        dropdown_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, element_id))
        )
        dropdown_element.click()
        option_to_select = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//li[text()='{value}']"))
        )
        option_to_select.click()
    except WebDriverException as e:
        print(f"Error selecting value {value} for {element_id}: {e}")
        capture_screenshot(f"dropdown_error_{element_id}.png")

# Functions to interact with dropdowns
def select_country():
    select_first_value("select2-mailingdetails_country-container", "Pakistan")

def select_province():
    select_first_value("select2-mailingdetails_province-container", "Punjab")

def select_district():
    select_first_value("select2-mailingdetails_district-container", "BAHAWALNAGAR")

def select_city():
    select_first_value("select2-mailingdetails_city-container", "CHISHTIAN")

# Interact with dropdowns
select_country()
select_province()
select_district()
select_city()

# Fill in the address field
element_address = driver.find_element(By.ID, "mailingdetails_address")
element_address.send_keys("abcdefg absdg ghs shs ")

# Click the submit button
retry_click((By.ID, "btnSubmitMailingDetails"))

# Handle any alert or pop-up
def handle_alert():
    try:
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()  # Use alert.dismiss() if you want to cancel
        print("Alert accepted.")
    except NoAlertPresentException:
        print("No alert present.")
    except Exception as e:
        print(f"Error handling alert: {e}")
        capture_screenshot("alert_error.png")

# Wait and handle possible alerts
handle_alert()

# Click the 'OK' button after form submission if it is a modal dialog
def handle_modal():
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'confirm') and text()='OK']"))).click()
        print("Modal 'OK' button clicked.")
    except NoSuchElementException:
        print("OK button not found.")
    except Exception as e:
        print(f"Error handling modal: {e}")

# Wait and handle possible modals
handle_modal()

# Ensure 'wizstep3' is clicked before proceeding
# safe_click((By.ID, "wizstep3"))

# Close
driver.quit()
