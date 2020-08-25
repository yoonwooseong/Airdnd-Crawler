import pymysql
import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import quote_plus
from airbnblatlng import Convert_to_latlng

#####한글깨짐 방지###### 
os.environ["NLS_LANG"] = ".AL32UTF8"
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

# DB와 연결된 코드
conn = pymysql.connect(host = '52.79.141.237', user = 'mysqluser', password = '1111', db = 'AirdndDB', charset = 'utf8')

URL_BASE = "https://www.airbnb.co.kr/rooms/"
URL_PARAM = "?adults=1&location=%EA%B4%8C&check_in=2020-10-01&check_out=2020-10-03&source_impression_id=p3_1598247923_ydg6avDRJAlC0ViV"
take_out_start_index = 0
db = conn.cursor()

def check_room_idx_in_DB(): 
    sql_select = 'select room_idx from airdnd_room_test'
    db.execute(sql_select)
    room_nums_in_DB = db.fetchall()
    return room_nums_in_DB

def insert_room_data_in_MysqlDB(data):
    print(data['room_idx'])
    #DB에 접근하기 위한 쿼리문
    sql_insert =  'insert into airdnd_room_test (room_idx, room_name, room_price, room_score, room_review_num, room_type, room_option) VALUES (%s, %s, %s, %s, %s, %s, %s)'
    val = (data['room_idx'], data['main_title'].encode('utf8').decode('utf8'), data['price'],
                    data['room_score'].encode('utf8').decode('utf8'), data['room_review_num'].encode('utf8').decode('utf8'),
                    data['sub_title'].encode('utf8').decode('utf8'), data['room_option'].encode('utf8').decode('utf8'))
    
    db.execute(sql_insert, val)
    conn.commit()
    print("DB저장 성공")

def extract_pictures(room_pictures):
    picture = []
    i = 0
    for pictures in room_pictures:
        room_picture = pictures.find("img").attrs['src']
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

