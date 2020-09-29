from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
import json
import os
#CORSで同一制限元ポリシーの制限緩める
#bson.objectidでデータ更新

#Flaskクラスのインスタンス作ってapp(変数)に代入
app = Flask(__name__)
client = MongoClient("localhost:27017")
db = client.Kome_Info
CORS(app)


@app.route('/', methods=['GET'])
def get_all_Drama():
    Data = db.registration
    output = []
    for s in Data.find():
        _id = str(s['_id'])
        output.append({'_id': _id, 'name': s['name'], 'memo': s['memo']})
    return jsonify({'result': output})


@app.route('/', methods=['POST'])
def add_Drama():
    Data = db.registration
    output = []
    #json形式で書かれているのでflaskリクエストで受信したデータを取得するためのrequest.get_json
    data = request.get_json(force=True)
    name = data.get('name', None)
    memo = data.get('memo', None)
    Data.insert_one({'name': name, 'memo': memo})
    #insertだけでなくinsert_one
    # Insert後再検索をかける
    for s in Data.find():
        _id = str(s['_id'])
        output.append({'_id': _id, 'name': s['name'], 'memo': s['memo']})
    return jsonify({'result': output})


@app.route('/', methods=['PUT'])
def update_Drama():
    Data = db.registration
    output = []
    data = request.get_json(force=True)
    _id = data.get('id', None)
    name = data.get('name', None)
    memo = data.get('memo', None)
    Data.update_one({'_id':ObjectId(_id)},{'$set':{'name': name,'memo': memo}}, upsert = False)
    # Update後再検索をかける
    for s in Data.find():
        _id = str(s['_id'])
        output.append({'_id': _id, 'name': s['name'], 'memo': s['memo']})
    return jsonify({'result': output})

#pythonファイルが正常に～.pyとして実行されているかどうか(インポートとかしただけで実行されないように)
#__name__はpython ～.pyとして実行したときのみ__main__になる
#デバッグ出力機能有効にするのも忘れずに
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
