from ast import And
import requests
import time
from random import randint
from selenium import webdriver
import re
import pandas as pd


# список городов возможного присутствия
x = ('Курск', 'Магнитогорск', 'Махачкала', 'Мытищи', 'Нижневартовск',
     'Астрахань', 'Белгород', 'Брянск', 'Владимир', 'Волжский',
     'Грозный', 'Йошкар-Ола', 'Мурманск', 'Кемерово', 'Кострома',
     'Новороссийск', 'Пенза', 'Петрозаводск', 'Саранск', 'Саратов',
     'Симферополь', 'Смоленск', 'Ставрополь', 'Сыктывкар', 'Тамбов', 'Тула',
     'Улан-Удэ', 'Ульяновск', 'Чебоксары', 'Якутск',
     'Ярославль', 'Волгоград', 'Казань', 'Ростов-на-Дону', 'Челябинск',
     'Самара', 'Санкт-Петербург')


# функция поиска адресов
def find_all_indexes(input_str, search_str):
    l1 = []
    length = len(input_str)
    index = 0
    while index < length:
        i = input_str.find(search_str, index)
        if i == -1:
            return l1
        l1.append(i)
        index = i + 1
    return l1


def find(x):
    phones = {}
    count = 0
    # список городов, в которых не оказалось офиса
    wrong_cities = []
    output = []
    # перебор заданного списка городов
    for city in x:
        if len(output) < 12:
            # запуск браузера selenium
            browser = webdriver.Chrome('D:\\Dev\\chrome_driver\\chromedriver.exe')
            browser.get('https://yandex.ru/search/?text=dhl+'+(city))
            # для отслеживания прогресса
            count += 1
            print(f'город {count} из {len(x)}')
            response = requests.get('https://yandex.ru/search/?text=dhl+'+(city))
            print(response.status_code)
            response = response.text
            if response.find('aptcha') > 0:
                print('Kaptcha')
            # вызов функции поиска всех вхождений в текст response'а
            indexes = find_all_indexes(response, 'дрес организации')
            # ищем и обрабатываем телефоны с помощью regex
            search = re.compile('\s\(\d\d\d[\) \d][\) \d][\s \d]\d\d\-\d\d-\d\d')
            new_phones = [x for x in ((set(search.findall(response)))) if not x.startswith(' (800)') and not x.startswith(' (495)')]
            new_phones = (str(new_phones))[1:-1]
            new_phones = (new_phones).replace("\'", "")
            phones = (str(set(search.findall(response))))[1:-1]
            # ищем и обрабатываем адреса
            try:
                address = (response[indexes[0]+18:indexes[0]+100].split('"')[0])
            # в случае ошибки -- офиса нет
            except IndexError:
                print(f'{city} мимо')
                wrong_cities.append(city)
                address = ('нет офиса?')
            time.sleep(randint(20, 50))
            browser.close()
            # запись результата
            output.append({'Город': str(city), 'Адрес': str(address), 'Телефоны': (new_phones)})
            print(f'плохие города {wrong_cities}')
    return output


result = (find(x))
# запись в файл списка словарей с результатом
df = pd.DataFrame.from_dict(result)
df.to_excel('d:/Dev/dhl/output_dhl.xlsx')