def scrape_page(URL, room_idx, price):
    while True:
        driver = webdriver.Chrome('C:/Wooseong/web scraper/chromedriver') #, chrome_options=options
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
        abc = results.select_one('div._e296pg')
        bc = abc.select_one('div._tqmy57')

        if price.find('할') == -1:
            price = price[price.find('₩')+1:]
        else:
            price = price[price.find('₩')+1:price.find('할')]
        int_price = int(price.replace(',',''))
        
        #크롤링 소스 가져오기
        if bc is not None:
            main_title = abc.find("div", {"class","_mbmcsn"}).find("h1").get_text(strip=True)
            print()
            print("URL : ",URL)
            print('main_title : ',main_title)
            addr = results.find("a", {"class","_5twioja"}).get_text()
            print('addr : ', addr)
            latlng = Convert_to_latlng(addr)
            print('latlng : ' , latlng)
            # None일때 오류 방지
            room_scores = abc.find("span", {"class","_1jpdmc0"})
            if room_scores is not None:
                room_score = room_scores.get_text(strip=True)
            else:
                room_score = "0.00"
            print("room_score : ",room_score)
            room_review_nums = abc.find("span", {"class","_1sqnphj"})
            if room_review_nums is not None:
                room_review_num = room_review_nums.get_text(strip=True)
            else:
                room_review_num = "(0)"
            print("room_review_num :", room_review_num)
            try:
                soup.select('._nu65sd')[1].find("span")
                isSuperHost = True
            except:
                isSuperHost = False
            print("isSuperHost : ", isSuperHost)
            sub_titles , room_options = results.find("div", {"class", "_tqmy57"}).find_all("div", recursive=False)
            sub_title = sub_titles.get_text(strip=True)
            room_option = room_options.get_text(strip=True)
            print("sub, option : ", sub_title, room_option)
            #sub_title = ""
            #room_option = ""
            room_notice_title = abc.select('div._1044tk8 > div._1mqc21n > div._1qsawv5')
            room_notice_cont = abc.select('div._1044tk8 > div._1mqc21n > div._1jlr81g')
            
            room_pictures = abc.find_all("div", {"class", "_1h6n1zu"})
            room_bed_sort = abc.select('div._9342og > div._1auxwog')
            room_bed_sort_cont = abc.select('div._9342og > div._1a5glfg')
            room_convenient_facilities = abc.select('div._19xnuo97 > div._1nlbjeu')
            #room_scores_sort = abc.select('div._a3qxec > div._y1ba89')
            #room_scores_sort_num = abc.select('div._a3qxec > div._bgq2leu > div._4oybiu')
            room_reviews = abc.select('div._50mnu4')
            room_notice = take_out_list_two(room_notice_title, room_notice_cont)
            room_bed = take_out_list_two(room_bed_sort, room_bed_sort_cont)
            #room_rating = take_out_list_two(room_scores_sort, room_scores_sort_num)
            room_rating = {}
            room_convenient_facility = take_out_list_get_text_div(room_convenient_facilities)
            room_review = take_out_list_get_review(room_reviews)
            picture = extract_pictures(room_pictures)

            #reqeust로 출력------------------------------------------------------------

            room_loc_info = abc.select_one('div._1cvivhm > div._1byskwn > div._vd6w38n')
            #만약 지역 설명이 없으면
            if room_loc_info is not None:
                room_loc_info_cont = "location content is None"
                room_loc_info_dist = room_loc_info.select('div._dc0jge')
            else:
                room_loc_info_cont = abc.find_all("div",{"class","_162hp8xh"})[-2].select_one('div._1y6fhhr > span').get_text()
                #.select_one('._1byskwn > ._162hp8xh > section > span > ._cfvh61 > ._1y6fhhr').find("span").get_text() #얘는 context 한개
                room_loc_info_dist = abc.find_all("div",{"class","_dc0jge"})#.select_one('._162hp8xh > ._17k42na > ._1btxexp').select('._dc0jge') #얘는 결과값 여러개 = 리스트
            
            try:
                room_host = abc.select_one('div._1y6fhhr').find("span").get_text()
            except:
                room_host = ""
            print("room_host : " , room_host)

            room_rules_prev = abc.select('div._m9x7bnz > div._f42bxt')
            try:
                room_use_rules = room_rules_prev[0].select('div._ud8a1c > div._u827kd')
                room_safety = room_rules_prev[1].select('div._ud8a1c > div._u827kd')
            except:
                room_use_rules = []
                room_safety = []
            

            print("room_loc_info_cont : ", room_loc_info_cont)
            room_loc_info_distance = take_out_list_get_text_pre(room_loc_info_dist)
            room_use_rule = take_out_list_get_text_span(room_use_rules)
            room_safety_rule = take_out_list_get_text_span(room_safety)

            data = {'URL':URL,'main_title':main_title, 'isSuperHost':isSuperHost, 'addr':addr, 'latlng':latlng, 'room_idx':room_idx, 'price':int_price,
                    'room_score':room_score, 'room_review_num':room_review_num, 'sub_title':sub_title,
                    'room_option':room_option, 'room_host':room_host, 'room_loc_info_cont':room_loc_info_cont,
                    'picture':picture, 'room_convenient_facility':room_convenient_facility , 'room_use_rule':room_use_rule,
                    'room_safety_rule':room_safety_rule , 'room_loc_info_distance':room_loc_info_distance,
                    'room_notice':room_notice, 'room_bed':room_bed, 'room_rating':room_rating}
            data['room_reviews'] = room_review
            
            driver.quit()
            return data
            
        else:
            
            print("try again..")
            driver.quit()


def extract_detail(accommodation_infos):
    room_nums_in_DB = check_room_idx_in_DB()
    for room_info in accommodation_infos:
        room_idx = room_info["room_idx"]

        #방번호를 검색해 DB에 있는지 체크
        if tuple([int(room_idx)]) not in room_nums_in_DB:
            price = room_info["room_price"]
            URL = URL_BASE+room_idx+URL_PARAM
            data = scrape_page(URL, room_idx, price)
            insert_room_data_in_MysqlDB(data)
        else:
            print("방번호 ", room_idx, "는 이미 저장되어 있습니다.")

    db.close()
    conn.close()