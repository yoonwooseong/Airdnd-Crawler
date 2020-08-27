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
    print("DB저장 성공 - airdnd_home")

def insert_room_data_in_airdnd_home_picture(room_idx, room_picture):
    sql_insert =  'insert into airdnd_home_picture (idx, home_idx, url) VALUES (0, %s, %s)'
    val = (room_idx, room_picture.encode('utf8').decode('utf8'))
    db.execute(sql_insert, val)
    conn.commit()
    print("DB저장 성공 - airdnd_picture")

def insert_room_data_in_airdnd_home_notice(room_idx, room_picture):
    sql_insert =  'insert into airdnd_home_picture (idx, home_idx, url) VALUES (0, %s, %s)'
    val = (room_idx, room_picture.encode('utf8').decode('utf8'))
    db.execute(sql_insert, val)
    conn.commit()
    print("DB저장 성공 - airdnd_picture")

def insert_room_data_in_airdnd_home_convenient_facility(data):
    sql_insert =  'insert into airdnd_home_convenient_facility (idx, home_idx, facility) VALUES (0, %s, %s)'
    val = (data['room_idx'], data['room_convenient_facility'].encode('utf8').decode('utf8'))
    db.execute(sql_insert, val)
    conn.commit()
    print("DB저장 성공 - airdnd_convenient_facility")

def insert_room_data_in_airdnd_home_review(data):
    sql_insert =  'insert into airdnd_home_review (idx, home_idx, user_name, review_date, review_content) VALUES (0, %s, %s, %s, %s)'
    val = (data['room_idx'], data['room_reviews']['room_reviews_name'].encode('utf8').decode('utf8'), 
            data['room_reviews']['room_reviews_date'].encode('utf8').decode('utf8'),  data['room_reviews']['room_reviews_cont'].encode('utf8').decode('utf8'),)
    db.execute(sql_insert, val)
    conn.commit()
    print("DB저장 성공 - airdnd_review")

def insert_room_data_in_airdnd_home_attractions_distance(data):
    sql_insert =  'insert into airdnd_home_attractions_distance (idx, home_idx, attractions_name, attractions_distance) VALUES (0, %s, %s, %s)'
    val = (data['room_idx'], data['room_loc_info_distance'][0].encode('utf8').decode('utf8'), data['room_loc_info_distance'][1].encode('utf8').decode('utf8'))
    db.execute(sql_insert, val)
    conn.commit()
    print("DB저장 성공 - airdnd_attractions_distance")

def insert_room_data_in_airdnd_home_use_rule(data):
    sql_insert =  'insert into airdnd_home_use_rule (idx, home_idx, use_rule) VALUES (0, %s, %s)'
    val = (data['room_idx'], data['room_use_rule'][0].encode('utf8').decode('utf8'))
    db.execute(sql_insert, val)
    conn.commit()
    print("DB저장 성공 - airdnd_use_rule")

def insert_room_data_in_airdnd_home_safety_rule(data):
    sql_insert =  'insert into airdnd_home_safety_rule (idx, home_idx, safety_rule) VALUES (0, %s, %s)'
    val = (data['room_idx'], data['room_safety_rule'][0].encode('utf8').decode('utf8'))
    db.execute(sql_insert, val)
    conn.commit()
    print("DB저장 성공 - airdnd_safety_rule")

def insert_room_data_in_airdnd_home_bed(data):
    sql_insert =  'insert into airdnd_home_bed (idx, home_idx, bed_room_name, bed_room_option) VALUES (0, %s, %s, %s)'
    val = (data['room_idx'], data['room_bed'][0][0].encode('utf8').decode('utf8'), data['room_bed'][0][1].encode('utf8').decode('utf8'))
    db.execute(sql_insert, val)
    conn.commit()
    print("DB저장 성공 - airdnd_bed")

db.close()
conn.close()