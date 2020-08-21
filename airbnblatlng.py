import requests
from bs4 import BeautifulSoup

def Convert_to_latlng(query):
    base_url = "https://maps.googleapis.com/maps/api/geocode/xml?address="
    api_key = "본인 키 입력"
    url = base_url+query+"&key="+api_key
    result = requests.get(url)
    html = BeautifulSoup(result.text, "html.parser")

    lat = html.select("location > lat")[0].get_text()
    lng = html.select("location > lng")[0].get_text()
    latlng = {'lat':lat, 'lng':lng}
    return latlng
