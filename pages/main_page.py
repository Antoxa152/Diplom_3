import re
from typing import List

from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class MainPage(BasePage):
    CONSTRUCTOR_LINK = (By.CSS_SELECTOR, '[href="/constructor"]')
    ORDER_FEED_LINK = (By.CSS_SELECTOR, '[href="/feed"]')

    INGREDIENT_CARDS = (By.CSS_SELECTOR, ".ingredient-card")

    COUNTER_TOTAL = (By.CSS_SELECTOR, "[data-testid='counter-total']")
    COUNTER_TODAY = (By.CSS_SELECTOR, "[data-testid='counter-today']")

    INGREDIENT_IN_ASSEMBLY = (By.CSS_SELECTOR, ".burger-ingredients__ingredient")

    WORK_IN_PROGRESS_BLOCK = (By.CSS_SELECTOR, "[data-testid='work-in-progress']")
    ORDER_CARDS_IN_WORK = (By.CSS_SELECTOR, ".order-card")

    ORDER_BUTTON = (By.CSS_SELECTOR, ".button_order")

    def go_to_constructor(self) -> None:
        self.click(self.CONSTRUCTOR_LINK)

    def go_to_order_feed(self) -> None:
        self.click(self.ORDER_FEED_LINK)

    def open_ingredient_modal(self, index: int = 0) -> None:
        cards: List = self.find_elements(self.INGREDIENT_CARDS)
        if index >= len(cards):
            raise IndexError(f"Нет карточки с индексом {index}, всего карточек: {len(cards)}")
        card = cards[index]
        self.scroll_into_view(card)
        self.click((By.CSS_SELECTOR, f".ingredient-card:nth-child({index + 1})"))

    def is_ingredients_list_visible(self, timeout: int = 8) -> bool:
        """Проверка, что список ингредиентов виден (для теста навигации)."""
        return self.is_visible(self.INGREDIENT_CARDS, timeout=timeout)

    def is_work_in_progress_block_visible(self, timeout: int = 8) -> bool:
        """Проверка, что блок «В работе» виден (для теста перехода в ленту)."""
        return self.is_visible(self.WORK_IN_PROGRESS_BLOCK, timeout=timeout)

    def _get_first_ingredient_name_substring(self) -> str:
        """
        Вспомогательный метод: берёт текст первой карточки и возвращает
        первую английскую подстроку (например, 'cheese' из 'Cheese, 100g').
        Логика спрятана здесь, а не в тесте.
        """
        cards = self.find_elements(self.INGREDIENT_CARDS)
        if not cards:
            raise AssertionError("Нет карточек ингредиентов на странице")
        text = cards[0].text
        match = re.search(r"[A-Za-z]+", text)
        return match.group(0).lower() if match else "ingredient"

    def get_ingredient_count_in_assembly_by_first_card(self) -> int:
        """Считает количество ингредиентов в сборке по названию первой карточки."""
        substring = self._get_first_ingredient_name_substring()
        return self.get_ingredient_count_in_assembly(substring)

    def add_first_ingredient(self) -> None:
        """
        Открывает модалку первого ингредиента.
        Предполагается, что в тренажёре клик по карточке в модалке
        автоматически добавляет ингредиент в сборку.
        Если нужна отдельная кнопка «Добавить» — логику переносят сюда.
        """
        self.open_ingredient_modal(index=0)

    def get_total_counter(self) -> int:
        text = self.get_text(self.COUNTER_TOTAL)
        return int(text)

    def get_today_counter(self) -> int:
        text = self.get_text(self.COUNTER_TODAY)
        return int(text)

    def get_ingredient_count_in_assembly(self, ingredient_name_substring: str) -> int:
        ingredients = self.find_elements(self.INGREDIENT_IN_ASSEMBLY)
        count = 0
        substring = ingredient_name_substring.lower()
        for el in ingredients:
            text = el.text.lower()
            if substring in text:
                count += 1
        return count

    def wait_for_order_in_work(self, order_number: str, timeout: int = 15) -> bool:
        def condition(_):
            cards = self.find_elements(self.ORDER_CARDS_IN_WORK, timeout=timeout)
            for card in cards:
                if order_number in card.text:
                    return True
            return False
        try:
            self.wait_until(condition, timeout=timeout)
            return True
        except Exception:
            return False
