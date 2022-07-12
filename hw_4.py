from lxml import html
import requests
from pprint import pprint
import pymongo
from pymongo import MongoClient


def proc_replece(value):
    value = ' '.join(value).replace('\xa0', ' ')
    return value


client = MongoClient('127.0.0.1', 27017)
db = client['ya_news']
ya_news = db.ya_news
ya_href = [i['link'] for i in ya_news.find({})]


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
url = "https://yandex.ru/news/"

session = requests.Session()
response = session.get(url, headers=headers)

dom = html.fromstring(response.text)
block = dom.xpath(
    '//div[contains(@class, "mg-card_stretching")] | //div[contains(@class, "mg-card_media-fixed-height")]')



news = []
for i in block:
    gathering = {}

    source = i.xpath('.//span[@class="mg-card-source__source"]/a/text()')
    name = i.xpath('.//h2[@class="mg-card__title"]/a/text()')
    link = i.xpath('.//h2[@class="mg-card__title"]/a/@href')
    date = i.xpath('.//span[@class="mg-card-source__time"]/text()')

    gathering['source'] = source
    gathering['name'] = proc_replece(name)
    gathering['link'] = link
    gathering['date'] = date

    if gathering['link'] in ya_href:
        continue

    news.append(gathering)


pprint(news)