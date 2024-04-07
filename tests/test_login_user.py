import pytest
import requests
import allure

from check_response_methods import check_user_data_response
from assistant_methods import generate_random_string
from check_response_methods import check_error_response

from data import URL
from data import ErrorSample
from data import ResponseSample


class TestLoginUser:
    @allure.title('Проверка: пользователя можно авторизовать')
    def test_login_user_success(self, create_new_user_and_return_email_and_pass):
        payload = create_new_user_and_return_email_and_pass
        response = requests.post(URL.LOGIN, data=payload, timeout=10)
        check_response = check_user_data_response(response.json(), ResponseSample.USER_CREATED_OR_LOGIN_SUCCESS)
        assert response.status_code == 200 and check_response == "OK"

    @pytest.mark.parametrize(
        "wrong_field", [
            'email',
            'password'
        ])
    @allure.title('Проверка: если одно из полей некорректное, вернётся ошибка 401')
    def test_login_user_with_wrong_fields_causes_error(
            self, create_new_user_and_return_email_and_pass, wrong_field):
        payload = create_new_user_and_return_email_and_pass
        payload[wrong_field] = generate_random_string(5)
        response = requests.post(URL.LOGIN, data=payload, timeout=10)
        check_response = check_error_response(response.json(), ErrorSample.LOGIN_INVALID_FIELDS)
        assert response.status_code == 401 and check_response == "OK"
