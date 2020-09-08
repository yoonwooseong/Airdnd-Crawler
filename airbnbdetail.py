import pymysql
import os
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import quote_plus
from airbnblatlng import Convert_to_latlng
from airbnbsql import check_room_idx_in_DB, insert_room_data_in_MysqlDB, insert_room_data_in_airdnd_home_picture, insert_room_data_in_airdnd_home_notice
from airbnbsql import insert_room_data_in_airdnd_home_bed, insert_room_data_in_airdnd_home_convenient_facility, insert_room_data_in_airdnd_home_review, insert_room_data_in_airdnd_home_attractions_distance
from airbnbsql import insert_room_data_in_airdnd_home_use_rule, insert_room_data_in_airdnd_home_safety_rule, insert_room_data_in_airdnd_host

#####한글깨짐 방지###### 
os.environ["NLS_LANG"] = ".AL32UTF8"

# DB와 연결된 코드
conn = pymysql.connect(host = '52.79.141.237', user = 'mysqluser', password = '1111', db = 'AirdndDB', charset = 'utf8mb4', use_unicode=True)

URL_BASE = "https://www.airbnb.co.kr/rooms/"
URL_PARAM = "?adults=1&location=%EA%B4%8C&check_in=2020-10-01&check_out=2020-10-03&source_impression_id=p3_1598247923_ydg6avDRJAlC0ViV"
take_out_start_index = 0
db = conn.cursor()

def extract_pictures(room_idx, room_pictures):
    picture = []
    i = 0
    for pictures in room_pictures:
        try:
            room_picture = pictures.find("img").attrs['src']
        except:
            room_picture = "None"
        insert_room_data_in_airdnd_home_picture(room_idx, room_picture)
        picture.append(room_picture)
        i += 1
        if i == 5:
            print("picture : ", picture)
            return picture

def extract_home_notice(room_idx, notice_sort, content, notice_icon):
    data_out_list = []
    take_out_start_index = 0
    print("길이오류 : ",len(notice_sort),len(content),len(notice_icon))
    for f_list in notice_sort:
        try:
            bring_notice_icon = notice_icon[take_out_start_index].select_one('path').attrs['d']
        except:
            bring_notice_icon = notice_icon[take_out_start_index].select_one('g > path').attrs['d']
        data_in_list = [f_list.string, content[take_out_start_index].get_text().replace("자세히 알아보기",""), bring_notice_icon]
        insert_room_data_in_airdnd_home_notice(room_idx, f_list.string, content[take_out_start_index].get_text().replace("자세히 알아보기",""), bring_notice_icon)
        data_out_list.append(data_in_list)
        take_out_start_index += 1
    take_out_start_index = 0
    print("data_list : ", data_out_list)  
    return data_out_list

def extract_home_bed(room_idx, bed_sort, content, bed_sort_icon): #print(room_bed_sort_icon[0].select_one('svg > path').attrs['d'])
    data_out_list = []
    take_out_start_index = 0
    icon_str = ""
    for f_list in bed_sort:
        for icon_list in bed_sort_icon[take_out_start_index].select('span._14tkmhr'):
            icon_str += icon_list.select_one('svg > path').attrs['d'] + "/"
        data_in_list = [f_list.string, content[take_out_start_index].string, icon_str]
        insert_room_data_in_airdnd_home_bed(room_idx, f_list.string, content[take_out_start_index].string, icon_str)
        data_out_list.append(data_in_list)
        take_out_start_index += 1
    take_out_start_index = 0
    print("data_list : ", data_out_list)  
    return data_out_list

def extract_convenient_facility(room_idx, convenient_facilities):
    data_list = []

    for e_list in convenient_facilities:
        try:
            convenient_facilitiy = e_list.find("div",{"class","_1nlbjeu"}).find("div").get_text()
            room_convenient_facility_icon = e_list.select_one('div._yp1t7a > svg > path').attrs['d']    
        except:
            convenient_facilitiy = e_list.find("div",{"class","_1nlbjeu"}).find("div").find("span",{"class","_krjbj"}).get_text()
            room_convenient_facility_icon = e_list.select_one('div._13tgo6a4 > svg > path').attrs['d']
        insert_room_data_in_airdnd_home_convenient_facility(room_idx, convenient_facilitiy, room_convenient_facility_icon)         
        data_list.append([convenient_facilitiy, room_convenient_facility_icon])
    return data_list

