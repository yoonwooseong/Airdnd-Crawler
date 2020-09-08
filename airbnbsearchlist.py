import requests
from bs4 import BeautifulSoup

URL_BASE = "https://www.airbnb.co.kr/s/"

def get_last_page():
    set_last_page = 1
    return int(set_last_page)

def extract_room_idx(last_page, Query):
    query_infos = {}
    room_infos = []
    for page in range(last_page):
        print("Scraping the titles of page", page+1,"...")
        URL_PLACE = Query['place'] + "/homes?"
        URL_CHECKIN = "checkin=" + Query['checkin']
        URL_CHECKOUT = "&checkout=" + Query['checkout']
        URL_ADULTS = "&adults=" + Query['adults'] 

        URL = URL_BASE + URL_PLACE + URL_CHECKIN + URL_CHECKOUT + URL_ADULTS + "&children=0&infants=0"
        print(URL)
        result = requests.get(f"{URL}&items_offset={page*20}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class":"_1048zci"})
        
        for result in results:
            result_url = result.find("a")["href"]
            room_price = result.find("span", {"class":"_1p7iugi"}).get_text()
            room_idx = result_url[result_url.index('s/')+2:result_url.index('?')]
            room_info = {"room_idx":room_idx, "room_price":room_price}
            if room_info not in room_infos:
                room_infos.append(room_info)
    
        query_infos['Query'] = Query
        query_infos['room_infos'] = room_infos
    return query_infos

def get_accommodation_infos(Query):
    last_page = get_last_page()
    query_infos  = extract_room_idx(last_page, Query)
    print(query_infos)
    return query_infos

