import pytest
import requests
import allure

from assistant_methods import generate_random_string
from check_response_methods import check_user_data_response
from check_response_methods import check_error_response

from data import URL
from data import ErrorSample
from data import ResponseSample


class TestChangeUserData:
    @pytest.mark.parametrize("changed_field", [
        'email',
        'password',
        'name'
    ])
    @allure.title('Проверка: у авторизованного пользователя можно изменить каждое поле')
    def test_change_authorized_user_data_success(self, create_new_user_and_return_token, changed_field):
        token = create_new_user_and_return_token
        new_data = {changed_field: generate_random_string(5)}
        response = requests.patch(URL.USER, headers={'Authorization': token}, data=new_data, timeout=10)
        check_response = check_user_data_response(response.json(), ResponseSample.USER_INFO)
        assert response.status_code == 200 and check_response == "OK"

    @pytest.mark.parametrize("changed_field", [
        'email',
        'password',
        'name'
    ])
    @allure.title('Проверка: при попытке изменить любое поле без авторизации вернётся ошибка 401')
    def test_change_unauthorized_user_data_causes_error(self, changed_field):
        new_data = {changed_field: generate_random_string(5)}
        response = requests.patch(URL.USER, data=new_data, timeout=10)
        check_response = check_error_response(response.json(), ErrorSample.UNAUTHORIZED_USER)
        assert response.status_code == 401 and check_response == "OK"
