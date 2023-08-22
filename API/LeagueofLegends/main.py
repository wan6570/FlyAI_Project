import api
import pymysql
import pandas as pd
import matchequip

# MySQL 연결 정보 설정
hostname='minseok.mysql.database.azure.com'
username='doyoon'
password='1234!@#$'
database='project'
connection = pymysql.connect(user=username, password=password, host=hostname, port=3306, database=database, ssl_ca="C:\\Users\\066\\Desktop\\DigiCertGlobalRootCA.crt.pem", ssl_disabled=False)
cursor = connection.cursor()


##함수 설명
df= api.getAPI('장연석') #데이터 프레임 만들어주는 함수 input : username / output : 전적데이터프레임

equipment= matchequip.equip('Canna',connection) #장비 찾아주는 함수 input : proname / output : 장비 데이터프레임

connection.close()

