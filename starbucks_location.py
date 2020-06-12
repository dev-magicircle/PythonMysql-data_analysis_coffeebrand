#라이브러리 불러오기

import folium
import pymysql
import pandas
m = folium.Map(
  location=[37.5257672,127.0140216],
  zoom_start=11
)
m.save('map.html')

#SQL연결, 테이블생성

conn = pymysql.connect(host='127.0.0.1', port=3307, user='root', password='010701',db='db', charset='utf8')
cur=conn.cursor()

#sql table create
sql="create table location("\
    "id int(20) PRIMARY KEY,"\
    "num int(20),"\
    "latitude double,"\
    "longitude double,"\
    "FOREIGN KEY(num)REFERENCES store(num))"

cur.execute(sql)
conn.commit()
conn.close()

#CSV파일 연결해서 데이터정리

with open("seoul_store.csv",'r',encoding="utf8")as f:
    for line in f:
        store=f.read()
f.close()
store=store.split('\n')
store=pandas.DataFrame(store)
store=pandas.DataFrame(store[0].str.split(',').tolist())
sql = "INSERT IGNORE INTO location (id,num,latitude,longitude) VALUES (%s,%s,%s,%s)"
for i in range(0,len(store)+1):
    conn = pymysql.connect(host='127.0.0.1', port=3307, user='root', password='010701',db='db', charset='utf8')
    cur = conn.cursor()
    cur.execute(sql,(i+1,store[0][i],store[36][i],store[37][i]))
    conn.commit()
    conn.close()

#스타벅스 위도, 경도, 지점명 불러오기

conn = pymysql.connect(host='127.0.0.1', port=3307, user='root', password='010701',db='store_db', charset='utf8')
cur=conn.cursor()
sql="select s.lname,l.latitude,l.longitude from store as s,location as l where s.name like '%스타벅스%' and s.num=l.num"
cur.execute(sql)
starbucks=pandas.DataFrame(cur.fetchall())
starlocation=[]
for i in range(len(starbucks)):
    starlocation.append({'store':starbucks[0][i],"loc":[starbucks[2][i],starbucks[1][i]]})

#지도에 스타벅스 위치 표시

from folium.plugins import MarkerCluster
marker_cluster = MarkerCluster().add_to(m)

for i in range(len(starlocation)):
  folium.Marker(
    location=starlocation[i]['loc'],
    popup=starlocation[i]['store'],
    icon=folium.Icon(color='green',icon='star'),
  ).add_to(marker_cluster)

m.save('starbucks_map.html')
