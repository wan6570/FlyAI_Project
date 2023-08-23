import pymysql

username='minseok'
password='1234!@#$'
database='testdb'

# MySQL 데이터베이스 연결
connection = pymysql.connect(user=username, password=password, host=hostname, port=3306, database=database, ssl_ca="DigiCertGlobalRootCA.crt.pem", ssl_disabled=False)
# 커서 생성
cursor = connection.cursor()
