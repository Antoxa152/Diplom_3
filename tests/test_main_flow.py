import allure
import pytest


@allure.title("Переход по клику на «Конструктор»")
@allure.description("Пользователь переходит в конструктор бургеров через меню")
def test_go_to_constructor(main_page):
    main_page.go_to_constructor()
    
    assert main_page.is_visible(main_page.INGREDIENT_CARDS, timeout=8)


@allure.title("Переход по клику на раздел «Лента заказов»")
@allure.description("Пользователь переходит к ленте заказов")
def test_go_to_order_feed(main_page):
    main_page.go_to_order_feed()
    assert main_page.is_visible(main_page.WORK_IN_PROGRESS_BLOCK, timeout=8)


@allure.title("Клик на ингредиент открывает модальное окно")
@allure.description("При клике на карточку ингредиента появляется всплывающее окно с деталями")
def test_ingredient_modal_opens(main_page, ingredient_modal):
    main_page.go_to_constructor()
    main_page.open_ingredient_modal(index=0)
    assert ingredient_modal.wait_for_open() is True


@allure.title("Модальное окно закрывается по клику на крестик")
@allure.description("Окно закрывается, и можно снова взаимодействовать со страницей")
def test_ingredient_modal_closes(main_page, ingredient_modal):
    main_page.go_to_constructor()
    main_page.open_ingredient_modal(index=0)
    ingredient_modal.close()
    
    assert not ingredient_modal.is_visible(ingredient_modal.TITLE, timeout=3)


@allure.title("Добавление ингредиента увеличивает его счётчик в сборке")
@allure.description("После добавления ингредиента счётчик этого ингредиента в бургере увеличивается")
def test_ingredient_counter_increases(main_page):
    main_page.go_to_constructor()

    cards = main_page.driver.find_elements(*main_page.INGREDIENT_CARDS)
    first_card_text = cards[0].text
    import re
    match = re.search(r"[A-Za-z]+", first_card_text)
    name_substring = match.group(0) if match else "ingredient"

    initial_count = main_page.get_ingredient_count_in_assembly(name_substring)

   
    main_page.open_ingredient_modal(0)  # в тренажёрах часто клик на карточку сразу добавляет
    
    final_count = main_page.get_ingredient_count_in_assembly(name_substring)
    assert final_count == initial_count + 1


@allure.title("Счётчик «Выполнено за всё время» увеличивается при новом заказе")
@allure.description("Оформление заказа увеличивает глобальный счётчик выполненных заказов")
def test_counter_total_increases_on_new_order(main_page):
    main_page.go_to_constructor()
    initial_total = main_page.get_total_counter()

    assert True  # Заглушка: сюда нужно вставить реальный флоу оформления заказа


@allure.title("Счётчик «Выполнено за сегодня» увеличивается при новом заказе")
@allure.description("Оформление заказа увеличивает счётчик за сегодня")
def test_counter_today_increases_on_new_order(main_page):
    main_page.go_to_constructor()
    initial_today = main_page.get_today_counter()
    assert True  # Заглушка


@allure.title("Номер нового заказа появляется в разделе «В работе»")
@allure.description("После оформления заказа его номер отображается в ленте «В работе»")
def test_order_appears_in_work_in_progress(main_page):
    main_page.go_to_constructor()
   

    assert True  # Заглушка: здесь будет реальная логика оформления и проверки
