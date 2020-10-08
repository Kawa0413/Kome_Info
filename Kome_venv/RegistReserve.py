from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import requests
#import locale
import json
import os
from os.path import join, dirname
from dotenv import load_dotenv


#load_envでファイルの中身を読み込む

# load_dotenv(verbose=True)

# dotenv_path = join(dirname(__file__), '.env')
# load_dotenv(dotenv_path)
# #MONGODB_URLを読み込む
# PWD = os.environ.get("MONGODB_URL")

#CORSで同一制限元ポリシーの制限緩める
#bson.objectidでデータ更新

#LINE Botで通知させるためのクラスを用意
class Line_bot:
    def __init__(self):
        #発行したトークンをセットする
        self._api = "https://notify-api.line.me/api/notify"
        self._token = "SoNMrPc66LKFJdr4YUTmrAGGyBMLLT4x9iPnPIOtMK8"
        self._headers = {"Authorization" : "Bearer "+ self._token}

    def bot1(self,line):
        #引数lineの中に後々使う二つのkeyに対応した文章を作る
        message = line['name'] + 'が' + line['line_airdate'] + 'に放送！もし外出予定なら予約しとき~知らんけど'
        payload = {"token" : self._token, "message" :  message}
        #repuestsはflaskのrequestとは違うからまた別でimport
        post = requests.post(self._api, headers = self._headers, params=payload)

    def bot2(self,line):
        #引数lineの中に後々使う二つのkeyに対応した文章を作る
        message = line['name'] + 'が' + line['line_airdate'] + 'に放送に予約変更！もし外出予定なら予約しとき~知らんけど'
        payload = {"token" : self._token, "message" :  message}
        #repuestsはflaskのrequestとは違うからまた別でimport
        post = requests.post(self._api, headers = self._headers, params=payload)

            
#Flaskクラスのインスタンス作ってapp(変数)に代入
app = Flask(__name__, static_folder='Frontend')
client = MongoClient("mongodb+srv://Kome:Hikaru0721@komeinfo.mmmm6.mongodb.net/admin?authSource=admin&replicaSet=atlas-214nbh-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true")
#mongodb+srv://Kome:*****@komeinfo.mmmm6.mongodb.net/admin?authSource=admin&replicaSet=atlas-214nbh-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true
#client = MongoClient("MONGODB_URL")mongodb://127.0.0.1:27017/Kome_Info
db = client.Kome_Info
CORS(app)

#日本語以外のwindowsにて日本語をエンコードするため
#locale.setlocale(locale.LC_CTYPE, "Japanese_Japan.932")

@app.route("/")
def init():
    return render_template('Top.html')

#Registration関連の動作
@app.route('/forcollection1', methods=['GET'])
def get_all_Drama():
    Data = db.registration
    output = []
    for s in Data.find():
        _id = str(s['_id'])
        output.append({'_id': _id, 'name': s['name'], 'memo': s['memo']})
    return jsonify({'result': output})


@app.route('/forcollection1', methods=['POST'])
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


@app.route('/forcollection1', methods=['PUT'])
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

#Reservation関連の動作
@app.route('/forcollection2', methods=['GET'])
def get_all_Drama2():
    Data = db.reservation
    output = []
    for s in Data.find():
        _id = str(s['_id'])
        airdate = (s['day'].strftime('%Y年%m月%d日 %H時%M分'))
        output.append({'_id': _id, 'name': s['name'], 'day': airdate})
    return jsonify({'result': output})

#strptimeで文字列を日付と変換してDB登録、strftimeで日付を文字列として表示
@app.route('/forcollection2', methods=['POST'])
def add_Drama2():
    Data = db.reservation
    output = []
    #json形式で書かれているのでflaskリクエストで受信したデータを取得するためのrequest.get_json
    data = request.get_json(force=True)
    name = data.get('name', None)
    #datetime.strptimeでデータベースの登録情報を整理
    day_default = data.get('day', None)
    day = datetime.strptime(day_default, '%Y-%m-%dT%H:%M')
    Data.insert_one({'name': name, 'day': day})
    #lineに通知いった時にも日本語化されるようにするためのline_airdate
    line_airdate = datetime.strftime(day, '%Y年%m月%d日 %H時%M分')
    #insertだけでなくinsert_one
    # Insert後再検索をかける
    for s in Data.find():
        _id = str(s['_id'])
        airdate = (s['day'].strftime('%Y年%m月%d日 %H時%M分'))
        output.append({'_id': _id, 'name': s['name'], 'day': airdate})

    #辞書型で対応させてやりたいから空の辞書型を定義
    component = {}
    component["name"] = name
    component["line_airdate"] = line_airdate
    #最後に引数componentをとるLine_botを呼び出してやる
    bot = Line_bot()
    bot.bot1(component)
    return jsonify({'result': output})


@app.route('/forcollection2', methods=['PUT'])
def update_Drama2():
    Data = db.reservation
    output = []
    data = request.get_json(force=True)
    _id = data.get('id', None)
    name = data.get('name', None)
    day_default = data.get('day', None)
    day = datetime.strptime(day_default, '%Y-%m-%dT%H:%M')
    Data.update_one({'_id':ObjectId(_id)},{'$set':{'name': name,'day': day}}, upsert = False)
    #lineに通知いった時にも日本語化されるようにするためのline_airdate
    line_airdate = datetime.strftime(day, '%Y年%m月%d日 %H時%M分')
    # Update後再検索をかける
    for s in Data.find():
        _id = str(s['_id'])
        airdate = (s['day'].strftime('%Y年%m月%d日 %H時%M分'))
        output.append({'_id': _id, 'name': s['name'], 'day': airdate})
    
    #辞書型で対応させてやりたいから空の辞書型を定義
    component = {}
    component["name"] = name
    component["line_airdate"] = line_airdate
    #最後に引数componentをとるLine_botを呼び出してやる
    bot = Line_bot()
    bot.bot2(component)
    return jsonify({'result': output})

#pythonファイルが正常に～.pyとして実行されているかどうか(インポートとかしただけで実行されないように)
#__name__はpython ～.pyとして実行したときのみ__main__になる
#デバッグ出力機能有効にするのも忘れずに
if __name__ == '__main__':
    #app.run(debug = True)
    #with Line_bot():
    app.debug = True
    port = int(os.environ.get("PORT", 5050))
    app.run(host='0.0.0.0', port=port)
