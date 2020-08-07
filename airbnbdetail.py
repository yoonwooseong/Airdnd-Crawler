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
            while True:
                result = requests.get(f"{URL}"+room)
                soup = BeautifulSoup(result.text, "html.parser")
                if results is not None:
                    print(results)
                    break;
                else:
                    print("try again")
