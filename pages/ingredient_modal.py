from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class IngredientModal(BasePage):
    TITLE = (By.CSS_SELECTOR, ".modal__title")
    CLOSE_BTN = (By.CSS_SELECTOR, ".modal__close")

    def wait_for_open(self):
        return self.is_visible(self.TITLE)

    def close(self):
        self.click(self.CLOSE_BTN)

    def get_title(self):
        return self.get_text(self.TITLE)
