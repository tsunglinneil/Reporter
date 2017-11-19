# import class
import sys
from Crawler import Reporter, Utils

# ============== Main ==============

URL = "http://sports.ltn.com.tw/nba"
report = Reporter.reporter(Reporter.get_nba_report(URL))
print(sys.path)
if report:
    # create FileUtils object
    fileUtil = Utils.FileUtils()
    # call object method
    fileUtil.generate_sound(report)