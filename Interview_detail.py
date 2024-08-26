import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotInteractableException,
    TimeoutException,
    WebDriverException,
    ElementClickInterceptedException
)
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
        retry_click(locator)

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
driver.implicitly_wait(5)

# Ensure 'wizstep2' is clicked before proceeding
safe_click((By.ID, "wizstep3a"))

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

# File upload function
def upload_file(input_id, file_path):
    absolute_path = os.path.abspath(file_path)
    if os.path.exists(absolute_path):
        print(f"Uploading file from path: {absolute_path}")
        try:
            driver.find_element(By.ID, input_id).send_keys(absolute_path)
            print(f"File uploaded successfully to {input_id}.")
        except Exception as e:
            print(f"Error uploading file: {e}")
            capture_screenshot(f"upload_error_{input_id}.png")
    else:
        print(f"File does not exist at path: {absolute_path}. Please check the file path.")

# Uploading files
upload_file("upload_file", r"F:\1pec\test data\Test  data pec\1.5mb.pdf")
upload_file("expupload_file", r"F:\1pec\test data\Test  data pec\1.5mb.pdf")

# Click the submit button
retry_click((By.ID, "btnSubmitInterviewDetail"))
driver.implicitly_wait(4)

# Handling modal dialog
retry_click((By.XPATH, "/html/body/div[6]/div[7]/button[2]"))
retry_click((By.XPATH, "//*[@id='Interview-modal']/div/div/div[3]/button[3]"))

# Perform assertion after clicking the modal button
try:
    # Wait for the interview modal to appear
    header_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="documents-modal"]/div/div/div[1]/h4'))
    )

    # Assert that the header text matches the expected value
    expected_text = "Uploading of Documents"  # Replace with actual expected text
    actual_text = header_element.text
    assert actual_text == expected_text, f"Assertion failed: Expected '{expected_text}', but got '{actual_text}'"
    print("Assertion passed: Header text is correct.")
except Exception as e:
    print(f"Error during assertion or modal handling: {e}")
    capture_screenshot("assertion_error")


# Close the browser
driver.quit()
