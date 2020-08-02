# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from datetime import timedelta, date
import datetime
import DataCollection
from sqlalchemy import func
import time

def DataRequest(req, site):
    LS = 'mysql+pymysql://root:nkfustBeaconData@127.0.0.1/NanRenHu_Data?charset=utf8'
    linkObj = create_engine(LS, encoding='utf-8', pool_recycle = True)  # Link to database
    DBsession = sessionmaker(bind=linkObj)  # Database session maker
    session = DBsession()
    d = None
    if req == "Overview":
        d = DataCollection.ParkingStatus
    elif req == "Record":
        d = DataCollection.ParkingRecord
    elif req == "Power":
        d = DataCollection.ParkingEquipmentPower
    elif "RecordPlace-" in req:
        req = req.split('-', 1 )[1]
        d = DataCollection.ParkingRecord
        RecordList=[]
        
        for ParkingSpace in session.query(d).filter_by(ParkingSpace = req, Site = site).order_by("ParkingTime"):
            if ParkingSpace.EnterOrLeave == "1":
                RecordList.append({"I": str(ParkingSpace.ParkingTime),"L":"--"})
            elif ParkingSpace.EnterOrLeave == "0":    
                RecordList[-1]["L"] = str(ParkingSpace.ParkingTime)

        RecordDict = {"parkingRecord":RecordList, "parkingTimes":len(RecordList)}
        return json.dumps(RecordDict)
    else:
        return None
    DataObj = session.query(d).filter_by(Site = site).all()
    session.close()
    jsonData = []
    for i in DataObj:
        jsonData.append(i.convert_Json())
    jsonData = json.dumps(jsonData)
    return jsonData

def DataRequest_report1(startday):
    LS = 'mysql+pymysql://root:nkfustBeaconData@127.0.0.1/NanRenHu_Data?charset=utf8'
    linkObj = create_engine(LS, encoding='utf-8', pool_recycle = True)  # Link to database
    DBsession = sessionmaker(bind=linkObj)  # Database session maker
    session = DBsession()
    d = DataCollection.ParkingRecord
    jsonData = []
    endday = int(startday) + 86400*7
    startday = datetime.datetime.utcfromtimestamp(int(startday))
    endday = datetime.datetime.utcfromtimestamp(endday)
    #1547078400
    delta = datetime.timedelta(days=1)
    for k in session.query(d.Site).group_by(d.Site).all():
        data = []
        startday_count = startday
        while startday_count<endday:
            data.append([(startday_count - startday).days, 0])
            startday_count += delta

        for i in session.query(d.Site, d.ParkingTime, func.count(d.ParkingSpace)).filter(d.ParkingTime.between(startday, endday), d.Site == k[0]).group_by(d.Site).group_by(func.date(d.ParkingTime)).all():
            data[(i[1]-startday).days] = [(i[1]-startday).days, i[2]]
        jsonData.append({"Site": k[0],
                         "data":data})

    session.close()
    jsonData = json.dumps(jsonData)

    return jsonData

def DataRequest_report2(site, fromtime, totime):
    LS = 'mysql+pymysql://root:nkfustBeaconData@127.0.0.1/NanRenHu_Data?charset=utf8'
    linkObj = create_engine(LS, encoding='utf-8', pool_recycle = True)  # Link to database
    DBsession = sessionmaker(bind=linkObj)  # Database session maker
    session = DBsession()
    d = DataCollection.ParkingRecord
    jsonData = []
    
    fromtime = datetime.datetime.utcfromtimestamp(int(fromtime)).strftime('%Y-%m-%d %H:%M:%S')
    totime = datetime.datetime.utcfromtimestamp(int(totime)).strftime('%Y-%m-%d %H:%M:%S')
    for i in session.query(d.Area, func.count(d.ParkingSpace)).filter_by(Site = site).filter(d.ParkingTime.between(fromtime, totime)).group_by(d.Area):
        jsonData.append({"Area": i.Area,"ParkingTimes": i[1]})
    session.close()
    jsonData = json.dumps(jsonData)
    return jsonData    

def DataRequest_report3(site, fromtime, totime):
    LS = 'mysql+pymysql://root:nkfustBeaconData@127.0.0.1/NanRenHu_Data?charset=utf8'
    linkObj = create_engine(LS, encoding='utf-8', pool_recycle = True)  # Link to database
    DBsession = sessionmaker(bind=linkObj)  # Database session maker
    session = DBsession()
    d = DataCollection.ParkingRecord
    jsonData = []
    
    fromtime = datetime.datetime.utcfromtimestamp(int(fromtime)).strftime('%Y-%m-%d %H:%M:%S')
    totime = datetime.datetime.utcfromtimestamp(int(totime)).strftime('%Y-%m-%d %H:%M:%S')
    for i in session.query(d.ParkingSpace, func.count(d.ParkingSpace)).filter_by(Site = site).filter(d.ParkingTime.between(fromtime, totime)).group_by(d.ParkingSpace):
        jsonData.append({"ParkingSpace": i.ParkingSpace,"ParkingTimes": i[1]})
    session.close()
    jsonData = json.dumps(jsonData)
    return jsonData 
