import pytest
import requests

from assistant_methods import new_user_data

from data import URL


@pytest.fixture(scope="function")
def new_user_payload():
    payload = new_user_data()
    email_pass = {'email': payload['email'], 'password': payload['password']}
    yield payload
    response = requests.post(URL.LOGIN, data=email_pass)
    if response.status_code == 200:
        token = response.json()['accessToken']
        requests.delete(URL.USER, headers={'Authorization': token})


@pytest.fixture(scope="function")
def create_new_user_and_return_email_and_pass(new_user_payload):
    email_pass = {}
    payload = new_user_payload
    requests.post(URL.REGISTRATION, data=payload)
    email_pass['email'] = payload['email']
    email_pass['password'] = payload['password']
    return email_pass


@pytest.fixture(scope="function")
def create_new_user_and_return_token(create_new_user_and_return_email_and_pass):
    payload = create_new_user_and_return_email_and_pass
    response = requests.post(URL.LOGIN, data=payload, timeout=10).json()
    token = response['accessToken']
    return token
