#!/usr/local/bin/python3.7
import datetime


from linebot import LineBotApi
from linebot.models import TextSendMessage


# import asyncio
import requests
# import json
# from io import BytesIO
# from PIL import Image
# import query_string


# from urllib.request import Request, urlopen
# import xml.dom.minidom as MD


# # リモートリポジトリに"ご自身のチャネルのアクセストークン"をpushするのは、避けてください。
# # 理由は、そのアクセストークンがあれば、あなたになりすまして、プッシュ通知を送れてしまうからです。
LINE_CHANNEL_ACCESS_TOKEN = "myE+CwoFGrYDc69ldhD4ip4q8fmgy0zepd/4xhHn/+pT75iw9UxZ4Hr38nZX4cQ/JfG3uTyxATpJikhaAwrQF8YWycF+1OMzDybfZh0zUKMS5Bux3RV6WEog1BHGZktyOdzLkb7eSGGw3ScfVPnLagdB04t89/1O/w1cDnyilFU="


def noticeLine(dateStart, rainfall, DateEnd):
    
    line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
    
    # 該当botを友達追加している全員にメッセージを送る。
    strMessage = "" + dateStart + "から" + rainfall + "mmの雨が降ります。"

    if DateEnd != '':
        strMessage = strMessage + DateEnd + "に止む予報です。"

    line_bot_api.broadcast(TextSendMessage(text = strMessage))

    # 特定の１ユーザーに送る時はこちら。その他にも、マルチキャスト、ナローキャストがある。
    # line_bot_api.push_message('<to>', TextSendMessage(text='test message from python to one user'))



    # user_id = "プッシュ通知を送りたLINEユーザーのuser_id"

    # messages = TextSendMessage(text=f"こんにちは😁\n\n"
    #                                 f"最近はいかがお過ごしでしょうか?")
    # line_bot_api.push_message(user_id, messages=messages)




# if __name__ == "__main__":
#     main()






# アプリケーションID
APPID = 'dj00aiZpPTllWUR6WTJCQVpyNyZzPWNvbnN1bWVyc2VjcmV0Jng9MWU-'



def main():

    now = datetime.datetime.now()
    timeFrom = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=7, minute=0, second=0)
    timeTo = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=21, minute=0, second=0)

    # 処理対象時間チェック
    if now < timeFrom or timeTo < now:
        return

    try:

        # 住所の緯度経度を取得
        # params1 = {
        #     "appid": APPID,
        #     "output":"json",
        #     "query":"東京都千代田区丸の内1-1-1"
        # }
        params1 = {
            "appid": APPID,
            "output":"json",
            "query":"長野県長野市稲里町中氷鉋490"
        }

        # params1 = {
        #     "appid": APPID,
        #     "output":"json",
        #     "query":"岐阜県本巣市根尾黒津"
        # }

        url = 'https://map.yahooapis.jp/geocode/V1/geoCoder'

        r = requests.get(url, params=params1)
        res = r.json()

        print(res["Feature"][0]["Name"]) #名称
        print(res["Feature"][0]["Geometry"]["Coordinates"]) #緯度経度
        coordinates = res["Feature"][0]["Geometry"]["Coordinates"]

        # ---

        params2 = {
            "appid": APPID,
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




        # text = input("Input: ")
        # location = get_address_location("長野市")
        # weather = await get_weather_info(location)
        # weather_text = get_weather_text(weather, location)
        # print('Message:', weather_text)
        # map_image_data = await get_map_image(location)

        # with open('map.png', 'wb') as f:
        #     f.write(map_image_data)

    except Exception as err:
        print(err)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
# loop.close()

main()