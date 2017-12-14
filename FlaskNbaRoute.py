# coding=utf-8
# import class
import Leveldbutil, Reporter, Utils
from datetime import datetime
from flask import Flask, render_template, send_from_directory
from flask_bootstrap import Bootstrap
from werkzeug.datastructures import Headers
from werkzeug.wrappers import Response

# Hint doc: datetime Module使用說明參考官方文件
# datetime in python : https://docs.python.org/3/library/datetime.html#datetime-objects
# datetime strftime() and strptime() : https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior

app = Flask(__name__)  # define app using flask

# Flask-Bootstrap test...
@app.route('/base')
def base():
    return render_template("base.html")


# 首頁
@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def nba_reporter():
    return render_template("index.html")


# 列出NBA即時資訊(爬蟲結果)
@app.route('/list', methods=['POST'])
def list_data():
    # 建立資料庫
    db = Leveldbutil.init("nbaDB")

    # 即時賽事資料來源
    url = "http://sports.ltn.com.tw/nba"

    # 取得即時賽事資料
    report = Reporter.reporter(Reporter.get_nba_report(url))

    # print(sys.path)

    if report:
        print('Report not null')
        #  以下單純以當前時間作為key(記錄到秒) 收集每一次取到的即時賽事結果
        time_form = "%Y-%m-%d %H:%M:%S"
        today = datetime.today().strftime(time_form)

        # 寫入DB(key:時分秒 value:即時賽事資料)
        Leveldbutil.insert(db, today, report)

        # 從DB取得此次即時賽事資訊並匯出音檔
        try:
            # create FileUtils object
            file_util = Utils.FileUtils()
            # call object method(從DB取得方才寫入的即時賽事結果，並傳入generate_sound產生MP3檔案)
            file_util.generate_sound(Leveldbutil.search(db, today))
        except:
            print("No data found : {}".format(datetime.today().strftime("%Y-%m-%d %H:%M:%S")))

        # 查看DB所有資料
        # Leveldbutil.dump(db)

    return render_template("index.html", reportData=report)


# 下載MP3檔案(一)
@app.route("/download", methods=['POST'])
def download():
    headers = Headers()
    headers.set('Content-Disposition', 'attachment', filename='NBAReporter.mp3')

    return Response(generate(), mimetype='audio/mp3', headers=headers)


# 讀取MP3檔案(read bytes)
# yield用法說明:
# 1. 使用yield會將目前的函式看作是iterator(迭代器)
# 2. yield就像是return返回一個值(yield 右邊的值)，並且記住這個返回的位置，下次iterator就從這個位置後(下一行)開始
def generate():
    with open("Sound/NBAReporter.mp3", "rb") as music:
        data = music.read(1024)
        while data:
            yield data
            data = music.read(1024)


# 下載MP3檔案(二)
@app.route('/downloadfile/<path:filename>', methods=['GET', 'POST'])
def downloadfile(filename):
    uploads = "Sound/"
    return send_from_directory(directory=uploads, filename=filename)


# 線上播放MP3
@app.route('/player/<path:filename>', methods=['GET', 'POST'])
def player(filename):
    uploads = "Sound/"
    return send_from_directory(directory=uploads, filename=filename)


def start():
    Bootstrap(app)   # using flask bootstrap
    app.run(debug=True, port=8080)  # run
