from flask import Flask, jsonify

import json
import urllib.parse

import requests

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
        
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 7790,debug=True)

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
