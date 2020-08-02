# -*- coding: utf-8 -*-
from flask import Flask, render_template, session, request, redirect
import hashlib, base64
from datetime import datetime as dttm
from API import DataRequest
from API import DataRequest_report1, DataRequest_report2, DataRequest_report3, DataRequest_report4, DataRequest_report5
from collections import OrderedDict
# just use AJAX, don't import websocket
# MVC structure:
# Module:API
# View:templates
# Controll:Flask

app = Flask(__name__)

s256 = hashlib.sha256()
tstamp = dttm.now().isoformat().encode()
s256.update(b'NanRenHu' + tstamp)
app.config.update(
    SECRET_KEY = base64.b64encode(s256.digest()), 
    TEMPLATES_AUTO_RELOAD = True, 
    SEND_FILE_MAX_AGE_DEFAULT = 1
)

# 首頁
@app.route("/")
def index():
    # 檢查登入狀態
    LoginFailed = False
    session["isLogin"] = True

    tryLogin = False
    if "isLogin" in session:
        tryLogin = True
        LoginFailed = not session["isLogin"]

    return render_template("index.html", tryLogin=tryLogin, LoginFailed=LoginFailed)

# 儲存更改的停車場格式到DB、Json檔
@app.route("/store/<StoreType>/<site>", methods=["POST"])
def Store(StoreType, site):
    from bs4 import BeautifulSoup
    import json
    StoreData = []
    jsdata = request.form['javascript_data']
    jsdata = json.loads(jsdata)['html']
    soup = BeautifulSoup(jsdata, "lxml")
    
    elems = soup.find_all('td', id=False)
    import io
    # 讀取原本的Json檔
    with io.open('./static/js/ParkingLotMap_' + site +'.json', encoding='utf-8', errors='ignore') as f:
        oldData = f.read()
        oldData = json.loads(oldData, object_pairs_hook=OrderedDict)
    isNumberedData = {}

    # 由原本Json檔更改有無停車
    for CarType in oldData:
        for Area in oldData[CarType]:
            for i in oldData[CarType][Area]:
                isNumberedData[i['MacAddr']] = i['isNumbered']
    MacAddrAndPlace = []

    # 整理網頁端使用者建立的停車場格式
    for elem in elems:
        store_row = 1
        store_name = store_type = ''
        isOfficial = isDisable = isNight = isNumbered = False
        name = elem.find('input', {"name": "PlaceName"})
        if name!=None and name.has_attr('value'):
           if name['value'] != None:
                store_name = name['value']
                macaddr = elem.find('input', {"name": "PlaceMacaddr"})
                MacAddr = macaddr['value']
           else:
                store_name=' '
        else:
            continue
        store_row = int(elem.parent['id'])

        if elem.has_attr('class'):
            store_type = elem['class']
            if store_type==['official']:
                isOfficial=True
            elif store_type==['night']:
                isNight=True
            elif store_type==['disable']:
                isDisable=True
        if MacAddr in  isNumberedData:
            isNumbered = isNumberedData[MacAddr]
            
        MacAddrAndPlace.append({"MacAddr": MacAddr,
                                "Area": StoreType,
                                "Name": store_name
                                })

        StoreData.append({  "MacAddr": MacAddr,
                                "Name": store_name,
                                "isOfficial": isOfficial, 
                                "isDisable": isDisable, 
                                "isNight": isNight, 
                                "isNumbered": isNumbered,
                                "row":store_row
                                })

    if StoreType=='Bus':
        oldData['Bus']['Bus'] = StoreData
    else:
        oldData['Car'][StoreType] = StoreData
    
    with io.open('./static/js/ParkingLotMap_'+site+'.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(oldData, ensure_ascii=False))
        
    import TakeAndUpdateData
    for i in MacAddrAndPlace:
        TakeAndUpdateData.SaveMacAddress(i['MacAddr'], i['Name'], i['Area'], site)
    return 'OK'

@app.route("/API/<req>/<site>")
def API(req, site):
    return DataRequest(req, site)

@app.route("/REPORTAPI_1/<startday>")
def REPORTAPI_1(startday):
    return DataRequest_report1(startday)
    
@app.route("/REPORTAPI_2/<site>/<fromtime>/<totime>")
def REPORTAPI_2(site, fromtime, totime):
    return DataRequest_report2(site, fromtime, totime)

@app.route("/REPORTAPI_3/<site>/<fromtime>/<totime>")
def REPORTAPI_3(site, fromtime, totime):
    return DataRequest_report3(site, fromtime, totime)

@app.route("/REPORTAPI_4/<site>/<fromtime>/<totime>")
def REPORTAPI_4(site, fromtime, totime):
    return DataRequest_report4(site, fromtime, totime)

@app.route("/REPORTAPI_5/<site>/<fromtime>/<totime>/<limitData>")
def REPORTAPI_5(site, fromtime, totime, limitData):
    return DataRequest_report5(site, fromtime, totime, limitData)

@app.route("/login", methods=["POST"])
def Login():
    LoginInformation = request.form

    if (LoginInformation["account"] == 'NanRenHu_Admin') and (LoginInformation["password"] == 'NanRenHu_Password'):
        session["isLogin"] = True
    else:
        session["isLogin"] = False
    isLogin = False
    if "isLogin" in session:
        isLogin = session["isLogin"]
    return redirect("/")


def main():
    app.run(host="0.0.0.0", port=8787 , threaded=True)

if __name__ == "__main__":
    main()
