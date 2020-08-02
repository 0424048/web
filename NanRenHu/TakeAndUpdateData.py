# -*- coding: utf-8 -*-
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
# from sqlalchemy.ext.declarative import declarative_base

Base = automap_base()
LS = 'mysql+pymysql://root:nkfustBeaconData@127.0.0.1/NanRenHu_Data?charset=utf8'
engine = create_engine(LS, encoding='utf-8', pool_recycle = True)  # Link to database

Base.prepare(engine, reflect=True)
# tables = Base.classes
Parking_Status = Base.classes.parkingstatus
Parking_Record = Base.classes.parkingrecord
Parking_Equipment_Power = Base.classes.parkingequipmentpower
Mac_Address = Base.classes.macaddress

session = Session(engine)

def MacAddr_getPlaceName(MacAddr):
    space = session.query(Mac_Address).filter(Mac_Address.MacAddr==MacAddr).one()
    return space.PlaceName, space.Site

def SaveParkingStatus(MacAddr, isEmpty):
    # 先從 Mac_Address找出對照placeName 再存
    
    status = Parking_Status(ParkingSpace = MacAddr_getPlaceName(MacAddr)[0], isEmpty = isEmpty, Site = MacAddr_getPlaceName(MacAddr)[1])
    session.merge(status)
    session.commit()
    status_space = status.ParkingSpace
    status_isEmpty = status.isEmpty
    return json.dumps({"ParkinSpace":status_space,"isEmpty": status_isEmpty})
    
def SaveParkingRecord(MacAddr, isEmpty, Time):
    import datetime
    timestamp = datetime.datetime.fromtimestamp(int(Time)).strftime('%Y-%m-%d %H:%M:%S')
    
    status = Parking_Record(ParkingSpace = MacAddr_getPlaceName(MacAddr)[0], EnterOrLeave = isEmpty, ParkingTime = timestamp, Site = MacAddr_getPlaceName(MacAddr)[1])
    session.merge(status)
    session.commit()
    status_space = status.ParkingSpace
    status_EnterOrLeave = status.EnterOrLeave
    status_Time = status.ParkingTime
    return json.dumps({"ParkinSpace":status_space,"EnterOrLeave": status_EnterOrLeave,"ParkinTime":status_Time})

def SaveEquipmentPower(MacAddr, Power):
    status = Parking_Record(ParkingSpace = MacAddr_getPlaceName(MacAddr)[0], Power = Power, Site = MacAddr_getPlaceName(MacAddr)[1])
    session.merge(status)
    session.commit()
    status_space = status.ParkingSpace
    status_Power = status.Power
    return json.dumps({"ParkinSpace":status_space,"Power":status_Power})
    
def SaveMacAddress(MacAddr, Name, Area , Site):
    status = Mac_Address(MacAddr = MacAddr, PlaceName = Name, Area = Area, Site = Site)
    session.merge(status)
    session.commit()
    return 'OK'
    
# def SaveArea(MacAddr, Area):
    # status = Area(MacAddr = MacAddr, Area = Area)
    # session.merge(status)
    # session.commit()
    # return 'OK'
