# coding=utf-8
# import class
# .pyc ==> 編譯好的byte暫存
# ident
from datetime import datetime

import Reporter
import Utils
import Leveldbutil
from flask import Flask, render_template, send_from_directory, request
from flask_bootstrap import Bootstrap
from werkzeug.datastructures import Headers
from werkzeug.wrappers import Response, Request

# Hint doc: datetime Module使用說明參考官方文件
# datetime in python : https://docs.python.org/3/library/datetime.html#datetime-objects
# datetime strftime() and strptime() : https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior

app = Flask(__name__)  # define app using flask


# 在執行第一個Request之前預先執行（for test)
@app.before_first_request
def activate_job():
    print("activate_job Do something")


# Flask-Bootstrap test...
@app.route('/base')
def base():
    return render_template("base.html")


# 首頁
@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def nba_reporter():
    return render_template("index.html", report_data={})


# 列出NBA即時資訊(爬蟲結果)
@app.route('/list', methods=['POST'])
def list_data():
    # 建立或取得資料庫
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

        report_dict = {"time":today, "report": report}

        # 查看DB所有資料
        # Leveldbutil.dump(db)

    return render_template("index.html", report_data=report_dict)


# 從DB取得此次即時賽事資訊並匯出音檔
def get_report_by_key(key):
    # 建立或取得資料庫
    db = Leveldbutil.init("nbaDB")
    print("key===> {}".format(key))

    try:
        # create FileUtils object
        file_util = Utils.FileUtils()
        # call object method(從DB取得方才寫入的即時賽事結果，並傳入generate_sound產生MP3檔案)
        file_util.generate_sound(Leveldbutil.search(db, key))
    except:
        print("No data found : {}".format(datetime.today().strftime("%Y-%m-%d %H:%M:%S")))


# 讀取MP3檔案(read bytes)
# yield用法說明:
# 1. 使用yield會將目前的函式看作是iterator(迭代器)
# 2. yield就像是return返回一個值(yield 右邊的值)，並且記住這個返回的位置，下次iterator就從這個位置後(下一行)開始
def generate():
    # open("path") 說明:
    # file open 會直接從專案根目錄底下尋找路徑，故無須指定回上一層目錄
    with open("{}".format(Utils.FileUtils.path), "rb") as music:
        data = music.read(1024)
        while data:
            yield data
            data = music.read(1024)

def generate2():
    # open("path") 說明:
    # file open 會直接從專案根目錄底下尋找路徑，故無須指定回上一層目錄
    with open("{}".format(Utils.FileUtils.path), "rb") as music:
        data = music.read()
    return data


# 下載MP3檔案(一) => 依據key取得Report內容，再產生MP3
@app.route("/download", methods=['POST'])
def download():
    # 從DB取得此次即時賽事資訊並匯出音檔
    get_report_by_key(request.form['time'])

    # 執行下載
    headers = Headers()
    headers.set('Content-Disposition', 'attachment', filename='NBAReporter.mp3')

    return Response(generate(), mimetype='audio/mp3', headers=headers)


# 下載MP3檔案(二) => 依據key取得Report內容，再產生MP3
@app.route('/upload/<path:filename>', methods=['GET', 'POST'])
def upload(filename):
    # 從DB取得此次即時賽事資訊並匯出音檔
    # print(request.form['time'])
    # get_report_by_key(request.form['time'])

    # path 說明:
    # 指定取得目錄中的檔案，由於有建立Python Package，所以需指定回上一層目錄
    file_path = "../{}/".format(Utils.FileUtils().folder)
    return send_from_directory(directory=file_path, filename=filename)


# 線上播放MP3 => 依據key取得Report內容，再播放MP3
@app.route('/player/<path:filename>', methods=['GET', 'POST'])
def player(filename):
    # 從DB取得此次即時賽事資訊並匯出音檔
    # print(request.form.get('time'))
    # get_report_by_key(request.form['time'])

    # path 說明:
    # 指定取得目錄中的檔案，由於有建立Python Package，所以需指定回上一層目錄
    path = "../{}/".format(Utils.FileUtils().folder)
    return send_from_directory(directory=path, filename=filename)


if __name__ == "__main__":
    Bootstrap(app)   # using flask bootstrap
    # 針對Debug設定做說明：
    # debug=True  表示每次有異動python code都會重新reload並攔截發生的錯誤
    # debug=False 則不會進行上述動作
    #
    # 重點細節: 當debug=True時，會啟用Reloader，Flask中有引用WSGI協定(werkzeug)，其中共有兩種Reloader(stat and watchdog)，如果
    # 有安裝watchdog則優先使用watchdog。
    #
    # 在此例中app.run 啟用了debug mode，並執行run_simple方法，故會去執行run_with_reloader方法使用預設的stat reloader交由subprocess
    # 做重啟的動作(reloader中的restart_with_reloader方法)

    # 對LevelDB使用上的影響:
    # 由於在開發過程中建議會啟用debug mode，server會進行reload的行為，所以若是將leveldb.init()寫在最外層，會發現leveldb.init()被執行
    # 了兩次，而因為LevelDB是single process，是不允許新增新的process 來init leveldb，所以才會報錯。

    # 解決方式1: 既然啟用debug mode會進行reload，那可以將debug mode設為false，此時將levedb.init()寫在最外層就沒有問題，Production建議debug=False。
    # 解決方式2: 通常開發還是建議啟用debug mode，故只要把leveldb.init()的動作與啟用server (app.run)的動作區隔開即可，例如：寫在route內
    # 解決方式3: 資料庫可以宣告成class物件引入
    app.run()  # run
