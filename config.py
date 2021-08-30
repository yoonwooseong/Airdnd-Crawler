import pymysql

# DB 설정
conn = pymysql.connect(host = '52.78.111.36', user = 'root', password = '1111', db = 'AirdndDB', charset = 'utf8mb4', use_unicode=True)