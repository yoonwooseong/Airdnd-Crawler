import cx_Oracle
import os
from urllib.parse import quote_plus
from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
driver.get('https://www.airbnb.co.kr/rooms/1673711?check_in=2020-10-01&check_out=2020-10-03')

price = driver.find_elements_by_class_name('_pgfqnw')
price2 = price.find_elements_by_tag_name('span')[0].find_elements_by_tag_name('span')
print(price2)