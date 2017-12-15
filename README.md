# Reporter
### 概述
* 即時抓取NBA賽況資料，並轉換為MP3
* 使用Flask Web Page 呈現即時資料
* 提供MP3下載功能
* 即時播報功能
* 使用LevelDB紀錄即時資訊(以時間為單位)
* Flask-Bootstrap 測試(pip3 install flask-bootstrap)

### 執行
* 建立虛擬環境(mac):
    * 若無virtualenv module : pip3 install virtualenv
    * 建立virtualenv : virtualenv env
    * 啟動virtualenv : source env/bin/activate
    
* 安裝所需套件(2 ways)擇一執行(建議安裝到虛擬環境，故須先啟用虛擬環境):
    1. python3 setup.py install
    2. pip3 install -r requirements.txt
    
* 執行主程式:
    * python3 Main.py