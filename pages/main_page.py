from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import time


class MainPage(BasePage):
    # Навигация
    CONSTRUCTOR_LINK = (By.CSS_SELECTOR, '[href="/constructor"]')
    ORDER_FEED_LINK = (By.CSS_SELECTOR, '[href="/feed"]')

    # Ингредиенты (список карточек)
    INGREDIENT_CARDS = (By.CSS_SELECTOR, ".ingredient-card")

    # Счётчики (в шапке/сайдбаре)
    COUNTER_TOTAL = (By.CSS_SELECTOR, "[data-testid='counter-total']")
    COUNTER_TODAY = (By.CSS_SELECTOR, "[data-testid='counter-today']")

    # Сборка бургера: счётчик каждого ингредиента в сборке
    INGREDIENT_IN_ASSEMBLY = (By.CSS_SELECTOR, ".burger-ingredients__ingredient")

    # Лента заказов: блок «В работе» и карточки заказов
    WORK_IN_PROGRESS_BLOCK = (By.CSS_SELECTOR, "[data-testid='work-in-progress']")
    ORDER_CARDS_IN_WORK = (By.CSS_SELECTOR, ".order-card")

    # Кнопка оформления заказа (если нужна в других тестах)
    ORDER_BUTTON = (By.CSS_SELECTOR, ".button_order")

    def go_to_constructor(self):
        self.click(self.CONSTRUCTOR_LINK)

    def go_to_order_feed(self):
        self.click(self.ORDER_FEED_LINK)

    def open_ingredient_modal(self, index=0):
        cards = self.driver.find_elements(*self.INGREDIENT_CARDS)
        # Прокрутка, если элемент не в видимой области
        self.driver.execute_script("arguments[0].scrollIntoView();", cards[index])
        time.sleep(0.3)  # небольшая пауза, чтобы клик не «пролетел»
        cards[index].click()

    def get_total_counter(self):
        return int(self.get_text(self.COUNTER_TOTAL))

    def get_today_counter(self):
        return int(self.get_text(self.COUNTER_TODAY))

    def get_ingredient_count_in_assembly(self, ingredient_name_substring: str) -> int:
        """
        Считает количество карточек ингредиента в сборке по подстроке в названии.
        Например, 'cheese' найдёт карточку с 'Cheese'.
        """
        ingredients = self.driver.find_elements(*self.INGREDIENT_IN_ASSEMBLY)
        count = 0
        for el in ingredients:
            text = el.text.lower()
            if ingredient_name_substring.lower() in text:
                count += 1
        return count

    def wait_for_order_in_work(self, order_number: str, timeout=15):
        """Ждёт появления заказа с номером в блоке «В работе»."""
        def condition(driver):
            cards = driver.find_elements(*self.ORDER_CARDS_IN_WORK)
            for card in cards:
                if order_number in card.text:
                    return True
            return False
        self.wait.until(condition, timeout)
