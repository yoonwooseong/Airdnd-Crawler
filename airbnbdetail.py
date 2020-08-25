import pymysql
import os
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import quote_plus
from airbnblatlng import Convert_to_latlng

#####한글깨짐 방지###### 
os.environ["NLS_LANG"] = ".AL32UTF8"

# DB와 연결된 코드
conn = pymysql.connect(host = '52.79.141.237', user = 'mysqluser', password = '1111', db = 'AirdndDB', charset = 'utf8mb4', use_unicode=True)

URL_BASE = "https://www.airbnb.co.kr/rooms/"
#URL_PARAM = "?adults=1&location=%EA%B4%8C&check_in=2020-10-01&check_out=2020-10-03&source_impression_id=p3_1598247923_ydg6avDRJAlC0ViV"
take_out_start_index = 0
db = conn.cursor()

def check_room_idx_in_DB(): 
    sql_select = 'select home_idx from airdnd_home'
    db.execute(sql_select)
    room_nums_in_DB = db.fetchall()
    return room_nums_in_DB

def insert_room_data_in_MysqlDB(data):
    print(data['room_idx'])
    #DB에 접근하기 위한 쿼리문
    sql_insert =  'insert into airdnd_home (home_idx, place, title, score, review_num, isSuperHost, addr, lat, lng, sub_title, filter_max_person, filter_bedroom, filter_bed, filter_bathroom, price, host_notice, loc_info) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    val = (data['room_idx'], data['place'].encode('utf8').decode('utf8'), data['main_title'].encode('utf8').decode('utf8'),
            data['room_score'], data['room_review_num'], data['isSuperHost'], data['addr'].encode('utf8').decode('utf8'),
            data['latlng']['lat'], data['latlng']['lng'], data['sub_title'].encode('utf8').decode('utf8'), data['room_filter_max_person'],
            data['room_filter_bedroom'], data['room_filter_bed'], data['room_filter_bathroom'], data['price'],
            data['room_host'].encode('utf8').decode('utf8'), data['room_loc_info_cont'].encode('utf8').decode('utf8'))
    db.execute(sql_insert, val)
    conn.commit()
    print("DB저장 성공")

def extract_pictures(room_pictures):
    picture = []
    i = 0
    for pictures in room_pictures:
        try:
            room_picture = pictures.find("img").attrs['src']
        except:
            room_picture = "None"
        picture.append(room_picture)
        i += 1
        if i == 5:
            print("picture : ", picture)
            return picture

def take_out_list(extracted_list):
    data_list = []
    for e_list in extracted_list:
        data_list.append(e_list.string)
    print("data_list : ", data_list)         
    return data_list

def take_out_list_get_text_pre(extracted_list):
    data_list = []
    for e_list in extracted_list:
        nearby_attraction, attraction_distance = e_list.find_all("div")            
        data_list.append([nearby_attraction.string, attraction_distance.string])
    print("data_list : ", data_list)  
    return data_list

def take_out_list_get_review(extracted_list):
    data_list = []
    for e_list in extracted_list:               
        room_reviews_name_date = e_list.select_one('div._1oy2hpi').find("div",{"class", "_1lc9bb6"}, recursive=False).get_text()
        room_reviews_name = room_reviews_name_date[:room_reviews_name_date.find("년 ")-4]
        room_reviews_date = e_list.select_one('div._1oy2hpi > div._1lc9bb6 > div').string
        room_reviews_cont = e_list.select_one('div._1y6fhhr > span').get_text()

        data_dict = {'room_reviews_name':room_reviews_name, 'room_reviews_date':room_reviews_date ,'room_reviews_cont':room_reviews_cont}
        data_list.append(data_dict)
    print("reviews : ", data_list)  
    return data_list

def take_out_list_get_text_div(extracted_list):
    data_list = []
    for e_list in extracted_list:               
        data_list.append(e_list.find("div").get_text())
    print("data_list : ", data_list)
    return data_list

def take_out_list_get_text_span(extracted_list):
    data_list = []
    for e_list in extracted_list:               
        data_list.append(e_list.find("span", recursive=False).get_text())
    print("data_list : ", data_list)  
    return data_list

