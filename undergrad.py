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
    ElementClickInterceptedException,
    NoSuchFrameException
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
            print(f"Retry {i + 1}/{attempts} failed: {e}")
            time.sleep(1)


def safe_click(locator):
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(locator)).click()
    except (
            ElementNotInteractableException, NoSuchElementException, TimeoutException,
            ElementClickInterceptedException) as e:
        print(f"Error interacting with element: {e}")
        driver.save_screenshot(f"error_{locator[1]}.png")
        retry_click(locator)


# Function to remove files using the remove button
def remove_file(xpath):
    try:
        remove_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        remove_button.click()
        print(f"Successfully clicked remove button for XPath: {xpath}")
        time.sleep(2)  # Wait for the removal to complete
    except Exception as e:
        print(f"Error removing existing file for XPath {xpath}: {e}")
        capture_screenshot(f"remove_file_error_{xpath.replace('/', '_')}")


# DropzonePage class to handle file uploads
class DropzonePage:
    def __init__(self, driver):
        self.driver = driver

    def upload_file(self, dropzone_id, file_path):
        dropzone_form = (By.ID, dropzone_id)
        dropzone_message = (By.CLASS_NAME, "dz-message")

        # Wait until the dropzone is visible
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(dropzone_form)
        )

        # Click on the dropzone to open the file dialog
        dropzone = self.driver.find_element(*dropzone_form)
        dropzone.click()

        # Upload the file by sending the file path
        self.driver.find_element(By.CSS_SELECTOR, "input[type='file']").send_keys(file_path)

        # Optional: Wait for the upload to complete
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(dropzone_message)
        )
        print(f"File uploaded successfully to {dropzone_id}.")
        capture_screenshot(f"upload_success_{dropzone_id}.png")


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

# Ensure 'wizstep4' is clicked before proceeding
safe_click((By.ID, "wizstep5"))

# Dropdown selection function with improved waiting
def select_first_value(element_id, value):
    try:
        dropdown_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, element_id))
        )
        dropdown_element.click()

        # Wait until the dropdown options are fully loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//li[text()='{value}']"))
        )

        option_to_select = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//li[text()='{value}']"))
        )
        option_to_select.click()
    except WebDriverException as e:
        print(f"Error selecting value {value} for {element_id}: {e}")
        capture_screenshot(f"dropdown_error_{element_id}")


def select_matric_board():
    select_first_value("select2-matric_board-container", "BISE GUJRANWALA")
def select_matric_certificate():
    select_first_value("select2-matric_program-container", "S.S.C(Science)/ O-Level(Science) or equivalent ")
def select_matric_batchyear():
    select_first_value("select2-matric_batchyear-container", "1999")
def select_matric_passyear():
    select_first_value("select2-matric_passingyear-container", "2000")
def select_inter_board():
    select_first_value("select2-inter_board-container", "BISE GUJRANWALA")
def select_inter_passyear():
    select_first_value("select2-inter_passingyear-container", "2004")
def select_inter_certificate():
    select_first_value("select2-inter_program-container", "F.Sc Pre Engg")
def select_inter_batch():
    select_first_value("select2-inter_batchyear-container", "2001")

select_inter_batch()
select_inter_board()
select_matric_board()
select_inter_certificate()
select_matric_certificate()
select_matric_batchyear()
select_matric_passyear()
select_inter_passyear()

# Clear existing data before entering new percentages
matric_percentage_element = driver.find_element(By.ID, "matric_percentage")
matric_percentage_element.clear()
matric_percentage_element.send_keys("80.12")

inter_percentage_element = driver.find_element(By.ID, "inter_percentage")
inter_percentage_element.clear()
inter_percentage_element.send_keys("85.12")




# Remove files from different dropzones
xpaths = [
    '//*[@id="dropzoneMatricDMC"]/div[2]/a[1]',
    '//*[@id="dropzoneInterDMC"]/div[2]/a[1]',
    '//*[@id="dropzoneMatricCertificate"]/div[2]/a[1]',
    '//*[@id="dropzoneInterCertificate"]/div[2]/a[1]'
]

for xpath in xpaths:
    remove_file(xpath)

# Upload files using the DropzonePage class
dropzone_page = DropzonePage(driver)
dropzone_page.upload_file("dropzoneMatricDMC", r"F:\1pec\test data\Test  data pec\1.jpeg")  # Profile
dropzone_page.upload_file("dropzoneInterDMC", r"F:\1pec\test data\Test  data pec\1.jpeg")  # CNIC2
dropzone_page.upload_file("dropzoneMatricCertificate", r"F:\1pec\test data\Test  data pec\1.jpeg")  # Signature
dropzone_page.upload_file("dropzoneInterCertificate", r"F:\1pec\test data\Test  data pec\1.jpeg")  # CNIC

driver.implicitly_wait(10)
# Click the submit button
retry_click((By.ID, "btnSubmitUndergradDetails"))
driver.implicitly_wait(4)

# Handling modal dialog
retry_click((By.XPATH, "/html/body/div[6]/div[7]/button[2]"))
retry_click((By.XPATH, "//*[@id='undergrad-modal']/div/div/div[3]/button[4]"))

# Perform assertion after clicking the modal button
try:
    # Wait for the interview modal to appear
    header_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="grad-modal"]/div/div/div[1]/h4'))
    )

    # Assert that the header text matches the expected value
    expected_text = "Qualification Details"  # Replace with actual expected text
    actual_text = header_element.text
    assert actual_text == expected_text, f"Assertion failed: Expected '{expected_text}', but got '{actual_text}'"
    print("Assertion passed: Header text is correct.")
except Exception as e:
    print(f"Error during assertion or modal handling: {e}")
    capture_screenshot("assertion_error")

# Close the browser
driver.quit()
