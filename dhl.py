import requests
import time
from random import randint
from selenium import webdriver
import re
import pandas as pd


x = ('Курск', 'Магнитогорск', 'Махачкала', 'Мытищи', 'Нижневартовск',
     'Астрахань', 'Белгород', 'Брянск', 'Владимир', 'Волжский',
     'Грозный', 'Йошкар-Ола', 'Мурманск', 'Кемерово', 'Кострома',
     'Новороссийск', 'Пенза', 'Петрозаводск', 'Саранск', 'Саратов',
     'Симферополь', 'Смоленск', 'Ставрополь', 'Сыктывкар', 'Тамбов', 'Тула',
     'Улан-Удэ', 'Ульяновск', 'Чебоксары', 'Якутск',
     'Ярославль', 'Волгоград', 'Казань', 'Ростов-на-Дону', 'Челябинск',
     'Самара', 'Санкт-Петербург')


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
    phones={}
    count = 0
    wrong_cities=[]
    output=[]
    for city in x:
        if len(output) < 12:
            browser = webdriver.Chrome('D:\Dev\chrome_driver\chromedriver.exe')
            browser.get('https://yandex.ru/search/?text=dhl+'+(city)+'&lr=37135')
            count +=1
            print(f'город {count} из {len(x)}')
            response = requests.get('https://yandex.ru/search/?text=dhl+'+(city)+'&lr=37135')
            print(response.status_code)
            response= response.text
            print(len(response))
            if response.find('aptcha') > 0:
                print('Kaptcha')
            indexes = find_all_indexes(response,'дрес организации')
            search = re.compile('\+7\s\(\d\d\d[0-9)\s\-\)]{11}')
            print((list(set(search.findall(response)))))
            new_phones = [x for x in ((set(search.findall(response)))) if not x.startswith("+7 (495)") ]
            new_phones = (str(new_phones))[1:-1]
            new_phones = (new_phones).replace("\'", "")
            print(new_phones)
            phones = (str(set(search.findall(response))))[1:-1]
            phones = phones.replace("\'", "")
            try:
                address = (response[indexes[0]+18:indexes[0]+100].split('"')[0])
            except IndexError:
                print(f'{city} мимо')
                wrong_cities.append(city)
                address = ('нет офиса?')
            time.sleep(randint(20, 50))
            browser.close()
            output.append({'Город': str(city), 'Адрес': str(address), 'Телефоны': (new_phones)})
            print(f'плохие города {wrong_cities}')
    return output


result = (find(x))
df = pd.DataFrame.from_dict(result)
df.to_excel('d:/Dev/dhl/output_dhl.xlsx')
