import datetime
import functools
from decorators import do_twice
from decorators import debug
import pytest
import requests


# 26.1. Функции и как они работают. Возвращаемые типы и типы передаваемых параметров:

# 1

# name = 'John'
#
# def say_hello(name):
#     return f"Hello {name}"
#
# def be_awesome(name):
#     return f"Yo {name}, together we are the awesomest!"
#
# def greet_bob(be_awesome):
#     return be_awesome("Bob")
#
#
# print(greet_bob(be_awesome))

# 2

# def parent():
#     print("Printing from the parent() function")
#
#     def first_child():
#         print("Printing from the first_child() function")
#
#     def second_child():
#         print("Printing from the second_child() function")
#
#     second_child()
#     first_child()
#
# parent() # Порядок выполнения заложен не в порядке описания дочерних функций, а в порядке их вызова.
# Сами по себе дочерние функции не вызываются при вызове родительской.
# =>
# Printing from the parent() function
# Printing from the second_child() function
# Printing from the first_child() function

# 3

# def parent(num):
#     def first_child():
#         return "Hi, I am Emma"
#
#     def second_child():
#         return "Call me Liam"
#
#     if num == 1:
#         return first_child
#     else:
#         return second_child
# # Чтобы воспользоваться тем, что функция в качестве значения возвращает другую функцию,
# # нужно вызвать ее следующим образом:
#
# first = parent(1)
# second = parent(2)
#
# print(first()) # Фактически при вызове parent() с аргументом мы записываем в переменную ссылку
# # на функцию и можем в будущем выполнить эту функцию, просто добавив к переменной ().
#
# print(second())


# Задание 26.1.1
# Какое значение вернёт следующая функция?:
# def custom_func(num):
# 	print("Calling function")

# - Эта функция с побочным эффектом, в ней не задан явно тип возвращаемого значения (return), поэтому вернется none.


# 26.2. Простые декораторы
# 1

# def my_decorator(func):
#     def wrapper():
#         print("Начало выполнения функции.")
#         func()
#         print("Конец выполнения функции.")
#
#     return wrapper
#
# def my_first_decorator():
#     print("Это мой первый декоратор!")
#
# my_first_decorator = my_decorator(my_first_decorator)
#
# my_first_decorator()

# 2

# def working_hours(func):
#     def wrapper():
#         if 9 <= datetime.datetime.now().hour < 18:
#             func()
#         else:
#             print("Я не пишу тесты на python, время отдыха (:-)!")
#     return wrapper
#
# @ working_hours
# def writing_tests():
#     print("Я пишу тесты на python!")

# writing_tests = working_hours(writing_tests)


# writing_tests()

# 3

# Воспользуемся удобной функцией Python - символом @ ("Синтаксический сахар"), чтобы каждый раз
# не объявлять переменную для вызова декоратора и декорируемой функции, т.е.
# вот так writing_tests = working_hours(writing_tests):

# def working_hours(func):
#     def wrapper():
#         if 9 <= datetime.datetime.now().hour < 18:
#             func()
#         else:
#             print("Я не пишу тесты на python, время отдыха!")
#     return wrapper
#
# @ working_hours # сахар, это выражение равносильно выраж-ю writing_tests = working_hours(writing_tests)
# def writing_tests():
#     print("Я пишу тесты на python!")
#
# writing_tests()

# 4
# Импортируем функцию декоратор do_twice из файла decorators.py., созданного в корневой директории этого проекта:
# @do_twice
# def test_twice():
#     print("Это вызов функции test_twice!")
#
#
# test_twice()

                                        # 26.3 Декорирование функций аргументами.

# 1
# В функцию-декортаор do_twice передали один аргумент str, но это ограничит ее использование, так как перадавать более
# одного аргумента и/или ни одного аргумента (0) в нее больше нельзя.
# @do_twice
# def test_twice(str):
#     print("Этот вызов возвращает строку {0}".format(str))
#
# test_twice()

# 2
# Следовательно, Чтобы сделать нашу функцию-декоратор универсальной, существует достаточно простое решение:
# нужно использовать *args и **kwargs внутри функции-обёртки. В этом случае наша функция будет принимать любое
# количество аргументов (включая 0) (см. файл decorators.py):

# @do_twice
# def test_twice_without_params():
#     print("Этот вызов без параметров")
#
# @do_twice
# def test_twice_2_params(str1, str2, str3):
#     print(f'В этой функции 3 параметра - {str1}, {str2}, {str3}.')
#
# @do_twice
# def test_twice(str):
#     print(f'Этот вызов возвращает строку {str}')
#
# test_twice_without_params()
#
# test_twice_2_params(1, 2, 3)
#
# test_twice('single')

# 3
# Возврат значения из функции-декоратора.
# Для возврата значения из функции-декоратора нужно из функции-обёртки в декораторе возвращать значение
# (return func(*args, **kwargs) (см. файл decorators.py):
# @do_twice
# def test_twice(str):
#     print(f'Этот вызов возвращает строку {str}')
#     return 'Done'
#
# decorated_value = test_twice('single')
# print(decorated_value)

# 4
# Интроспекция, пример реального использования декораторов.

# @do_twice
# def test_twice(str):
#     print(f'Этот вызов возвращает строку {str}')
#     return 'Done'
#
# print(test_twice.__name__)

# 5
# Функция-дебаггер (декортаор см. в файле decorators.py):

# @debug
# def age_passed(name, age=None):
#   if age is None:
#     return "Необходимо передать значение age"
#   else:
#     return "Аргументы по умолчанию заданы!"
#
# age_passed("Роман")
# age_passed("Роман", age=21)

                                        # 26.4.1 Фикстуры.

# 1

# @pytest.fixture()
# def random_data():
#     return 42
#
# def test_random_data(random_data):
#     assert random_data == 42

# 2  Фикстуры setup и teardown.

def get_key():
    # переменные email и password нужно заменить своими учетными данными
    response = requests.post(url='https://petfriends.skillfactory.ru/login',
                             data={"email": email, "pass": password})
    assert response.status_code == 200, 'Запрос выполнен неуспешно'
    assert 'Cookie' in response.request.headers, 'В запросе не передан ключ авторизации'
    return response.request.headers.get('Cookie')

def test_getAllPets(get_key):
    response = requests.get(url='https://petfriends.skillfactory.ru/api/pets',
                            headers={"Cookie": get_key})
    assert response.status_code == 200, 'Запрос выполнен неуспешно'
    assert len(response.json().get('pets')) > 0, 'Количество питомцев не соответствует ожиданиям'

