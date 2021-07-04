from faker import  *
import random
import string
import os
import csv
import pandas as pd
import  numpy as np
import requests


def generate_password(password_len: int = 10) -> str:
    if not isinstance(password_len, int):
        raise TypeError('Invalid Type...')

    choices = string.ascii_letters + string.digits + '#$%^'
    result = ''

    for _ in range(password_len):
        result += random.choice(choices)

    return result

#функция открытие и сохранение файла
def open_file(file) -> str:
    opw = open(file, 'r')
    txt_text = ''
    while True:
        line = opw.readline()
        if not line:
            break
        txt_text = txt_text + line
    opw.close()
    return txt_text if len(txt_text) > 0 else 'Empty file'


# 3 - домашка создание доп вариантов
# для создание регулярного пользователя мы добавим уникальный индефикатор в виде большой буквы R   в конце
# таким образом сможем отсортировать не зарегестрированных или пустых пользователей
def create_fake_name(numbers = 1) -> str:
    fake = Faker()
    f_seed = random.randint(0, 10000)
    Faker.seed(f_seed)

    return  str(fake.first_name()) + 'R'
def create_fake_phone(numbers = 1) -> str:
    fake = Faker()
    f_seed = random.randint(0, 1000)
    Faker.seed(fake)
    return  str(fake.msisdn()) + 'R'

#функция для проверка имени на корректность(без спец символов и цифр)
def check_name(name:str) -> str:
    return ''.join(i for i in name if i.isalpha()) if len(name) > 0 else 'Unknown User'

def check_number(number:str) -> str:
    return ''.join(i for i in number if i.isdigit() or i == '+') if len(number)  > 0 else '000'

#функция проверки почты,  проверяем на спец символы и отсутсие идентификатора @
def validator_for_email(email = 'example.@gmail.com'):
    def helper_delete_symbol(items:str) -> str:
        pass
    if '@' in email and email.count('@') == 1:
        print(email.split('@'))
    else:
        print(email)


def create_fake_email(numbers = 1) -> list:
    #есть два варианта решение через Faker
    # 1.  Использовать готовую функцию генерации,  которая сама будет все генерировать
    # 2.  Взять только генерацию имен и вручнуб подганять email
    # 3. Решение в одну строку с одной проверкой
    fake = Faker()
    f_seed = 0
    result = ''
    # 1 - вариант решение
    # Для создание большего рандома мы изменяем сиид в ходе выполнение
    for _ in range(0, numbers):
        Faker.seed(f_seed)
        result = result + fake.ascii_email() + '\n'
        #result.append(fake.ascii_email())
        f_seed += random.randint(0,  random.randint(500, 1000))
    return  result if len(result) > 0 else 'example@gmail.com'

    # 2 - решение
    #def helper_create_name(name: str) -> str:
    #    email = ['@gmail.com', '@gmail.com.ua', '@gmail.com.ru', '@yahoo.com', '@hotmail.com', '@info', '@ua', '@us', '@bind.com']
    #    return name.lower() + email[random.randint(0, 8)] if  isinstance(name, str) == True else 'example@gmail.com'
    #return [helper_create_name(fake.first_name()) for _ in  range(0, numbers)]

    #  3 - решение
    # return  [fake.ascii_email()  for i in range(0, numbers)]


#функция чтение и нормализации файла
#пришлось переместить файл csv в папку с проектом, по другому не находила файл
def normalize_and_calculate(path) -> str:
    #функция перевода из дюймов в сантиметры( 2.54 - это столько сантиметров в дюйме, наша константа)
    def inches_to_catm(value):
        return  value * 2.54
    #функция перевода из фунтов в кг( 0.4535923745 - это столько килограм в одном футе, наша константа)
    def pounds_to_kilogram(value):
        return  value * 0.4535923745

    path = os.path.abspath(path) # для создание универсальности получим полный нормализированный путь
    df = pd.read_csv(path) # для упрощение чтение и будущей реализации считываем с помощью pandas
    df = df.rename(columns= {' "Height(Inches)"': 'Inches', ' "Weight(Pounds)"': 'Ponds'}) # так как наши название ввдены не правильно, имеют пробелы и доп кавычки мы их переиминовали

    # 1 - вариант решение, пойдем в обход и посчитаем среднее вес и средний рост в дюймах и фунтах соотвественно, а потом умножим результат на соотвествующию константу
    # 2 - вариант решение, преобразуем все данных в метрическую систему и потом посчитаем среднее(тут тоже несколько вариантов, взять каунт и пройтись по циклы суммируя или использовать готовую функцию)


    #  1 - вариант
    #print(df.columns)
    #print(df.describe()) #  тут можно проверить результат
    #print(df['Inches'].mean() , df['Ponds'].mean() )
    return 'Сантиметры среднее : ' + str(inches_to_catm(df['Inches'].mean())) + '\n' + 'Килограммы в среднее: ' + str(pounds_to_kilogram(df['Ponds'].mean()))


    # 2 - вариант
    #df['Inches'] = df['Inches'].apply(inches_to_catm)
    #df['Ponds'] = df['Ponds'].apply(pounds_to_kilogram)
    #return  [df['Inches'].mean(), df['Ponds'].mean()]


#функция чтение и подсчета для косманавтов
def spacemarin_count(path = 'http://api.open-notify.org/astros.json') -> str:
    r = requests.get(path)
    return r.json()["number"]




