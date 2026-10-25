from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        element = self.find_element(locator)
        self.wait.until(EC.element_to_be_clickable(element))
        element.click()

    def is_visible(self, locator, timeout=5):
        try:
            self.wait.until(EC.visibility_of_element_located(locator), timeout=timeout)
            return True
        except TimeoutException:
            return False

    def get_text(self, locator):
        return self.find_element(locator).text
