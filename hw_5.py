from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from itertools import zip_longest
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['mvideo']
trends = db.trends
trends_hrefs = [i['href'] for i in trends.find({})]


s = Service("./chromedriver")
options = Options()
options.add_argument("start-maximized")
driver = webdriver.Chrome(service=s, options=options)
driver.implicitly_wait(10)
url = "https://www.mvideo.ru/"
driver.get(url)

#захардкодил(1)
step = 600
while True:
        try:

            driver.execute_script(f"window.scrollTo(0, window.scrollY + {step})")
            button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@class="tab-button ng-star-inserted"]'))
            )
            actions = ActionChains(driver)
            actions.move_to_element(button)
            actions.perform()
            button.click()
            driver.execute_script(f"window.scrollTo(0, window.scrollY + {step})")
            break
        except:
            step += 300
            continue

#захардкодил(2)
items = driver.find_elements(By.XPATH, '//mvid-carousel[@class="carusel ng-star-inserted"]//div[@class="product-mini-card__name ng-star-inserted"]')
prices = driver.find_elements(By.XPATH, '//mvid-carousel[@class="carusel ng-star-inserted"]//div[@class="price price--mini ng-star-inserted"]/span[@class="price__main-value"]')
links = driver.find_elements(By.XPATH, '//mvid-carousel[@class="carusel ng-star-inserted"]//div[@class="title"]/a')

for item, price, link in zip_longest(items, prices, links, fillvalue='None'):
    products = {}

    products['item'] = item.text
    products['price'] = price.text
    products['href'] = link.get_attribute('href')

    pprint(products)

    trends.insert_one(products)













