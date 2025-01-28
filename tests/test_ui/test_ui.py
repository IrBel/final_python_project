import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from core.ui_text_box_page import TextBoxPage
from core.logger import get_logger

# Initialize the logger
logger = get_logger(__name__)


@pytest.fixture(scope="session")
def driver():
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.mark.ui
def test_text_box_scenario(driver):
    logger.debug("Starting log for test_text_box_scenario")
    page = TextBoxPage(driver)
    page.load()

    # Define WebDriverWait
    wait = WebDriverWait(driver, 10)

    # Input data
    page.set_full_name("Donald Duck")
    page.set_email("donald.duck@example.com")
    page.set_current_address("56 Main St")
    page.set_permanent_address("379 Apple Rd")

    # Ensure the submit button is clickable
    submit_button = wait.until(EC.element_to_be_clickable((By.ID, page.SUBMIT_BUTTON[1])))

    # Scroll the element into view
    driver.execute_script("arguments[0].scrollIntoView();", submit_button)

    # Click the submit button
    submit_button.click()

    # Assertions to verify the output
    assert "Name:Donald Duck" in page.get_output_name()
    assert "Email:donald.duck@example.com" in page.get_output_email()
    assert "Current Address :56 Main St" in page.get_output_current_address()
    assert "Permananet Address :379 Apple Rd" in page.get_output_permanent_address()
    logger.debug("test_text_box_scenario successfully passed")