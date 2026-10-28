from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def _wait(self, condition, locator=None, timeout=None):
        """Вспомогательный метод для ожидания с правильным таймаутом."""
        if timeout is None:
            timeout = self.timeout
        return WebDriverWait(self.driver, timeout).until(condition)

    def find_element(self, locator, timeout=None):
        """Ждёт появления элемента по локатору."""
        return self._wait(
            EC.presence_of_element_located(locator),
            locator=locator,
            timeout=timeout
        )

    def find_elements(self, locator, timeout=None):
        """Ждёт появления списка элементов по локатору."""
        return self._wait(
            EC.presence_of_all_elements_located(locator),
            locator=locator,
            timeout=timeout
        )

    def click(self, locator, timeout=None):
        """Кликает по элементу после ожидания его кликабельности."""
        element = self._wait(
            EC.element_to_be_clickable(locator),
            locator=locator,
            timeout=timeout
        )
        element.click()

    def is_visible(self, locator, timeout=None):
        """Возвращает True, если элемент виден, иначе False."""
        if timeout is None:
            timeout = self.timeout
        try:
            self._wait(
                EC.visibility_of_element_located(locator),
                locator=locator,
                timeout=timeout
            )
            return True
        except TimeoutException:
            return False

    def get_text(self, locator, timeout=None):
        """Получает текст элемента после ожидания его видимости."""
        element = self._wait(
            EC.visibility_of_element_located(locator),
            locator=locator,
            timeout=timeout
        )
        return element.text.strip()

    def scroll_into_view(self, element):
        """Прокручивает элемент в область видимости."""
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def wait_until(self, condition, timeout=None):
        """Универсальный метод для кастомных условий (например, поиск по тексту)."""
        if timeout is None:
            timeout = self.timeout
        return WebDriverWait(self.driver, timeout).until(condition)
    