def extract_review(room_idx, extracted_list, room_rating):
    data_list = []
    for e_list in extracted_list:               
        room_reviews_name_date = e_list.select_one('div._1oy2hpi').find("div",{"class", "_1lc9bb6"}, recursive=False).get_text()
        room_reviews_name = room_reviews_name_date[:room_reviews_name_date.find("년 ")-4]
        room_reviews_date = e_list.select_one('div._1oy2hpi > div._1lc9bb6 > div').string
        room_reviews_cont = e_list.select_one('div._1y6fhhr > span').get_text()

        room_cleanliness = room_rating[0]
        room_accuracy = room_rating[1]
        room_communication = room_rating[2]
        room_position = room_rating[3]
        room_checkin = room_rating[4]
        room_cost_effectiveness = room_rating[5]

        review_dic = {'room_reviews_name':room_reviews_name, 'room_reviews_date':room_reviews_date ,'room_reviews_cont':room_reviews_cont, 
                    'room_cleanliness':room_cleanliness, 'room_accuracy':room_accuracy, 'room_communication':room_communication, 'room_position':room_position,
                    'room_checkin':room_checkin, 'room_cost_effectiveness':room_cost_effectiveness}
        insert_room_data_in_airdnd_home_review(room_idx, review_dic)
        data_list.append(review_dic)
    print("reviews : ", data_list)  
    return data_list

def extract_loc_info_distance(room_idx, distance):
    data_list = []
    for e_list in distance:
        nearby_attraction, attraction_distance = e_list.find_all("div")
        attractions = [nearby_attraction.string, attraction_distance.string]
        data_list.append(attractions)
        insert_room_data_in_airdnd_home_attractions_distance(room_idx, attractions)
    print("data_list : ", data_list)  
    return data_list

def extract_use_rule(room_idx, room_use_rules):
    data_list = []
    for e_list in room_use_rules:
        use_rule = e_list.find("span", recursive=False).get_text()
        data_list.append(use_rule)
        insert_room_data_in_airdnd_home_use_rule(room_idx, use_rule)
    print("data_list : ", data_list)
    return data_list

def extract_safety_rule(room_idx, room_safety):
    data_list = []
    for e_list in room_safety:
        safety = e_list.find("span", recursive=False).get_text()               
        data_list.append(safety)
        insert_room_data_in_airdnd_home_safety_rule(room_idx, safety)

    print("data_list : ", data_list)  
    return data_list

def extract_rating(room_idx, room_rating_num):
    data_list = []
    for e_list in room_rating_num:
        rating = float(e_list.string)
        data_list.append(rating)
    if len(data_list) == 0:
        data_list = [0, 0, 0, 0, 0, 0]
    print("data_list : ", data_list)
    return data_list

