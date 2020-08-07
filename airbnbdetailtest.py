import requests
from bs4 import BeautifulSoup

URL = "https://www.airbnb.co.kr/rooms/6064582?location=%EA%B4%8C&previous_page_section_name=1000&federated_search_id=f3d68a91-b8de-45ea-bdaa-a313a4a37ec3"


def extract_detail():

    result = requests.get(URL)
    print(result)
    soup = BeautifulSoup(result.text, "html.parser")

    results = soup.find("div",{"class","_tqmy57"})
    print(results)
        
extract_detail()

