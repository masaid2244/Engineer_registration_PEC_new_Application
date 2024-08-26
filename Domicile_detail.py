import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException, ElementNotInteractableException, TimeoutException,
    WebDriverException, NoAlertPresentException, ElementClickInterceptedException
)
from webdriver_manager.chrome import ChromeDriverManager

# Setup Chrome WebDriver
chrome_service = ChromeService(ChromeDriverManager().install())
chrome_options = Options()
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Function to capture screenshots with unique filenames
def capture_screenshot(filename):
    try:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        full_filename = f"{filename}_{timestamp}.png"
        driver.get_screenshot_as_file(full_filename)
        print(f"Screenshot saved as {full_filename}")
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
        capture_screenshot(f"clicked_{locator[1]}")
    except ElementClickInterceptedException:
        print(f"Element click intercepted for locator {locator}.")
        driver.execute_script("arguments[0].click();", driver.find_element(*locator))
        print(f"Successfully clicked element with locator {locator} using JavaScript.")
        capture_screenshot(f"clicked_{locator[1]}_js")
    except Exception as e:
        print(f"Error clicking element with locator {locator}: {e}")
        capture_screenshot(f"click_error_{locator[1]}")

# Function to retry clicking an element
def retry_click(locator, attempts=3):
    for i in range(attempts):
        try:
            scroll_and_click(locator)
            break
        except Exception as e:
            print(f"Retry {i + 1}/{attempts} failed: {e}")
            time.sleep(1)

# Function to safely click an element with error handling
def safe_click(locator):
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(locator)).click()
    except (
    ElementNotInteractableException, NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
        print(f"Error interacting with element: {e}")
        capture_screenshot(f"error_{locator[1]}")

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

# Functions to interact with dropdowns
def select_country():
    select_first_value("select2-domiciledetails_country-container", "Pakistan")

def select_province():
    select_first_value("select2-domiciledetails_province-container", "Punjab")

def select_district():
    select_first_value("select2-domiciledetails_district-container", "BAHAWALNAGAR")

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
safe_click((By.ID, "wizstep3"))

# Interact with dropdowns
select_country()
select_province()
select_district()

# Fill in the address field
element_address = driver.find_element(By.ID, "domiciledetails_address")
element_address.send_keys("abcd efg123")

# Remove existing file from the frame before uploading a new one
try:
    remove_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="dropzoneDomicile"]/div[2]/a[1]'))
    )
    remove_button.click()
    print("Existing file removed.")
    time.sleep(2)  # Wait for removal to complete
except Exception as e:
    print(f"Error removing existing file: {e}")
    capture_screenshot("remove_file_error")

# Handle file upload directly without switching to a frame
try:
    upload_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "dropzoneDomicile"))
    )
    upload_element.send_keys("F:/1pec/test data/SampleJPGImage_1mbmb.jpg")
    print("New file uploaded.")
except Exception as e:
    print(f"Error uploading file: {e}")
    capture_screenshot("upload_file_error")

# Click the submit button
driver.implicitly_wait(5)
retry_click((By.ID, "btnSubmitDomicileDetails"))
retry_click((By.XPATH, "/html/body/div[6]/div[7]/button[2]"))
retry_click((By.XPATH,"//*[@id='domicile-modal']/div/div/div[3]/button[3]"))

# Perform assertion after clicking the modal button
try:
    # Wait for the interview modal to appear
    header_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="Interview-modal"]/div/div/div[1]/h4'))
    )

    # Assert that the header text matches the expected value
    expected_text = "Assessment/Interview Details"  # Replace with actual expected text
    actual_text = header_element.text
    assert actual_text == expected_text, f"Assertion failed: Expected '{expected_text}', but got '{actual_text}'"
    print("Assertion passed: Header text is correct.")
except Exception as e:
    print(f"Error during assertion or modal handling: {e}")
    capture_screenshot("assertion_error")

# Minimize the browser window
driver.minimize_window()

# Close the browser
driver.quit()
