import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

# Setup Chrome WebDriver
chrome_service = ChromeService(ChromeDriverManager().install())
chrome_options = Options()
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)


# Function to select a value from a dropdown
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


# Function to handle modal alerts
def handle_modal_alert():
    try:
        modal_ok_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[6]/div[7]/button[2]"))
        )
        modal_ok_button.click()
        print("Successfully clicked the OK button on the modal alert.")
        capture_screenshot("modal_alert_ok_clicked.png")
        time.sleep(2)  # Wait for the alert to disappear
    except TimeoutException:
        print("No modal alert found to handle.")
    except Exception as e:
        print(f"Error handling modal alert: {e}")
        capture_screenshot("modal_alert_error.png")


# Function to upload file
def wait_and_upload_file(input_id, file_path):
    try:
        input_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, input_id))
        )
        input_element.send_keys(file_path)
        print(f"File uploaded successfully to {input_id}.")
    except Exception as e:
        print(f"Error uploading file: {e}")
        capture_screenshot(f"upload_error_{input_id}.png")


# Function to capture a screenshot
def capture_screenshot(filename):
    try:
        if not filename.endswith(".png"):
            filename += ".png"
        driver.get_screenshot_as_file(filename)
        print(f"Screenshot saved as {filename}")
    except Exception as e:
        print(f"Error capturing screenshot: {e}")


# Function to remove files using the remove button
def remove_file(xpath):
    try:
        remove_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", remove_button)
        remove_button.click()
        print(f"Successfully clicked remove button for XPath: {xpath}")
        time.sleep(2)
    except Exception as e:
        print(f"Error removing existing file for XPath {xpath}: {e}")
        capture_screenshot(f"remove_file_error_{xpath.replace('/', '_')}")


# Function to clear the value and then set a new value
def clear_and_set_value(element, value):
    try:
        element.clear()
        time.sleep(1)  # Small delay to ensure the field is cleared
        element.send_keys(value)
        print(f"Successfully set value '{value}' in element {element.get_attribute('id')}.")
    except Exception as e:
        print(f"Error setting value '{value}' in element {element.get_attribute('id')}: {e}")
        capture_screenshot(f"set_value_error_{element.get_attribute('id')}.png")


# Function to scroll to the element and click it
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


# Function to wait for an overlay to disappear
def wait_for_overlay_to_disappear():
    try:
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, ".sweet-overlay"))
        )
        print("Overlay has disappeared.")
    except TimeoutException:
        print("Timeout: Overlay did not disappear within the given time.")
        capture_screenshot("overlay_timeout_error.png")


# Function to click the save button once
def click_save_button(locator):
    try:
        wait_for_overlay_to_disappear()
        WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(locator)
        ).click()
        print("clicking save button ?????.")
        time.sleep(2)

        success_message_locator = (By.CSS_SELECTOR, ".success-message")
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located(success_message_locator)
        )
        print("Save action successful.")
    except ElementClickInterceptedException:
        print("ElementClickInterceptedException: Save button click was intercepted.")
        capture_screenshot("save_button_intercepted.png")
    except Exception as e:
        print(f"Error clicking save button: {e}")
        capture_screenshot("save_button_error.png")


# Function to select bank from dropdown
def select_bank():
    select_first_value("select2-challan_bank-container", "Alfalah")


xpaths = [
    '//*[@id="dropzoneChallan"]/div[2]/a[1]',
    # Add other XPaths if needed
]

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

# Ensure 'wizstep7' is clicked before proceeding
scroll_and_click((By.ID, "wizstep7"))

scroll_and_click((By.XPATH, "//*[@id='challan-modal']/div/div/div[2]/div[3]/div[2]/span"))

select_bank()

challan_docno = driver.find_element(By.ID, "challan_docno")
clear_and_set_value(challan_docno, "01589886")

challan_field = driver.find_element(By.ID, "challan_date")
clear_and_set_value(challan_field, "10-Aug-2024")

amount = driver.find_element(By.ID, "challan_amount")
clear_and_set_value(amount, "5500")

for xpath in xpaths:
    remove_file(xpath)

# Wait for and upload the file
wait_and_upload_file("//*[@id='dropzoneChallan']", r"F:\1pec\test data\Test  data pec\download (1).jpg")

# Remove file if necessary
for xpath in xpaths:
    remove_file(xpath)

# Click save button or any other button to submit
try:
    grad_details_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "btnSubmitChallanDetails"))
    )
    grad_details_button.click()
    print("YES, TEST CASE PASSED")
except Exception as e:
    print(f"Failed to click 'btnSubmitChallanDetails' button: {e}")
    capture_screenshot("btnSubmitChallanDetails_error.png")

driver.close()
