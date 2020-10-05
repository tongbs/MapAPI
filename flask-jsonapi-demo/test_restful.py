from flask import Flask, jsonify

import json
import urllib.parse

import requests

from datetime import datetime
from sensor_const import airbox_sensor_list
from sensor_const import airbox_sensor_mac

from cord import Cord as Cord

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return {'Enter':'please enter correct request!'}

@app.route('/api/zcom/fish', methods=['GET'])
def fish():
    url_login = 'http://iothub.nctu.me:11000/login?next=/datas/BigBlackFish'
    payload = {'username':'demo','password':'demo'}
    with requests.session() as s:
        r = s.post(url_login, data = payload)
        url = 'http://iothub.nctu.me:11000/datas/BigBlackFish?limit=1'
        data = s.get(url)
        return data.json()

@app.route('/api/zcom/farm/<string:farm_name>', methods=['GET'])
def farm(farm_name):
    url_login = 'https://sql.iottalk.tw/login?next=/#bao3'
    payload = {'username':'xs1523c','password':'zxcv85246'}
    with requests.session() as s:
        r = s.post(url_login, data = payload)
        url = 'https://sql.iottalk.tw/datas/%s?limit=1'%farm_name
        data = s.get(url)
        return data.json()

@app.route('/api/zcom/bus/history/<string:bus_name>/<string:time>', methods=['GET'])
def bus(bus_name,time):
    if bus_name == 'medium_bus':
        word = '機動中巴'
    elif bus_name == 'HSR_bus':
        word = '高鐵大巴'
    elif bus_name == 'NCTU_bus':
        word = '光復博愛大巴'
    word = urllib.parse.quote(word)
    
    if time == 'hour':
        url = 'https://map.iottalk.tw/secure/history?app_num=92&name=NCTUBus_%s&time=2'%word
    elif time == 'min':
        url = 'https://map.iottalk.tw/secure/history?app_num=92&name=NCTUBus_%s&time=1'%word
    data = requests.get(url)
    return data.json()

class Error(Exception):
    pass

def airbox_pull_data(url):
    data = requests.get(url,verify=False)
    if data.status_code != 200:
        raise Error(data.text)
    return data.json()['devices']

@app.route('/api/zcom/air/<string:air_sensor>', methods=['GET'])
def air(air_sensor):
    url = 'https://nctuairbox.edimaxcloud.com:55443/devices?token=c58affa8-b74e-4341-a020-82b4ba776a69'
    data = airbox_pull_data(url)
    response = []
    if data != None and data != []:
        for devices in data:
            if devices['id'] in airbox_sensor_mac:
                for sensor in airbox_sensor_list:
                    if air_sensor == 'pm2.5'and sensor['FEATURE_NAME'] == 'PM2.5':
                        response.append({'sensor':sensor['FEATURE_NAME'], 'lat':devices['lat'], 'lon':devices['lon'], 'loc':str(airbox_sensor_mac[devices['id']]['name']), 'value':devices[sensor['NAME_ON_AIRBOX']], 'time':devices['time'] })
                    elif air_sensor == 'pm10' and sensor['FEATURE_NAME'] == 'PM10':
                        response.append({'sensor':sensor['FEATURE_NAME'], 'lat':devices['lat'], 'lon':devices['lon'], 'loc':str(airbox_sensor_mac[devices['id']]['name']), 'value':devices[sensor['NAME_ON_AIRBOX']], 'time':devices['time'] })
    else:
        print("Airbox data may have some erros!!")
    return json.dumps(response, ensure_ascii=False, indent = 4,separators=(',',':'))


#-----------------------------------------------------------------------------------------------------
@app.route('/api/iot/covid/<string:type>', methods=['GET'])
def covid(type):
    web = requests.get('https://pomber.github.io/covid19/timeseries.json');
    site_json = json.loads(web.text)
    result = [];
    for key in Cord:
        if type == 'confirmed': 
            #print(site_json[key][-1]['confirmed'],Cord[key]['name'],Cord[key]['lat'],Cord[key]['lng'],str(site_json[key][-1]['date']),datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            result.append([Cord[key]['name'],Cord[key]['lat'],Cord[key]['lng'],site_json[key][-1]['confirmed'],datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        elif type == 'deaths':
            #print(site_json[key][-1]['deaths'],Cord[key]['name'],Cord[key]['lat'],Cord[key]['lng'],str(site_json[key][-1]['date']),datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            result.append([Cord[key]['name'],Cord[key]['lat'],Cord[key]['lng'],site_json[key][-1]['deaths'],datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        elif type == 'recovered':
            #print(site_json[key][-1]['recovered'],Cord[key]['name'],Cord[key]['lat'],Cord[key]['lng'],str(site_json[key][-1]['date']),datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            result.append([Cord[key]['name'],Cord[key]['lat'],Cord[key]['lng'],site_json[key][-1]['recovered'],datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
    return json.dumps(result, ensure_ascii=False, indent = 4,separators=(',',':'))


@app.route('/api/iot/speed/5s', methods=['GET'])
def speeds():
    url_login = 'http://140.113.215.2:25000/login?next=/datas/highway5S'
    payload = {'username':'admin','password':'admin666'}
    with requests.session() as s:
        r = s.post(url_login, data = payload)
        url = 'http://140.113.215.2:25000/datas/highway5S?limit=1'
        data = s.get(url)
        return data.json()

@app.route('/api/iot/speed/5n', methods=['GET'])
def speedn():
    url_login = 'http://140.113.215.2:25000/login?next=/datas/highway5N'
    payload = {'username':'admin','password':'admin666'}
    with requests.session() as s:
        r = s.post(url_login, data = payload)
        url = 'http://140.113.215.2:25000/datas/highway5N?limit=1'
        data = s.get(url)
        return data.json()

#--------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 7790,debug=True)

#if __name__ == '__main__':
#    app.run(debug=True)
'''
@app.route('api/zcom/fish', methods=['GET'])
def fish():
    url = 'http://fish.iottalk.tw:11000/datas/Lab117_Aquarium?limit=1'
    #data = urllib.request.urlopen(url).read().decode('utf-8')
    data = requests.get(url)
    return data.json()
    #data_dict= json.loads(data)
    #return jsonify(data_dict)
'''
