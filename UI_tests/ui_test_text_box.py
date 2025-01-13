import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from ui_text_box_page import TextBoxPage


@pytest.fixture
def driver():
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def test_text_box_scenario(driver):
    page = TextBoxPage(driver)
    page.load()

    # Input data
    page.set_full_name("Donald Duck")
    page.set_email("donald.duck@example.com")
    page.set_current_address("56 Main St")
    page.set_permanent_address("379 Apple Rd")

    # Submit the form
    page.submit()

    # Assertions to verify the output
    assert "Name:Donald Duck" in page.get_output_name()
    assert "Email:donald.duck@example.com" in page.get_output_email()
    assert "Current Address :56 Main St" in page.get_output_current_address()
    assert "Permananet Address :379 Apple Rd" in page.get_output_permanent_address()
