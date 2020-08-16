import cx_Oracle
import os
from urllib.parse import quote_plus
from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get('https://www.airbnb.co.kr/rooms/1673711?check_in=2020-10-01&check_out=2020-10-03')
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
driver.implicitly_wait(10)
price = soup.select('._3r2zp5v')[0]


print(price)