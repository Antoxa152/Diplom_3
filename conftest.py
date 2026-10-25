import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    browser = request.param

    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(
            service=ChromeDriverManager().install(),
            options=options
        )
    elif browser == "firefox":
        options = FirefoxOptions()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        driver = webdriver.Firefox(
            service=GeckoDriverManager().install(),
            options=options
        )
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.implicitly_wait(5)
    yield driver
    driver.quit()


@pytest.fixture
def main_page(driver):
    from pages.main_page import MainPage
    page = MainPage(driver)
    driver.get("https://stellarburgers.education-services.ru/")  
    return page


@pytest.fixture
def ingredient_modal(driver):
    from pages.ingredient_modal import IngredientModal
    return IngredientModal(driver)
