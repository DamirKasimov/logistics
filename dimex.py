import requests
from random import randint
from selenium import webdriver
import re
import time
import pandas as pd


# функция поиска адресов, реквизитов и т.д.
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


# формируем список городов присутствия в формате '/название города/'
response = requests.get('https://www.dimex.ws/regiony-prisutstviya/novorossiysk/')
print(response.status_code)
response = response.text
indexes = find_all_indexes(response, '/regiony-prisutstviya/')
cities = []


for index in indexes:
    cities.append(str(response[index+21:index+100].split('><')[0])[:-1])
del cities[:7]


def find(cities):
    output = []
    bad_cities = []
    # перебор списка городов
    for city in cities:
        if len(output) < 200:
            # запуск браузера selenium
            browser = webdriver.Chrome('D:\\Dev\\chrome_driver\\chromedriver.exe')
            browser.get('https://www.dimex.ws/regiony-prisutstviya'+(city))
            response = requests.get('https://www.dimex.ws/regiony-prisutstviya'+(city))
            time.sleep(randint(5, 15))
            print(response.status_code)
            if response.status_code == 200:
                response = response.text
                # вызов функции для поиска поиска адреса
                indexes = find_all_indexes(response, "map-marker")
                # вызов функции для поиска поиска эл. почты
                mail_index = find_all_indexes(response, "mailto")
                # вызов функции для поиска поиска реквизитов
                entity_index = find_all_indexes(response, "ИНН/КПП")
                try:
                    # обработка адресов
                    address = (response[indexes[0]+17:indexes[0]+200].split('</'))[0]
                    # обработка телефонов
                    search_pho = re.compile('\([0-9)\)]{4}\)*\s*[0-9)\s*\-]*')
                    phones = str(set(search_pho.findall(response[indexes[0]+17:indexes[0]+2000])))
                    phones = phones.replace("\'", "")
                    phones = phones[1:-1]
                    # обработка реквизитов
                    leg_entity_inn = str((response[entity_index[0]:entity_index[0]+2000].split('</p></li>'))[0])
                    leg_entity_inn = leg_entity_inn.replace("</strong>", " ")
                    leg_entity_inn = (leg_entity_inn.replace("<strong>", " "))
                    leg_entity_inn = leg_entity_inn.replace("<br />", "")
                    leg_entity_inn = leg_entity_inn.replace("&nbsp;", "")
                    leg_entity_inn = leg_entity_inn.replace("&raquo;", "")
                    leg_entity_inn = leg_entity_inn.replace("&laquo;", " ")
                    leg_entity_inn = leg_entity_inn.replace("\r\n", " ")
                    # эл. почта
                    mail = (response[mail_index[0]+7:mail_index[0]+200].split('>'))[0][:-1]
                    # запись результата
                    output.append({'Город': str(city), 'Адрес': str(address), 'Телефоны': (phones), 'Почта': str(mail), 'Реквизиты': leg_entity_inn})
                except IndexError:
                    bad_cities.append(city)
                browser.close()
                print(bad_cities)
    return(output)


result = find(cities)
# запись в файл списка словарей с результатом
df = pd.DataFrame.from_dict(result)
df.to_excel('output.xlsx')
