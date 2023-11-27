#!/usr/local/bin/python3.7
import datetime

from linebot import LineBotApi
from linebot.models import TextSendMessage

import requests
import config



# LINE
LINE_CHANNEL_ACCESS_TOKEN = config.LINE_CHANNEL_ACCESS_TOKEN

def noticeLine(dateStart, rainfall, DateEnd):
    
    line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
    
    # 該当botを友達追加している全員にメッセージを送る。
    strMessage = "" + dateStart + "から" + rainfall + "mmの雨が降ります。"

    if DateEnd != '':
        strMessage = strMessage + DateEnd + "に止む予報です。"

    line_bot_api.broadcast(TextSendMessage(text = strMessage))


# if __name__ == "__main__":
#     main()



# yahooのアプリケーションID
YAHOO_APPID = config.YAHOO_APPID

def main():

    now = datetime.datetime.now()
    timeFrom = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=7, minute=0, second=0)
    timeTo = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=21, minute=0, second=0)

    # 処理対象時間チェック
    if now < timeFrom or timeTo < now:
        return

    try:
        # 位置情報を取得
        params1 = {
            "appid": YAHOO_APPID,
            "output": "json",
            "query": config.ADDRESS
        }

        url = 'https://map.yahooapis.jp/geocode/V1/geoCoder'

        r = requests.get(url, params=params1)
        res = r.json()

        print(res["Feature"][0]["Name"]) #名称
        print(res["Feature"][0]["Geometry"]["Coordinates"]) #緯度経度
        coordinates = res["Feature"][0]["Geometry"]["Coordinates"]

        # 雨予報を取得
        params2 = {
            "appid": YAHOO_APPID,
            "coordinates": coordinates,
            "output":"json"
        }
        url = 'https://map.yahooapis.jp/weather/V1/place'

        r = requests.get(url, params=params2)
        res = r.json()

        print(res["Feature"][0]["Name"]) #名称
        print(res["Feature"][0]["Property"]["WeatherList"]["Weather"][0]["Date"]) #緯度経度      

        weatherlist = res["Feature"][0]["Property"]["WeatherList"]["Weather"]
        needNotice = False
        dateStringStart = ''
        dateStringEnd = ''
        for w in weatherlist:
            if needNotice == False:
                if w["Type"] == 'forecast': # 予測値
                    print(w['Rainfall'])
                    if w['Rainfall'] > 0:
                        needNotice = True
                        dateStringStart = w['Date']
                        rainfall = w['Rainfall']
            else:
                # 雨が止む時間
                if dateStringEnd == '':
                    if w["Type"] == 'forecast': # 予測値
                        if w['Rainfall'] == 0:
                            dateStringEnd = w['Date']

        # Lineに通知
        if needNotice:
            dateStart = datetime.datetime.strptime(dateStringStart, '%Y%m%d%H%M').strftime('%H:%M')
            if dateStringEnd != '':
                dateEnd = datetime.datetime.strptime(dateStringEnd, '%Y%m%d%H%M').strftime('%H:%M')
            else:
                dateEnd = ''

            rainfallmm = rainfall
            noticeLine(dateStart, str(rainfallmm), dateEnd)


    except Exception as err:
        print(err)

main()