def scrape_page(URL, room_idx, price, place):
    while True:
        driver = webdriver.Chrome('C:/Wooseong/web scraper/chromedriver')
        driver.set_window_size(1400,1000)
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
                try:
                    room_review_num2 = str(room_review_num).replace("(", "").replace(")", "")
                    room_review_num = int(room_review_num2)
                except:
                    room_review_num2 = str(room_review_num).replace("후기 ", "").replace("개", "")
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
            room_max_person_n = room_filter[0]
            room_filter_max_person = int(room_max_person_n[room_max_person_n.find('최대 인원 ')+6:room_max_person_n.find('명')])
            room_bedroom_n = room_filter[1]
            try:
                room_filter_bedroom = int(room_bedroom_n[room_bedroom_n.find('침실 ')+3:room_bedroom_n.find('개')])
            except:
                room_filter_bedroom = 0; #원룸
            try:
                room_bed_n = room_filter[2]
                room_filter_bed = int(room_bed_n[room_bed_n.find('침대 ')+3:room_bed_n.find('개')])
                room_bathroom = room_filter[3]
            except:
                room_filter_bed = 1
                room_bathroom = "욕실 1개"
            
            try:
                room_filter_bathroom = float(room_bathroom[room_bathroom.find('욕실 ')+3:room_bathroom.find('개')])
            except:
                room_filter_bathroom = 1

            room_pictures = main_container.find_all("div", {"class", "_1h6n1zu"})
            room_notice_title = main_container.select('div._1044tk8 > div._1mqc21n > div._1qsawv5')
            room_notice_cont = main_container.select('div._1044tk8 > div._1mqc21n > div._1jlr81g')
            room_notice_icon = main_container.select('div._1044tk8 > div._fz3zdn > svg')
            try:
                room_host = main_container.select_one('div._1y6fhhr').find("span")
            except:
                room_host = ""

            room_loc_info = main_container.select_one('div._1cvivhm > div._1byskwn > div._vd6w38n')
            #만약 지역 설명이 없이 주변 명소 거리만 나온다면
            if room_loc_info is not None:
                room_loc_info_cont = "location content is None"
                room_loc_info_dist = room_loc_info.select('div._dc0jge')
            else:
                try:
                    room_loc_info_cont = main_container.find_all("div",{"class","_162hp8xh"})[-2].select_one('div._1y6fhhr > span')
                except:
                    room_loc_info_cont = "location content is None"
                room_loc_info_dist = main_container.find_all("div",{"class","_dc0jge"})
            
            room_bed_sort = main_container.select('div._9342og > div._1auxwog')
            room_bed_sort_cont = main_container.select('div._9342og > div._1a5glfg')
            room_bed_sort_icon = main_container.select('div._9342og > div._p03egf')
            #room_convenient_facilities = main_container.select('div._19xnuo97 > div._1nlbjeu')
            room_convenient_facilities = main_container.find_all("div",{"class","_19xnuo97"})
            print("리스트 길이는 : ", len(room_convenient_facilities))
            room_reviews = main_container.select('div._50mnu4')
            room_rules_prev = main_container.select('div._m9x7bnz > div._f42bxt')
            try:
                room_use_rules = room_rules_prev[0].select('div._ud8a1c > div._u827kd')
                room_safety = room_rules_prev[1].select('div._ud8a1c > div._u827kd')
            except:
                room_use_rules = []
                room_safety = []

            # 세부 별점
            room_rating_num = main_container.select('div._a3qxec > div._bgq2leu > span._4oybiu')

            # 여기 호스트 내용
            host_dic = {}
            room_host_name = main_container.select_one('div._f47qa6 > div._svr7sj > h2').get_text()
            room_host_name = room_host_name.replace("호스트: ", "")
            room_host_sign_in_date = main_container.select_one('div._f47qa6 > div._svr7sj > div._1fg5h8r').get_text()
            room_host_sign_in_date = room_host_sign_in_date.replace("회원 가입일: ", "")
            room_host_char = main_container.select('div._1byskwn')[-2].select('div._siy8gh > ul._e13lb4n > li._1tvtahm > div._5kaapu > span._pog3hg')
            room_host_certification = False
            room_host_superhost = False
            room_host_review_num = 0
            for ischeck in room_host_char:
                if ischeck.string == "본인 인증 완료":
                    room_host_certification = True
                if ischeck.string == "슈퍼호스트":
                    room_host_superhost = True
                if "후기" in ischeck.string:
                    host_review_num = ischeck.string
                    room_host_review_num = int(host_review_num[host_review_num.find(' ')+1:host_review_num.find('개')])
            
            room_host_respone = main_container.select('ul._jofnfy > li._1q2lt74')
            host_language = ""
            host_response_rate = ""
            host_response_time = ""
            for host_res_list in room_host_respone:                  
                if "언어:" in host_res_list.string:
                    host_language = host_res_list.string
                    host_language = host_language[host_language.find(':')+2:]
                if "응답률:" in host_res_list.string:
                    host_response_rate = host_res_list.string
                    host_response_rate = host_response_rate[host_response_rate.find(':')+2:]
                if "응답 시간:" in host_res_list.string:
                    host_response_time = host_res_list.string
                    host_response_time = host_response_time[host_response_time.find(':')+2:]
            try:
                room_host_stats = main_container.select_one('div._152qbzi > span > div._1y6fhhr > span').get_text() #div._upzyfk1 > 
            except:
                room_host_stats = "None"
            
            try:
                room_host_interaction = main_container.select_one('div._uz1jgk > div._3lsmeq > span').get_text()
            except:
                room_host_interaction = "None"
            host_dic = {'room_host_name':room_host_name, 'room_host_sign_in_date':room_host_sign_in_date, 'room_host_certification':room_host_certification, 
                        'room_host_superhost':room_host_superhost, 'room_host_review_num':room_host_review_num, 'host_language':host_language, 'host_response_rate':host_response_rate,
                        'host_response_time':host_response_time, 'room_host_stats':room_host_stats, 'room_host_interaction':room_host_interaction }
            test = soup.find_all("li",{"class","_wmuyow"})
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
            print("room_host : " , room_host)
            print("room_loc_info_cont : ", room_loc_info_cont)
            picture = extract_pictures(room_idx, room_pictures)
            room_notice = extract_home_notice(room_idx, room_notice_title, room_notice_cont, room_notice_icon)
            room_bed = extract_home_bed(room_idx, room_bed_sort, room_bed_sort_cont, room_bed_sort_icon)
            room_convenient_facility = extract_convenient_facility(room_idx, room_convenient_facilities)
            room_rating = extract_rating(room_idx, room_rating_num)
            room_review = extract_review(room_idx, room_reviews, room_rating)
            room_loc_info_distance = extract_loc_info_distance(room_idx, room_loc_info_dist)
            room_use_rule = extract_use_rule(room_idx, room_use_rules)
            room_safety_rule = extract_safety_rule(room_idx, room_safety)
            insert_room_data_in_airdnd_host(room_idx, host_dic)
            print()

            data = {'URL':URL,'main_title':main_title, 'isSuperHost':isSuperHost, 'addr':addr, 'latlng':latlng, 'room_idx':room_idx, 'price':int_price,
                    'room_score':room_score, 'room_review_num':room_review_num, 'sub_title':sub_title, 'room_filter_max_person':room_filter_max_person,
                    'room_filter_bedroom':room_filter_bedroom, 'room_filter_bed':room_filter_bed, 'room_filter_bathroom':room_filter_bathroom, 'room_host':room_host, 
                    'room_loc_info_cont':room_loc_info_cont, 'picture':picture, 'room_convenient_facility':room_convenient_facility, 'room_use_rule':room_use_rule,
                    'room_safety_rule':room_safety_rule , 'room_loc_info_distance':room_loc_info_distance, 'place':place,
                    'room_notice':room_notice, 'room_bed':room_bed, 'room_reviews':room_review}

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