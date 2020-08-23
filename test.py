import requests
from bs4 import BeautifulSoup

URL_BASE = "https://www.airbnb.co.kr/rooms/39804170?check_in=2020-10-01&check_out=2020-10-03"

result = requests.get(URL_BASE)
soup = BeautifulSoup(result.text, "html.parser")
results = soup.select('.list_theme_wrap')
print(soup)
print(results)
