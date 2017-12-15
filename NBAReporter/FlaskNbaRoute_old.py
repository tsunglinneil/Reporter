# coding=utf-8
# import class
from datetime import datetime

import Reporter
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from werkzeug.datastructures import Headers
from werkzeug.wrappers import Response

from NBAReporter import Utils, Leveldbutil

# Hint doc:
# datetime in python : https://docs.python.org/3/library/datetime.html#datetime-objects
# datetime strftime() and strptime() : https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior

app = Flask(__name__)  #define app using flask

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def nba_reporter():
    return render_template("index.html")

# Flask-Bootstrap test...
@app.route('/base')
def base():
    return render_template("base.html")


@app.route('/list', methods=['POST'])
def list():
    db = Leveldbutil.init("nbaDB")  # get database object
    URL = "http://sports.ltn.com.tw/nba"
    report = Reporter.reporter(Reporter.get_nba_report(URL))
    # print(sys.path)
    # report = None  #  For Batch Test
    if report:
        print('Report not null')
        #  以下單純以當前時間作為key(記錄到秒) 收集每一次取到的即時賽事結果
        timeForm = "%Y-%m-%d %H:%M:%S"
        today = datetime.today().strftime(timeForm)

        # 寫入DB
        Leveldbutil.insert(db, today, report)

        # 從DB取得此次即時賽事資訊並匯出音檔
        try:
            # create FileUtils object
            fileUtil = Utils.FileUtils()
            # call object method
            fileUtil.generate_sound(Leveldbutil.search(db, today))
        except:
            print("No data found : {}".format(datetime.today().strftime("%Y-%m-%d %H:%M:%S")))

            # 查看DB所有資料
            # Leveldbutil.dump(db)
    else:
        print('Start Batch Test')
        # 取得Batch
        batch = Leveldbutil.init_batch()
        # 異動或新增資料
        Leveldbutil.write_batch(batch, 'hello', 'world_hello')
        Leveldbutil.write_batch(batch, 'hello again', 'world_hello_again')
        # 寫入或更新
        Leveldbutil.commit_batch(db, batch)

        # Get test data
        get_batch_test_data(db)

        # Delete test data (批次刪除）
        Leveldbutil.delete_batch(batch, 'hello')
        Leveldbutil.delete_batch(batch, 'hello again')
        # 執行刪除
        Leveldbutil.commit_batch(db, batch)

        # Get test data
        get_batch_test_data(db)

        # 查看DB所有資料
        Leveldbutil.dump(db)

    return render_template("index.html", reportData = report)


def generate():
    with open("Sound/NBAReporter.mp3", "rb") as music:
        data = music.read(1024)
        while data:
            yield data
            data = music.read(1024)


@app.route("/download", methods=['POST'])
def download():
    headers = Headers()
    headers.set('Content-Disposition', 'attachment', filename='NBAReporter.mp3')

    return Response(generate(), mimetype='audio/mp3', headers=headers)


# ============== Get Batch Test Data ==============
def get_batch_test_data(db):
    try:
        print('Get batch data => {} and {}'.format(Leveldbutil.search(db, 'hello'), Leveldbutil.search(db, 'hello again')))
    except:
        print('Get batch data error..')

def start():
    Bootstrap(app)
    app.run(debug=True, port=8080)