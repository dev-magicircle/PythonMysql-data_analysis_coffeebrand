import pymysql
import pandas
import csv

#sql 연결, 생성
conn = pymysql.connect(host='127.0.0.1', port=3307, user='root', password='010701',db='db', charset='utf8')
cur=conn.cursor()
sql="create table store("\
    "num int(20),"\
    "name varchar(30),"\
    "lname varchar(30),"\
    "primary key(num))"
cur.execute(sql)
conn.commit()
conn.close()



#테이블에 csv파일 분리해서 넣기
with open("seoul_store.csv",'r',encoding="utf8")as f:
    for line in f:
        store=f.read()
f.close()
store=store.split('\n')
store=pandas.DataFrame(store)
store=pandas.DataFrame(store[0].str.split(',').tolist())

#데이터 추가하는 문장
sql = "INSERT IGNORE INTO store (num,name,lname) VALUES (%s,%s,%s)"
for i in range(0,len(store)+1):
    conn = pymysql.connect(host='127.0.0.1', port=3307, user='root', password='010701',db='db', charset='utf8')
    cur = conn.cursor()
    cur.execute(sql,(store[0][i],store[1][i],store[2][i]))
    conn.commit()
    conn.close()