def take_out_list_two(title, content):
    data_dict = {}
    take_out_start_index = 0
    for f_list in title:               
        data_dict[take_out_start_index] = [f_list.string, content[take_out_start_index].string]
        take_out_start_index += 1
    take_out_start_index = 0
    print("data_dict : ", data_dict)  
    return data_dict

def scrape_page(URL, room_idx, price, place):
    while True:
        driver = webdriver.Chrome('C:/Wooseong/web scraper/chromedriver')
        driver.implicitly_wait(3)
        driver.get(URL)
        time.sleep(3)
        driver.implicitly_wait(15)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        html = driver.page_source
        time.sleep(3)
        soup = BeautifulSoup(html, "html.parser")
        
        results = soup.select_one('body.with-new-header')
        main_container = results.select_one('div._e296pg')
        load_test = main_container.select_one('div._tqmy57')

        if price.find('할') == -1:
            price = price[price.find('₩')+1:]
        else:
            price = price[price.find('₩')+1:price.find('할')]
        int_price = int(price.replace(',',''))
        
        #크롤링 소스 가져오기
        if load_test is not None:
            main_title = main_container.find("div", {"class","_mbmcsn"}).find("h1").get_text(strip=True)
            addr = results.find("a", {"class","_5twioja"}).get_text()
            latlng = Convert_to_latlng(addr) #Google geocording API 적용 함수
            
            # None일때 오류 방지
            room_scores = main_container.find("span", {"class","_1jpdmc0"})
            if room_scores is not None:
                room_score = room_scores.get_text(strip=True)
                room_score = float(room_score)
            else:
                room_score = 0.00
            room_review_nums = main_container.find("span", {"class","_1sqnphj"})
            if room_review_nums is not None:
                room_review_num = room_review_nums.get_text(strip=True)
                room_review_num2 = str(room_review_num).replace("(", "").replace(")", "")
                room_review_num = int(room_review_num2)
            else:
                room_review_num = 0

            try:
                soup.select('._nu65sd')[1].find("span")
                isSuperHost = True
            except:
                isSuperHost = False
            sub_titles , room_options = results.find("div", {"class", "_tqmy57"}).find_all("div", recursive=False)
            sub_title = sub_titles.get_text(strip=True)
            room_option = room_options.get_text(strip=True)
            room_filter = room_option.split('·')
            room_max_person = room_filter[0]
            room_filter_max_person = int(room_max_person[room_max_person.find('최대 인원 ')+6:room_max_person.find('명')])
            room_bedroom = room_filter[1]
            room_filter_bedroom = int(room_bedroom[room_bedroom.find('침실 ')+3:room_bedroom.find('개')])
            room_bed = room_filter[2]
            room_filter_bed = int(room_bed[room_bed.find('침대 ')+3:room_bed.find('개')])
            room_bathroom = room_filter[3]
            room_filter_bathroom = float(room_bathroom[room_bathroom.find('욕실 ')+3:room_bathroom.find('개')])

            room_pictures = main_container.find_all("div", {"class", "_1h6n1zu"})
            room_notice_title = main_container.select('div._1044tk8 > div._1mqc21n > div._1qsawv5')
            room_notice_cont = main_container.select('div._1044tk8 > div._1mqc21n > div._1jlr81g')
            try:
                room_host = main_container.select_one('div._1y6fhhr').find("span").get_text()
            except:
                room_host = ""

            room_loc_info = main_container.select_one('div._1cvivhm > div._1byskwn > div._vd6w38n')
            #만약 지역 설명이 없이 주변 명소 거리만 나온다면
            if room_loc_info is not None:
                room_loc_info_cont = "location content is None"
                room_loc_info_dist = room_loc_info.select('div._dc0jge')
            else:
                room_loc_info_cont = main_container.find_all("div",{"class","_162hp8xh"})[-2].select_one('div._1y6fhhr > span').get_text()
                room_loc_info_dist = main_container.find_all("div",{"class","_dc0jge"})
            
            room_bed_sort = main_container.select('div._9342og > div._1auxwog')
            room_bed_sort_cont = main_container.select('div._9342og > div._1a5glfg')
            room_convenient_facilities = main_container.select('div._19xnuo97 > div._1nlbjeu')
            room_reviews = main_container.select('div._50mnu4')
            room_rules_prev = main_container.select('div._m9x7bnz > div._f42bxt')
            try:
                room_use_rules = room_rules_prev[0].select('div._ud8a1c > div._u827kd')
                room_safety = room_rules_prev[1].select('div._ud8a1c > div._u827kd')
            except:
                room_use_rules = []
                room_safety = []

            # 세부 별점
            # room_scores_sort = abc.select('div._a3qxec > div._y1ba89')
            # room_scores_sort_num = abc.select('div._a3qxec > div._bgq2leu > div._4oybiu')
            # room_rating = take_out_list_two(room_scores_sort, room_scores_sort_num)
            print()
            print("URL : ",URL)
            print('main_title : ',main_title)
            print('addr : ', addr)
            print('latlng : ' , latlng)
            print("room_score : ", room_score)
            print("room_review_num :", room_review_num)
            print("isSuperHost : ", isSuperHost)
            print("sub_title : ", sub_title)
            print("option : ",room_filter_max_person , room_filter_bedroom, room_filter_bed, room_filter_bathroom)
            picture = extract_pictures(room_pictures)
            room_notice = take_out_list_two(room_notice_title, room_notice_cont)
            room_bed = take_out_list_two(room_bed_sort, room_bed_sort_cont)
            room_rating = {}
            room_convenient_facility = take_out_list_get_text_div(room_convenient_facilities)
            room_review = take_out_list_get_review(room_reviews)
            print("room_host : " , room_host)
            print("room_loc_info_cont : ", room_loc_info_cont)
            room_loc_info_distance = take_out_list_get_text_pre(room_loc_info_dist)
            room_use_rule = take_out_list_get_text_span(room_use_rules)
            room_safety_rule = take_out_list_get_text_span(room_safety)
            print()

            data = {'URL':URL,'main_title':main_title, 'isSuperHost':isSuperHost, 'addr':addr, 'latlng':latlng, 'room_idx':room_idx, 'price':int_price,
                    'room_score':room_score, 'room_review_num':room_review_num, 'sub_title':sub_title, 'room_filter_max_person':room_filter_max_person,
                    'room_filter_bedroom':room_filter_bedroom, 'room_filter_bed':room_filter_bed, 'room_filter_bathroom':room_filter_bathroom, 'room_host':room_host, 
                    'room_loc_info_cont':room_loc_info_cont, 'picture':picture, 'room_convenient_facility':room_convenient_facility, 'room_use_rule':room_use_rule,
                    'room_safety_rule':room_safety_rule , 'room_loc_info_distance':room_loc_info_distance, 'place':place,
                    'room_notice':room_notice, 'room_bed':room_bed, 'room_rating':room_rating}
            data['room_reviews'] = room_review
            driver.quit()
            return data
            
        else:
            print("try again..")
            driver.quit()


def extract_detail(accommodation_infos):
    room_nums_in_DB = check_room_idx_in_DB()
    Query = accommodation_infos['Query']
    place = Query['place']
    checkin = Query['checkin']
    checkout = Query['checkout']
    adults = Query['adults']

    for room_info in accommodation_infos['room_infos']:
        room_idx = room_info["room_idx"]

        #방번호를 검색해 DB에 있는지 체크
        if tuple([int(room_idx)]) not in room_nums_in_DB:
            price = room_info["room_price"]
            #URL = URL_BASE+room_idx+URL_PARAM
            URL = URL_BASE+room_idx+"?adults="+adults+"&location="+place+"&check_in="+checkin+"&check_out="+checkout+"&source_impression_id=p3_1598247923_ydg6avDRJAlC0ViV"
            data = scrape_page(URL, room_idx, price, place)
            insert_room_data_in_MysqlDB(data)
        else:
            print(" * 방번호 ", room_idx, "는 이미 저장되어 있습니다.")

    db.close()
    conn.close()