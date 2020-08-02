# -*- coding: utf-8 -*-
import json
import datetime
import paho.mqtt.client as mqtt
import TakeAndUpdateData
import io
# MQTT Settings
MQTT_Broker = "163.18.26.106"
MQTT_Topic = "MPlace/G08_APP/#"
MQTT_Port = 1883
Keep_Alive_Interval = 45
cn = 0
print('Go')
def on_connect(self, mosq, obj, rc):
    mqttc.subscribe(MQTT_Topic, 0)

def on_message(mosq, obj, msg):
    gps_handler(msg.topic, msg.payload)

def gps_handler(Topic, jsonData):
    try:
        global cn
        jsonData = str(jsonData, encoding = "utf-8")
        json_Dict = json.loads(jsonData)
        print(str(cn) + ')')
        
        if json_Dict['C'] == 'RP':
            json_Dict['C'] = 'Device report data'
            if json_Dict['I'] == '0001':    # power report
                print('power')
                # DB - EquipmentPower
                TakeAndUpdateData.SaveEquipmentPower(json_Dict['M'], json_Dict['V'])
            if json_Dict['I'] == '0500':    # in/out report
                print('in/out')
                ################ ->Find site
                Site = TakeAndUpdateData.MacAddr_getPlaceName(json_Dict['M'])[1]
                print(Site)
                with io.open('.\static\js\ParkingLotMap_' + Site +'.json', encoding='utf-8', errors='ignore') as f:
                    jsonRecordData = f.read()
                    jsonRecordData = json.loads(jsonRecordData)
                if json_Dict['V'] == '03' or json_Dict['V'] == '0B':  # 有車
                    # DB - ParkingStatus // ParkingRecord // Json - isNumbered
                    TakeAndUpdateData.SaveParkingStatus(json_Dict['M'], 1)
                    TakeAndUpdateData.SaveParkingRecord(json_Dict['M'], 1, json_Dict['T'])
                    for CarType in jsonRecordData:
                        for Area in jsonRecordData[CarType]:
                            for i in jsonRecordData[CarType][Area]:
                                if i['MacAddr'] == json_Dict['M']:
                                    i['isNumbered'] = True

                if str(json_Dict['V']) == '00' or  str(json_Dict['V']) == '08':  # 沒車
                    TakeAndUpdateData.SaveParkingStatus(json_Dict['M'], 0)
                    TakeAndUpdateData.SaveParkingRecord(json_Dict['M'], 0, json_Dict['T'])
                    for CarType in jsonRecordData:
                        for Area in jsonRecordData[CarType]:
                            for i in jsonRecordData[CarType][Area]:
                                if i['MacAddr'] == json_Dict['M']:
                                    i['isNumbered'] = False
                with io.open('.\static\js\ParkingLotMap_' + Site +'.json', 'w', encoding='utf-8') as f:
                    f.write(json.dumps(jsonRecordData, ensure_ascii=False))
        elif json_Dict['C'] == 'SR':
            json_Dict['C'] = 'Broadcast timestamp'
            print('Type: ' + json_Dict['C'])
            print('Macaddr: ' + json_Dict['M'])
            print('Timestamp: ' + json_Dict['T'])
        elif json_Dict['C'] == 'PN':
            json_Dict['C'] = 'Reply push notice from gateway'

        
        
        cn += 1

    except ValueError:
       print('ValueError:' + jsonData)

    except KeyError:
       print('KeyError')

def on_subscribe(mosq, obj, mid, granted_qos):
    pass

mqttc = mqtt.Client()

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

user = "flask"
password = "flask"
mqttc.username_pw_set(user, password)
# Connect
mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))

# Continue the network loop
mqttc.loop_forever()
