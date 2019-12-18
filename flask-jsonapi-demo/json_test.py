from flask import Flask, jsonify
from flask import request as request_fl
from flask_restful import Resource, Api

import json
from urllib import request as request_url
import urllib.parse

word = '機動中巴'
word = urllib.parse.quote(word)
url = 'https://map.iottalk.tw/secure/history?app_num=92&name=NCTUBus_%s&time=2'%word
data = request_url.urlopen(url).read().decode('utf-8')
#print(data)
data_dict= json.loads(data)
#print(data_dict)
print(json.dumps(data_dict))

#print(type(data))
#print(type(json.loads(data)))