def GetTime(ss):
    sec = timedelta(seconds=ss)
    d = datetime.datetime(1,1,1) + sec
    return ("%d%s%d:%d:%d" % (d.day-1,u'日', d.hour, d.minute, d.second))

def DataRequest_report4(site, fromtime, totime):
    LS = 'mysql+pymysql://root:nkfustBeaconData@127.0.0.1/NanRenHu_Data?charset=utf8'
    linkObj = create_engine(LS, encoding='utf-8', pool_recycle = True)  # Link to database
    DBsession = sessionmaker(bind=linkObj)  # Database session maker
    session = DBsession()
    d = DataCollection.ParkingRecord
    jsonData = []
    
    fromtime = datetime.datetime.utcfromtimestamp(int(fromtime)).strftime('%Y-%m-%d %H:%M:%S')
    totime = datetime.datetime.utcfromtimestamp(int(totime)).strftime('%Y-%m-%d %H:%M:%S')
    TotalQuery = session.query(d.ParkingSpace, d.EnterOrLeave, d.ParkingTime).filter_by(Site = site).filter(d.ParkingTime.between(fromtime, totime)).order_by("ParkingTime")
    OutPutDict = {}
    for k in session.query(d.ParkingSpace).filter_by(Site = site).filter(d.ParkingTime.between(fromtime, totime)).group_by(d.ParkingSpace).all():
        RecordList=[]
        for i in TotalQuery:
            if(i[0]==k[0]):
                if i[1] == "1":
                    RecordList.append({"I": str(i[2]),"L":"--"})
                elif i[1] == "0":    
                    RecordList[-1]["L"] = str(i[2])
        OutPutDict[k[0]] = RecordList
    session.close()
    NewDataDict={}
    import operator
    from dateutil.relativedelta import relativedelta
    for site in OutPutDict:
        RecordList={}
        TotalTime = 0
        for record in OutPutDict[site]:
            if(record["L"]!='--'):
                distanceTime = (datetime.datetime.strptime(record["L"], '%Y-%m-%d %H:%M:%S')-datetime.datetime.strptime(record["I"], '%Y-%m-%d %H:%M:%S')).total_seconds()
                RecordList[(record["I"]+"~"+record["L"])] = distanceTime
                TotalTime += distanceTime



        longest = max(RecordList.iteritems(), key=operator.itemgetter(1))[0]
        longestTime = RecordList[longest]
        Shortest = min(RecordList.iteritems(), key=operator.itemgetter(1))[0]
        ShortestTime = RecordList[Shortest]

        NewDataDict[site] = ({"longest": longest,
                              "longestTime": GetTime(RecordList[longest]),
                              "Shortest": Shortest,
                              "ShortestTime": GetTime(RecordList[Shortest]),
                              "average": GetTime(int(TotalTime / len(OutPutDict[site])))
                            })
    jsonData = json.dumps(NewDataDict, ensure_ascii=False)
    return jsonData

def DataRequest_report5(site, fromtime, totime, limitData):
    LS = 'mysql+pymysql://root:nkfustBeaconData@127.0.0.1/NanRenHu_Data?charset=utf8'
    linkObj = create_engine(LS, encoding='utf-8', pool_recycle = True)  # Link to database
    DBsession = sessionmaker(bind=linkObj)  # Database session maker
    session = DBsession()
    d = DataCollection.ParkingRecord
    jsonData = {}
    
    fromtime = datetime.datetime.utcfromtimestamp(int(fromtime)).strftime('%Y-%m-%d %H:%M:%S')
    totime = datetime.datetime.utcfromtimestamp(int(totime)).strftime('%Y-%m-%d %H:%M:%S')
    rk = 1
    for i in session.query(d.ParkingSpace, func.count(d.ParkingSpace)).filter_by(Site = site).filter(d.ParkingTime.between(fromtime, totime)).group_by(d.ParkingSpace).order_by(func.count(d.ParkingSpace).desc()).limit(int(limitData)):
        jsonData[rk] = ({"ParkingSpace": i.ParkingSpace,"ParkingTimes": i[1]})
        rk += 1
    session.close()
    jsonData = json.dumps(jsonData)
    return jsonData 

