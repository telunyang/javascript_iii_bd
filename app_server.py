'''
請先安裝 flask、requests、beautifulsoup4 套件
pip install flask requests beautifulsoup4
'''

from flask import Flask, render_template, jsonify, request
import requests, pprint, os, json, pprint
from bs4 import BeautifulSoup

# 建立 Flask 物件
app = Flask(__name__)

''' Web API '''
# 取得 youtube 所有列表
@app.route('/linesticker', methods=['GET'])
def getYouTubeList():
    # 預設回傳訊息
    dictResponse = {"success": False, "info": "請求失敗"}

    #放貼圖資訊用
    listLineStickers = []

    # 自訂標頭
    my_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
    }

    if 'url' in request.args:
        # 官方 LINE 貼圖的網址
        url = request.args.get('url')

        # 將自訂標頭加入 GET 請求中
        response = requests.get(url, headers = my_headers)

        # 建立 soup 物件
        soup = BeautifulSoup(response.text, 'lxml')

        # 取得放置貼圖的 li 元素 (list 型態)
        li_elements = soup.select("ul.mdCMN09Ul.FnStickerList > li.mdCMN09Li.FnStickerPreviewItem")

        # 如果取得 li 元素大於 0，代表有取得資料
        if len(li_elements) > 0:
            # 逐一取得 li 元素中的 data-preview 資訊
            for li in li_elements:
                # 取得 data-preview 屬性的值(字串)
                strJson = li['data-preview'] # 另一種寫法：li.get("data-preview")
                
                #把屬性的值(字串)轉成物件 
                obj = json.loads(strJson)
                
                # 將重要資訊放置在 list 當中，幫助我們稍候進行資料下載與儲存
                listLineStickers.append({
                    "id": obj['id'],
                    "link": obj['staticUrl']
                })

            # 成功訊息
            dictResponse["success"] = True
            dictResponse["info"] = "請求成功"
            dictResponse["results"] = listLineStickers
        else:
            dictResponse["info"] = "找不到貼圖資訊"
    else:
        dictResponse["info"] = "沒有設定URL"

    # 將回傳訊息 JSON 化
    response = jsonify(dictResponse)

    # 設定 Access-Control-Allow-Origin 為「*」，任何網域的請求都會接受
    response.headers.add("Access-Control-Allow-Origin", "*")

    # 回傳結果
    return response

# 主程式區域
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5003)