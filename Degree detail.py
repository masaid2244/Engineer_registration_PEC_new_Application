import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager

# Setup Chrome WebDriver
chrome_service = ChromeService(ChromeDriverManager().install())
chrome_options = Options()
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

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

def safe_upload_file(dropzone_id, file_path):
    try:
        # Attempt to upload the file
        dropzone_page.upload_file(dropzone_id, file_path)
    except Exception as e:
        print(f"Exception occurred while uploading the file to {dropzone_id}: {e}")
        capture_screenshot(f"upload_exception_{dropzone_id}.png")

        # Check if the modal alert is present only after the exception occurs
        try:
            if WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.XPATH, "/html/body/div[6]/div[7]/button[2]"))
            ):
                modal_ok_button = driver.find_element(By.XPATH, "/html/body/div[6]/div[7]/button[2]")
                modal_ok_button.click()
                print("Clicked the modal alert OK button after exception.")
                capture_screenshot("modal_alert_ok_clicked.png")
        except TimeoutException:
            print("No modal alert found to handle after file upload exception.")
        except Exception as click_exception:
            print(f"Error clicking the modal alert OK button: {click_exception}")
            capture_screenshot("modal_alert_click_error.png")

        # Retry the file upload after handling the modal, if necessary
        try:
            dropzone_page.upload_file(dropzone_id, file_path)
        except Exception as retry_exception:
            print(f"Retry failed for file upload to {dropzone_id}: {retry_exception}")
            capture_screenshot(f"retry_upload_exception_{dropzone_id}.png")

# DropzonePage class to handle file uploads
class DropzonePage:
    def __init__(self, driver):
        self.driver = driver

    def upload_file(self, dropzone_id, file_path):
        dropzone_form = (By.ID, dropzone_id)
        dropzone_message = (By.CLASS_NAME, "dz-message")

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(dropzone_form)
        )
        dropzone = self.driver.find_element(*dropzone_form)
        dropzone.click()
        self.driver.find_element(By.CSS_SELECTOR, "input[type='file']").send_keys(file_path)

        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(dropzone_message)
        )
        print(f"File uploaded successfully to {dropzone_id}.")
        capture_screenshot(f"upload_success_{dropzone_id}.png")


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
        remove_button.click()
        print(f"Successfully clicked remove button for XPath: {xpath}")
        time.sleep(2)  # Wait for the removal to complete
    except Exception as e:
        print(f"Error removing existing file for XPath {xpath}: {e}")
        capture_screenshot(f"remove_file_error_{xpath.replace('/', '_')}")

# Function to ensure the element is cleared and then set the value
def clear_and_set_value(element, value):
    try:
        element.clear()
        time.sleep(1)  # Small delay to ensure the field is cleared
        element.send_keys(value)
        print(f"Successfully set value '{value}' in element {element.get_attribute('id')}.")
    except Exception as e:
        print(f"Error setting value '{value}' in element {element.get_attribute('id')}: {e}")
        capture_screenshot(f"set_value_error_{element.get_attribute('id')}.png")

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

# Function to wait for overlay to disappear
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

# Ensure 'wizstep6' is clicked before proceeding
scroll_and_click((By.ID, "wizstep6"))

# Clear and set values in form fields
matric_percentage_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "grad_percentage"))
)
clear_and_set_value(matric_percentage_element, "79.12")

grad_passingyear_field = driver.find_element(By.ID, "grad_passingyearForeign")
clear_and_set_value(grad_passingyear_field, "10-Aug-2005")

inter_percentage_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "grad_percentage"))
)
clear_and_set_value(inter_percentage_element, "87.12")
driver.implicitly_wait(4)
# Click the save button once

# Remove files from different dropzones
xpaths = [
    '//*[@id="dropzoneEngDMC"]/div[2]/a[1]',
    '//*[@id="dropzoneEngCertificate"]/div[2]/a[1]',
]
for xpath in xpaths:
    remove_file(xpath)

# Upload files using the DropzonePage class
dropzone_page = DropzonePage(driver)
safe_upload_file("dropzoneEngDMC", r"F:\1pec\test data\Test  data pec\download (1).jpg")
driver.implicitly_wait(4)
#driver.find_element(By.XPATH , "/html/body/div[6]/div[7]/button[2]")
safe_upload_file("dropzoneEngCertificate", r"F:\1pec\test data\Test  data pec\download (1).jpg")
driver.implicitly_wait(4)
#driver.find_element(By.XPATH , "/html/body/div[6]/div[7]/button[2]")
driver.implicitly_wait(4)

#driver.find_element(By.XPATH , "/html/body/div[6]/div[7]/button[2]")
try:
    # Attempt to find and click the button with ID 'btnSubmitGradDetails'
    grad_details_button = driver.find_element(By.ID, "btnSubmitGradDetails")
    grad_details_button.click()
    print("YES, TEST CASE PASSED")
except Exception as e:
    # If there is an error, print the exception
    print(f"Failed to click 'btnSubmitGradDetails' button: {e}")



#driver.find_element(By.XPATH , "/html/body/div[6]/div[7]/button[2]")
# Close the browser session after the script is done
driver.quit()
