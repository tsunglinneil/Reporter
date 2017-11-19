import os
import webbrowser
from gtts import gTTS

# 關於static method and class method 參考文:
# http://www.wklken.me/posts/2013/12/22/difference-between-staticmethod-and-classmethod-in-python.html


class FileUtils:  # create FileUtils class
    # ==== Defined Constructor Code (For test) ====
    # <<Description:>>
    #   Python 只能存在一個建構子，也可以不用定義建構子
    #   self: 表示此Class的物件，所以如果有需求是class method call another method in the same class ==> self.methodName()
    #
    # <<Code:>>
    # def __init__(self):
    #     print(self)
    #
    # # constructor with parameter
    # def __init__(self, test1, test2):
    #     self.test1 = test1
    #     self.test2 = test2

    # 檢查並新增資料夾 (由於不需要instance相關變數or物件，所以考慮作為static function)
    def check_and_create(self, folder_name):
        check_dir = folder_name

        if os.path.exists(check_dir):  # Checks if the dir exists
            print("The directory exists")
        else:
            print("No directory found for " + check_dir)  # Output if no directory
            print()
            os.makedirs(check_dir)  # Creates a new dir for the given name
            print("Directory created for " + check_dir)

    # 產生聲音檔(含檢查作業系統) => 其實也可以作為static method，但在此練習class method
    def generate_sound(self, report):
        folder = "Sound"

        self.check_and_create(folder)

        # get path
        print(os.getcwd())
        tts = gTTS(text=report, lang='zh')
        tts.save("{}/{}/NBAReporter.mp3".format(os.getcwd(), folder))

        # 判斷當前作業系統
        sys_nm = os.name
        if sys_nm == "nt":  # os: windows
            webbrowser.open("NBAReporter.mp3")
        elif sys_nm == "posix":  # os: linus or maxos
            chrome_path = 'open -a /Applications/Google\ Chrome.app %s'  # 指定webbrower使用Chrome開啟檔案
            webbrowser.get(chrome_path).open("{}/NBAReporter.mp3".format(folder))

# ========= Test class code =========
# fileUtil = FileUtils(1,2)
# print(fileUtil.test1)
# print(fileUtil.test2)
# fileUtil.checkAndCreate("sound")
# fileUtil2 = FileUtils()
# fileUtil2.checkAndCreate("sound")
