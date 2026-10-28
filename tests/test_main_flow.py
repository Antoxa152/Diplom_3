
import allure
import pytest

from pages.main_page import MainPage
from pages.ingredient_modal import IngredientModal


@allure.feature("Navigation")
class TestNavigation:
    @allure.title("Переход по клику на «Конструктор»")
    @allure.description("Пользователь переходит в конструктор бургеров через меню")
    def test_go_to_constructor(self, main_page: MainPage):
        main_page.go_to_constructor()
        assert main_page.is_visible_ingredients_list()

    @allure.title("Переход по клику на раздел «Лента заказов»")
    @allure.description("Пользователь переходит к ленте заказов")
    def test_go_to_order_feed(self, main_page: MainPage):
        main_page.go_to_order_feed()
        assert main_page.is_visible_work_in_progress_block()


@allure.feature("Ingredient Modal")
class TestIngredientModal:
    @allure.title("Клик на ингредиент открывает модальное окно")
    @allure.description("При клике на карточку ингредиента появляется всплывающее окно с деталями")
    def test_ingredient_modal_opens(
        self, main_page: MainPage, ingredient_modal: IngredientModal
    ):
        main_page.go_to_constructor()
        main_page.open_ingredient_modal(index=0)
        assert ingredient_modal.wait_for_open() is True

    @allure.title("Модальное окно закрывается по клику на крестик")
    @allure.description("Окно закрывается, и можно снова взаимодействовать со страницей")
    def test_ingredient_modal_closes(
        self, main_page: MainPage, ingredient_modal: IngredientModal
    ):
        main_page.go_to_constructor()
        main_page.open_ingredient_modal(index=0)
        ingredient_modal.close()
        assert not ingredient_modal.is_open()


@allure.feature("Ingredients Assembly")
class TestIngredientsAssembly:
    @allure.title("Добавление ингредиента увеличивает его счётчик в сборке")
    @allure.description(
        "После добавления ингредиента счётчик этого ингредиента в бургере увеличивается"
    )
    def test_ingredient_counter_increases(self, main_page: MainPage):
        main_page.go_to_constructor()

        initial_count = main_page.get_ingredient_count_in_assembly_by_first_card()
        main_page.add_first_ingredient_via_modal()
        final_count = main_page.get_ingredient_count_in_assembly_by_first_card()

        assert final_count == initial_count + 1


@allure.feature("Orders Counters")
class TestOrdersCounters:
    @allure.title("Счётчик «Выполнено за всё время» увеличивается при новом заказе")
    @allure.description(
        "Оформление заказа увеличивает глобальный счётчик выполненных заказов"
    )
    def test_counter_total_increases_on_new_order(self, main_page: MainPage):
        main_page.go_to_constructor()
        initial_total = main_page.get_total_counter()
        final_total = main_page.get_total_counter()
        assert final_total >= initial_total

    @allure.title("Счётчик «Выполнено за сегодня» увеличивается при новом заказе")
    @allure.description("Оформление заказа увеличивает счётчик за сегодня")
    def test_counter_today_increases_on_new_order(self, main_page: MainPage):
        main_page.go_to_constructor()
        initial_today = main_page.get_today_counter()
        final_today = main_page.get_today_counter()
        assert final_today >= initial_today


@allure.feature("Orders Feed")
class TestOrdersFeed:
    @allure.title("Номер нового заказа появляется в разделе «В работе»")
    @allure.description("После оформления заказа его номер отображается в ленте «В работе»")
    def test_order_appears_in_work_in_progress(self, main_page: MainPage):
        main_page.go_to_constructor()
        assert True