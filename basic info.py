import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException, WebDriverException

# Setup Chrome WebDriver
chrome_service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=chrome_service)

def safe_click(element):
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element)).click()
    except (ElementNotInteractableException, NoSuchElementException) as e:
        print(f"Error interacting with element: {e}")
        capture_screenshot(f"error_{element[1]}.png")

def capture_screenshot(filename):
    try:
        driver.get_screenshot_as_file(filename)
        print(f"Screenshot saved as {filename}")
    except Exception as e:
        print(f"Error capturing screenshot: {e}")

def select_application_type():
    dropdown_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "select2-ApplicationType-container"))
    )
    dropdown_element.click()
    option_to_select = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//li[text()='Graduate Before 2008']"))
    )
    option_to_select.click()

def select_first_value(element_id, value):
    try:
        dropdown = Select(WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, element_id))
        ))
        dropdown.select_by_visible_text(value)
    except WebDriverException:
        dropdown_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, element_id))
        )
        dropdown_element.click()
        option_to_select = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//li[text()='{value}']"))
        )
        option_to_select.click()

def select_employment_sector():
    select_first_value("select2-basicinfo_employmentsector-container", "Government")

def select_blood_group():
        select_first_value("select2-basicinfo_bloodGroup-container", "A+ve")
def select_gender():
    select_first_value("select2-basicinfo_gender-container", "Male")

def click_element(driver, locator, wait_time=10):
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.visibility_of_element_located(locator)
        )
        element = WebDriverWait(driver, wait_time).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
    except Exception as e:
        print(f"Error clicking element with locator {locator}: {e}")
        capture_screenshot(f"click_error_{locator[1]}.png")

try:
    driver.get("http://10.0.32.90:8012/")
    driver.maximize_window()

    safe_click((By.LINK_TEXT, "Sign In"))

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "username"))).send_keys("pectesting12345@gmail.com")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "password"))).send_keys("pec123")
    safe_click((By.ID, "btn-login"))

    safe_click((By.ID, "wizstep1"))
    select_gender()
    select_application_type()
    select_blood_group()

    time.sleep(20)


    click_element(driver, (By.ID, "btnSubmitBasicInfo"))
    capture_screenshot(f"click_error_{[1]}.png")
    click_element(driver, (By.XPATH, "//button[text()='OK']"))
    capture_screenshot(f"click_error_{[2]}.png")
    click_element(driver, (By.XPATH, "//button[contains(@class, 'btn-info') and text()='Next']"))

    # Add these function calls to select gender and blood group


    try:
        capture_screenshot(f"click_error_{[3]}.png")
        time.sleep(20)
        element_basic_assertion = driver.find_element(By.XPATH, "//h4[text()='Mailing Details']")
        if element_basic_assertion.is_displayed():
            print("Basic info page pass")
        else:
            print("Basic info page fail - Element is not visible")
    except NoSuchElementException:
        print("Basic info page fail - Element not found")

finally:
    driver.quit()
