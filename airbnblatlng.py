import requests
from bs4 import BeautifulSoup

def Convert_to_latlng(query):
    base_url = "https://maps.googleapis.com/maps/api/geocode/xml?address="
    api_key = "AIzaSyBuSzbqsUUg0qzcvTAv3L_XkxoxXFyeAQ4"
    url = base_url+query+"&key="+api_key
    result = requests.get(url)
    html = BeautifulSoup(result.text, "html.parser")

    lat = html.select("location > lat")[0].get_text()
    lng = html.select("location > lng")[0].get_text()
    location = {'lat':lat, 'lng':lng}
    return location

location = Convert_to_latlng("의정부시")
print(location)
