import pandas as pd
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import json
import pandas as pd
import openpyxl
import pymongo
from pymongo import MongoClient
from pymongo import errors


client = MongoClient('127.0.0.1', 27017)
db = client['hh']
vacantions = db.vacantions

vacantions_href = [i['href'] for i in vacantions.find({})]




def processing_salary(value):
    if not value:
        return value
    replacement = value.text.replace('\u202f', '')
    replacement = replacement.split()

    data = {}
    if replacement[0] == "от" and len(replacement) == 3:
        data['from'] = int(replacement[1])
        data['to'] = None
        data['currency'] = replacement[-1]
    elif replacement[0] == "до" and len(replacement) == 3:
        data['from'] = None
        data['to'] = int(replacement[1])
        data['currency'] = replacement[-1]
    else:
        data['from'] = int(replacement[0])
        data['to'] = int(replacement[2])
        data['currency'] = replacement[-1]

    return data


headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
url = "https://samara.hh.ru/search/vacancy?&from=suggest_post&fromSearchLine=true&area=78"
params = {'text': "python", "items_on_page": '20'}

session = requests.Session()
response = session.get(url, headers=headers, params=params)

dom = BeautifulSoup(response.text, 'html.parser')
tags = dom.find_all('div', {'class': 'vacancy-serp-item-body__main-info'})


tags_list = []

i = 0
while tags:

    if not i:
        pass
    else:
        params['page'] = i
        response = session.get(url, params=params, headers=headers)
        dom = BeautifulSoup(response.text, 'html.parser')
        tags = dom.find_all('div', {'class': 'vacancy-serp-item-body__main-info'})
    if not response.ok:
        break
    for tag in tags:
        tags_data = {}
        name = tag.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
        href = url + name.get('href') #tag.get('href')
        salary = tag.find("span", {'data-qa': "vacancy-serp__vacancy-compensation"})

        tags_data['name'] = name.text
        tags_data['href'] = href
        tags_data['salary'] = processing_salary(salary)
        tags_data['url'] = 'https://hh.ru'
        tags_list.append(tags_data)

        # for item in vacantions.find({}):
        #     if tags_data["href"] == item["href"]:
        #         i += 1
        #         continue

        #Доработка 1 (если всё верно понял)
        if tags_data['href'] in vacantions_href:
            continue

        vacantions.insert_one(tags_data)

    i += 1

# pprint(tags_list)

client.close()




# Доработка 2 не удалась, пытался изначальный словарь salary преобразовать в список; искать с помощью$gt и $or, не вышло
# def find_salary(value):
#     value = int(value)
#     end_data = []
#
#     for i in vacantions.find({}):
#         pass
#
#
#     return end_data

#
# print(find_salary(10000))
