from sqlalchemy import Column, String, TIMESTAMP, Integer,create_engine
from sqlalchemy.ext.declarative import declarative_base
from collections import OrderedDict

Base = declarative_base()  # create ORM converter
LS = 'mysql+pymysql://root:nkfustBeaconData@127.0.0.1/NanRenHu_Data?charset=utf8'
engine = create_engine(LS, encoding='utf-8', pool_recycle = True)  # Link to database


class ParkingStatus(Base):
    __tablename__ = "parkingstatus"
    MacAddr = Column(String(40), primary_key=True)
    ParkingSpace = Column(String(40))
    isEmpty = Column(Integer())
    Site = Column(String(20))
    def convert_Json(self):
        jsonObj = OrderedDict([
            ("MacAddr", self.MacAddr), 
            ("ParkinSpace", self.ParkingSpace),            
            ("isEmpty", self.isEmpty),
            ("Site", self.Site)
        ])
        return jsonObj


class ParkingRecord(Base):
    __tablename__ = "parkingrecord"
    No = Column(Integer(), primary_key=True)
    ParkingSpace = Column(String(40))
    Area = Column(String(45))
    EnterOrLeave = Column(String(5))
    ParkingTime = Column(TIMESTAMP)
    Site = Column(String(20))
    
    def convert_Json(self):
        self.ParkingTime = self.ParkingTime.__str__()
        jsonObj = OrderedDict([
            ("No", self.No), 
            ("ParkinSpace", self.ParkingSpace), 
            ("Area", self.Area), 
            ("EnterOrLeave", self.EnterOrLeave), 
            ("ParkingTime", self.ParkingTime),
            ("Site", self.Site)
        ])
        return jsonObj


class ParkingEquipmentPower(Base):
    __tablename__ = "parkingequipmentpower"
    MacAddr = Column(String(40), primary_key=True)
    ParkingSpace = Column(String(40))
    Power = Column(Integer())
    Site = Column(String(20))
    
    def convert_Json(self):
        jsonObj = OrderedDict([
            ("MacAddr", self.MacAddr), 
            ("ParkinSpace", self.ParkingSpace), 
            ("Power", self.Power),
            ("Site", self.Site)
        ])
        return jsonObj
        
class MacAddress(Base):
    __tablename__ = "macaddress"
    MacAddr = Column(String(40), primary_key=True)
    PlaceName = Column(String(40))
    Area = Column(String(40))
    Site = Column(String(40))
    def convert_Json(self):
        jsonObj = OrderedDict([
            ("MacAddr", self.MacAddr), 
            ("PlaceName", self.PlaceName),
            ("Area", self.Area),
            ("Site", self.Site)
        ])
        return jsonObj
        
# class Area(Base):
    # __tablename__ = "area"
    # MacAddr = Column(String(40), primary_key=True)
    # Area = Column(String(40))
    # def convert_Json(self):
        # jsonObj = OrderedDict([
            # ("MacAddr", self.MacAddr), 
            # ("Area", self.Area)
        # ])
        # return jsonObj

Base.metadata.create_all(engine)
