# Author : ZhangTong
import pymysql

HOST = 'localhost'
USER = 'root'
PASSWORD = 'root'
PORT = 3306
DB = 'spider'

db = pymysql.connect(host=HOST, user=USER, password=PASSWORD, port=PORT, db=DB, charset='utf8')
cursor = db.cursor()
