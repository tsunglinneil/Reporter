# coding=utf-8
import requests
from bs4 import BeautifulSoup

# Coding Style Check:
# 最高層級的Class or Function 必須間隔兩行
# Function 與其參數命名必須要符合小寫規則，且依據可讀性適時地用底線分隔
# 字典中Key: Value (冒號後需空白)
# 想在程式碼同一行後加上註解建議先以兩個空白做分隔 在下註解符號 (Ex: 第64行)


def get_nba_report(url):
    resp = requests.get(url)
    if resp.status_code is 200:
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text.encode(), 'html.parser')

        # get main scope
        main_scope = soup.find("ul", {"class", "times"})

        # find class contain key word 'daytomove'
        li_scope = main_scope.select('li[class*="daytomove"]')

        return li_scope


def message_process(description, a_team, b_team, index):
    a_team_msg = msg_detail(a_team)
    b_team_msg = msg_detail(b_team)

    if index == 0:
        description += "比賽賽況\n"
    else:
        description = ""

    return "{} {}對上{} 比數 {}比{}".format(
                                    description,
                                    a_team_msg["team"],
                                    b_team_msg["team"], a_team_msg["score"], b_team_msg["score"]
    )


def msg_detail(team_data):
    # Get score and team name
    detail_dicts = {
                    "score": str(next(iter(team_data.find('span')))),
                    "team": str(team_data.find('span').next_sibling)
    }
    return detail_dicts


def reporter(scope_data):
    # To read
    report_msg = ""

    if scope_data:
        title = "NBA 即時賽事"
        end = "掰掰囉"

        for i in range(len(scope_data)):
            # Game Tile (Date and some information)
            description = scope_data[i].select(".s_time")[0].text
            game_num = len(scope_data[i].select(".s_01"))

            detail_msg = ""
            for j in range(game_num):
                a_team = scope_data[i].select(".s_01")[j].select("li")[1]  # A team's infomation
                b_team = scope_data[i].select(".s_02")[j].select("li")[1]  # B team's infomation

                detail_msg = "{}\n{}".format(
                                        detail_msg,
                                        message_process(description, a_team, b_team, j)  # Message process
                )

            report_msg = "{}\n{}".format(report_msg, detail_msg)

        report_msg = "{}\n{}\n{}".format(title, report_msg, end)
        # print(report_msg)
        # print("="*100)

    return report_msg

