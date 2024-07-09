## QA Diplom_2

#### Тесты API для Stellar Burgers

Содержимое проекта:

**tests** - папка с тестами

**conftest.py** - файл с с фикстурами

**check_response_methods** - файл с методами для проверки тела ответа

**assistant_methods** - файл со вспомогательными методами (генераторы и тд)

**data.py** - файл с данными проекта (урлы, образцы ответов)

**allure_results** - отчёты

**requirements.txt** - внешние зависимости

## Тесты
### Создание пользователя 
#### POST https://stellarburgers.nomoreparties.site/api/auth/register
**test_create_new_user_success**

Проверка: можно создать нового пользователя

Фикстура: new_user_payload

Метод проверки ответа: check_user_data_response

**test_create_two_same_users_causes_error**

Проверка: при попытке создать пользователя, идентичного уже существующему, вернётся ошибка 403

Фикстура: new_user_payload

Метод проверки ответа: check_error_response

**test_create_new_user_without_required_fields_causes_error**

Проверка: если одно из обязательных полей отсутствует, вернётся ошибка 403

Фикстура: new_user_payload

Параметр: удаляемое поле

Метод проверки ответа: check_error_response

### Логин пользователя 
#### POST https://stellarburgers.nomoreparties.site/api/auth/login 
**test_login_user_success**

Проверка: пользователя можно авторизовать

Фикстура: create_new_user_and_return_email_and_pass

Метод проверки ответа: check_user_data_response

**test_login_user_with_wrong_fields_causes_error**

Проверка: Проверка: если одно из полей некорректное, вернётся ошибка 401

Фикстура: create_new_user_and_return_email_and_pass

Параметр: невалидное поле

Исп. метод: generate_random_string

Метод проверки ответа: check_error_response

**test_login_user_with_wrong_fields_causes_error**

Проверка: Проверка: если одно из полей некорректное, вернётся ошибка 401

Фикстура: create_new_user_and_return_email_and_pass

Параметр: невалидное поле

Исп. метод: generate_random_string

Метод проверки ответа: check_error_response

### Изменение данных пользователя 
#### PATCH https://stellarburgers.nomoreparties.site/api/auth/user 
**test_change_user_data_success**

Проверка: у авторизованного пользователя можно изменить каждое поле

Фикстура: create_new_user_and_return_token

Параметр: изменяемое поле

Метод проверки ответа: check_user_data_response

**test_change_unauthorized_user_data_causes_error**

Проверка: при попытке изменить любое поле без авторизации вернётся ошибка 401

Параметр: изменяемое поле

Метод проверки ответа: check_error_response

### Получить список заказов пользователя 
#### GET https://stellarburgers.nomoreparties.site/api/orders
**test_get_user_orders_success**

Проверка: можно получить список заказов авторизованного пользователя

Фикстура: create_new_user_and_return_token

Метод проверки ответа: check_user_orders_response

**test_get_unauthorized_user_orders_causes_error**

Проверка: при попытке получить заказы без авторизации вернётся ошибка 401

Метод проверки ответа: check_error_response

### Создание заказа
#### POST https://stellarburgers.nomoreparties.site/api/orders
**test_create_order_success**

Проверка: с авторизацией заказ можно создать

Фикстура: create_new_user_and_return_token

Исп. методы: build_random_order

Метод проверки ответа: check_order_creation_response

**test_create_order_with_invalid_payload_causes_error**

Проверка: при попытке создать заказ с невалидным хэшем ингредиента вернётся ошибка 500

Фикстура: create_new_user_and_return_token

Исп. методы: build_random_order, generate_random_string

**test_create_order_without_any_ingredients_causes_error**

Проверка: при попытке создать заказ без ингредиентов вернётся ошибка 400

Фикстура: create_new_user_and_return_token

Метод проверки ответа: check_error_response

**test_create_order_by_unauthorized_user_causes_error**

Проверка: при попытке создать заказ без авторизации вернётся ошибка 401

Исп. методы: build_random_order

Метод проверки ответа: check_error_response

### Фикстуры:

**new_user_payload** - возвращает словарь со сгенерированными данными для регистрации нового пользователя, потом удаляет пользователя если он был создан

Вспомогательные методы: new_user_data

**create_new_user_and_return_email_and_pass(new_user_payload)** - создаёт нового пользователя и возвращает логин-пароль

**create_new_user_and_return_token(create_new_user_and_return_email_and_pass)** - возвращает токен созданного пользователя

### assistant_methods:

**new_user_data** - возвращает словарь со сгенерированными данными для создания нового пользователя

Исп. методы: generate_random_email, generate_random_string

**generate_random_string(length)** - возвращает случайную строку заданной длины

**generate_random_email** - возвращает случайную строку вида *****_test@ya.ru

Исп. методы: generate_random_string

**build_random_order** - возвращает случайный корректный заказ из 3-х ингредиентов

### check_response_methods:

Все методы сверяют тело ответа по структуре и ключам с образцами

**check_user_data_response(response, sample)** - сверяет с образцами ответа при регистрации, авторизации или изменении данных пользователя

Аргументы: тело ответа, образец ответа

**check_user_orders_response(response)** - сверяет с образцами ответа при получении списка заказов пользователя

Аргументы: тело ответа

**check_order_creation_response(response)** - сверяет с образцом ответа при успешном создании заказа

Аргументы: тело ответа

**def check_error_response(response, sample)** - проверяет статус и сверяет текст сообщения об ошибке с образцом

Аргументы: тело ответа, образец сообщения
