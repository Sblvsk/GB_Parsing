# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancies2007


    def process_item(self, item, spider):
        item['salary'] = self.process_salary(item['salary'])
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def process_salary(self, value):
        # if value[0] == "з/п не указана":
        #     min = None
        #     max = None
        #     cur = None
        if (value[0] == 'от' or value[0] == 'до') and value[2] == ' ':
            min = int(value[1].replace('\xa0', ''))
            max = None
            cur = value[-3]
        elif value[4] == ' ' and value[6] == ' ':
            min = int(value[1].replace('\xa0', ''))
            max = int(value[3].replace('\xa0', ''))
            cur = value[-3]
        else:
            min = None
            max = None
            cur = None

        return min, max, cur
