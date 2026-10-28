from pages.base_page import BasePage
from .locators import IngredientModalLocators


class IngredientModal(BasePage):
    def wait_for_open(self, timeout=8) -> bool:
        """Ждёт, пока модалка откроется (заголовок виден)."""
        return self.is_visible(IngredientModalLocators.TITLE, timeout=timeout)

    def is_open(self, timeout=3) -> bool:
        """Проверяет, открыто ли окно (заголовок виден). Возвращает True/False."""
        return self.is_visible(IngredientModalLocators.TITLE, timeout=timeout)

    def close(self, timeout=5) -> None:
        """Закрывает окно по кнопке «крестик»."""
        self.click(IngredientModalLocators.CLOSE_BTN, timeout=timeout)

    def get_title(self, timeout=5) -> str:
        return self.get_text(IngredientModalLocators.TITLE, timeout=timeout)
