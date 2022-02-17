import json
from urllib import response
import requests
import urllib.parse
import pandas as pd

pref=str(input('都道府県名を入力してください'))
station=str(input('駅名を入力してください'))
# urllib=日本語や特殊文字などの非ASCII文字をクエリ文字列に組み込んでGETリクエストを送信する場合など、これらの文字をURL構成要素として使用できるよう適切にエンコードする必要があります。 これを一般的にURLエンコードと呼んでいます。
def RailAPI(station,pref):
    station_url=urllib.parse.quote(station)
    pref_url=urllib.parse.quote(pref)
    api='http://express.heartrails.com/api/json?method=getStations&name={station_name}&prefecture={pref_name}'
    url=api.format(station_name=station_url,pref_name=pref_url)
    response=requests.get(url)
    result_list=json.loads(response.text)['response']['station']
    lng=result_list[0]['x']
    lat=result_list[0]['y']
    # print(result_list)
    return lat,lng

lat_st,lng_st=RailAPI(station,pref)
def HotpepperAPI(lat,lng):
    api_key="38995572dd3d1c7d"
    api="http://webservice.recruit.co.jp/hotpepper/gourmet/v1/?" \
            "key={key}&lat={lat}&lng={lng}&free_drink=1&private_room=1&course=1range=2&count=100&order=1&format=json"
    url=api.format(key=api_key,lat=lat_st,lng=lng_st)
    response=requests.get(url)
    result_list=json.loads(response.text)['results']['shop']
    shop_datas=[]
    for shop_data in result_list:
        shop_datas.append([shop_data["name"],shop_data["address"],shop_data["urls"]['pc'], shop_data["budget"]['average'], 'Hotpepper'])
    return shop_datas

columns=['name','address','url','budget','source']
HP_data=pd.DataFrame(HotpepperAPI(lat_st,lng_st),columns=columns)

total_data=pd.concat([HP_data])
print(total_data)