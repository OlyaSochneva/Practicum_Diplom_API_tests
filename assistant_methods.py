import string
import random
import requests
from data import URL


def new_user_data():
    payload = {
        "email": generate_random_email(),
        "password": generate_random_string(5),
        "name": generate_random_string(5)
    }
    return payload


def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


def generate_random_email():
    email = generate_random_string(5)
    email += '_test@ya.ru'
    return email


def build_random_order():
    buns_list = []
    main_list = []
    sauces_list = []
    response = requests.get(URL.INGREDIENTS).json()
    for ingredient in response['data']:
        if ingredient['type'] == 'bun':
            buns_list.append(ingredient['_id'])
        if ingredient['type'] == 'main':
            main_list.append(ingredient['_id'])
        if ingredient['type'] == 'sauce':
            sauces_list.append(ingredient['_id'])
    bun = random.choice(buns_list)
    main = random.choice(main_list)
    sauce = random.choice(sauces_list)
    burger = [bun, main, sauce]
    payload = {"ingredients": burger}
    return payload
