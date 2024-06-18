import requests
import allure

from check_response_methods import check_error_response
from check_response_methods import check_user_orders_response

from data import URL
from data import ErrorSample


class TestGetUserOrders:
    @allure.title('Проверка: можно получить список заказов авторизованного пользователя')
    def test_get_authorized_user_orders_success(self, create_new_user_and_return_token):
        token = create_new_user_and_return_token
        response = requests.get(URL.ORDERS, headers={'Authorization': token}, timeout=10)
        check_response = check_user_orders_response(response.json())
        assert response.status_code == 200 and check_response == "OK"

    @allure.title('Проверка: при попытке получить заказы без авторизации вернётся ошибка 401')
    def test_get_unauthorized_user_orders_causes_error(self):
        response = requests.get(URL.ORDERS, timeout=10)
        check_response = check_error_response(response.json(), ErrorSample.UNAUTHORIZED_USER)
        assert response.status_code == 401 and check_response == "OK"
