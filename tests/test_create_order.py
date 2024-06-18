import requests
import allure

from check_response_methods import check_order_creation_response
from check_response_methods import check_error_response
from assistant_methods import build_random_order
from assistant_methods import generate_random_string

from data import URL
from data import ErrorSample


class TestCreateOrder:

    # в тесте с 500-й ошибкой я посчитала правильным только проверить код и не делать парсинг ответа
    # кроме того, в документации не указано, что должно приходить сообщение (соотв. нет образца)
    @allure.title('Проверка: при попытке создать заказ с невалидным хэшем ингредиента вернётся ошибка 500')
    def test_create_order_with_invalid_payload_causes_error(self, create_new_user_and_return_token):
        token = create_new_user_and_return_token
        payload = build_random_order()
        payload["ingredients"].append(generate_random_string(10))
        response = requests.post(URL.ORDERS, headers={'Authorization': token}, data=payload, timeout=10)
        assert response.status_code == 500

    @allure.title('Проверка: при попытке создать заказ без ингредиентов вернётся ошибка 400')
    def test_create_order_without_any_ingredients_causes_error(self, create_new_user_and_return_token):
        token = create_new_user_and_return_token
        response = requests.post(URL.ORDERS, headers={'Authorization': token}, timeout=10)
        check_response = check_error_response(response.json(), ErrorSample.NO_INGREDIENTS)
        assert response.status_code == 400 and check_response == "OK"

    @allure.title('Проверка: при попытке создать заказ без авторизации вернётся ошибка 401')
    @allure.description('Баг: фактически можно создать заказ без авторизации')
    def test_create_order_by_unauthorized_user_causes_error(self):
        payload = build_random_order()
        response = requests.post(URL.ORDERS, data=payload, timeout=10)
        check_response = check_error_response(response.json(), ErrorSample.UNAUTHORIZED_USER)
        assert response.status_code == 401 and check_response == "OK"

    @allure.title('Проверка: с авторизацией заказ можно создать')
    @allure.description('Тест падает, тк структура ответа не соответствует той, что указана как «пример ответа» '
                        'в документации API, хотя фактически приходит больше данных о заказе и ответ '
                        'включает в себя образец, но содержит ещё много дополнительных ключей')
    def test_create_order_success(self, create_new_user_and_return_token):
        token = create_new_user_and_return_token
        payload = build_random_order()
        response = requests.post(URL.ORDERS, headers={'Authorization': token}, data=payload, timeout=10)
        check_response = check_order_creation_response(response.json())
        assert response.status_code == 200 and check_response == "OK"

