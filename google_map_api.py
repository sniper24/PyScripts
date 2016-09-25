# -*- coding: utf-8 -*-
import requests
import json


#googlemap direction api第一次使用

#params1 = {'origin': '香港沙田屈臣氏中心', 'destination': '香港理工大学','sensor':'false'}  #输入参数(从excel里读入)
params1 = dict(
    origin='香港城市大学',
    destination='沙田',
    waypoints='',
    optimize='true',
    sensor='false'
)

#{u'routes': [], u'status': u'ZERO_RESULTS'}



#http://maps.googleapis.com/maps/api/directions/json?origin='清华大学',destination='上海',waypoints='optimize:true|武汉|四川|厦门|大连',sensor='false'
r = requests.get('http://maps.googleapis.com/maps/api/directions/json', params=params1).json()

r1=r['routes'][0]['legs'][0]['distance']['text']#距离长度1,214 km

r2=r['routes'][0]['legs'][0]['distance']['value']#距离值1213511

r3=r['routes'][0]['legs'][0]['duration']['text']#时间长度13 hours 18 mins

r4=r['routes'][0]['legs'][0]['duration']['value']#时间值47881

r5=r['routes'][0]['legs'][0]['start_address']#起点 地址Beijing, Beijing, China

r6=r['routes'][0]['legs'][0]['start_location']['lat']#纬度39.9042062

r7=r['routes'][0]['legs'][0]['start_location']['lng']#精度116.4070326

r8=r['routes'][0]['legs'][0]['end_address']#终点 地址Shanghai, Shanghai, China

r9=r['routes'][0]['legs'][0]['end_location']['lat']#纬度31.2308393

r10=r['routes'][0]['legs'][0]['end_location']['lng']#精度121.4733199

r11=r['routes'][0]['waypoint_order']
#修改waypoint optimize 示例代码：http://maps.googleapis.com/maps/api/directions/json?origin=Adelaide,SA&destination=Adelaide,SA&waypoints=optimize:true|Barossa+Valley,SA|Clare,SA|Connawarra,SA|McLaren+Vale,SA&sensor=false

print r1,r2,r3,r4,r5,r6,r7,r8,r9,r10



