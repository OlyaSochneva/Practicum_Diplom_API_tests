import pytest
import requests
import allure

from check_response_methods import check_user_data_response
from check_response_methods import check_error_response

from data import URL
from data import ErrorSample
from data import ResponseSample


class TestCreateNewUser:
    @allure.title('Проверка: можно создать нового пользователя')
    def test_create_new_user_success(self, new_user_payload):
        payload = new_user_payload
        response = requests.post(URL.REGISTRATION, data=payload, timeout=10)
        check_response = check_user_data_response(response.json(), ResponseSample.USER_CREATED_OR_LOGIN_SUCCESS)
        assert response.status_code == 200 and check_response == "OK"

    @allure.title('Проверка: при попытке создать пользователя, идентичного уже существующему, вернётся ошибка 403')
    def test_create_two_same_users_causes_error(self, new_user_payload):
        payload = new_user_payload
        requests.post(URL.REGISTRATION, data=payload, timeout=10)
        response = requests.post(URL.REGISTRATION, data=payload, timeout=10)
        check_response = check_error_response(response.json(), ErrorSample.REG_USER_ALREADY_EXISTS)
        assert response.status_code == 403 and check_response == "OK"

    @pytest.mark.parametrize(
        "deleted_field", [
            "email",
            "password",
            "name"
        ]
    )
    @allure.title('Проверка: если одно из обязательных полей отсутствует, вернётся ошибка 403')
    def test_create_new_user_without_required_fields_causes_error(
            self, new_user_payload, deleted_field):
        payload = new_user_payload
        payload.pop(deleted_field)
        response = requests.post(URL.REGISTRATION, data=payload, timeout=10)
        check_response = check_error_response(response.json(), ErrorSample.REG_MISS_REQUIRED_FIELDS)
        assert response.status_code == 403 and check_response == "OK"
