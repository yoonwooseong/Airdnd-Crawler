import requests
from bs4 import BeautifulSoup

URL = "https://www.airbnb.co.kr/rooms/"


def extract_detail(accommodation_idxs):
    for room_idx in accommodation_idxs:
        print(room_idx)
        room = room_idx
        result = requests.get(f"{URL}"+room)
        soup = BeautifulSoup(result.text, "html.parser")

        results = soup.find("div",{"class","_tqmy57"})
        if results is not None:
            print(results)
        else:
            gooo = 1
            while gooo:
                result = requests.get(f"{URL}"+room)
                soup = BeautifulSoup(result.text, "html.parser")
                if results is not None:
                    print(results)
                    gooo = 0
                else:
                    print("try again")
