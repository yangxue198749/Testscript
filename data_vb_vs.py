#coding=utf-8
import socket
import json
import time
import random
from oracle import oracle_handler
import threading
from time import sleep,ctime,strftime
import multiprocessing

'''定义一个生成sn得函数，直接返回一个sn'''
def SN():
	sn=int('63'+''.join(random.choice("0123456789")for i in range(17)))
	return (sn)

def register_data(innerCode,key):
    data={
    "from":"vmBox",
    "to":"kcs",
    "sn":4543543,
    "needResend":False,
    "data":{
        "msgType":"register",
        "innerCode":innerCode,
        "key":key
        }
    }
    data['sn']=SN()
    data1=json.dumps(data)
    data2=bytes(str(str(data1)+'\n'),'utf8')
    print(data2)
    # data3=bytes(data2,'utf8')
    return data2

#心跳数据处理
def heart_data(innerCode):
	data={
    "from":"vmBox",
    "to":"kcs",
    "sn":4543543,
    "needResend":False,
    "data":{
        "msgType":"heart",
        "innerCode":innerCode
    	}
	}
	data['sn']=SN()
	data1=bytes((json.dumps(data)+'\n'),'utf8')
	return (data1)

#货道信息同步
def channelPolicy_data(innerCode):
	data={
    "from":"vmBox",
    "to":"vms",
    "sn":1234567890,
    "needResend":True,
    "data":
    	{
        "innerCode":innerCode,
        "msgType":"channelPolicy"
    	}
	}
	data['sn']=SN()
	data1 = json.dumps(data)
	data2 = bytes(str(str(data1) + '\n'), 'utf8')
	return data2

#补货信息同步
def supplyPolicy_data(innerCode):
	data={
    "from":"vmBox",
    "to":"vms",
    "sn":123456,
    "needResend":True,
    "data":{
        "innerCode":innerCode,
        "msgType":"skuCfgReq"
    	}
	}
	data['sn']=SN()
	data1 = json.dumps(data)
	data2 = bytes(str(str(data1) + '\n'), 'utf8')
	return data2
	
#闪购键信息同步
def spCfgReq_data(innerCode):
	data={
    "from":"vmBox",
    "to":"vms",
    "sn":123456,
    "needResend":True,
    "data":{
        "innerCode":innerCode,
        "msgType":"spCfgReq"
    	}
	}
	data['sn']=SN()
	data1 = json.dumps(data)
	data2 = bytes(str(str(data1) + '\n'), 'utf8')
	return data2

#请求走马灯信息
def repeatTextReq_data(innerCode):
	data={
    "from":"vmBox",
    "to":"vms",
    "sn":123456,
    "needResend":True,
    "data":{
        "innerCode":innerCode,
        "msgType":"repeatTextReq"
    	}
	}
	data['sn']=SN()
	data1 = json.dumps(data)
	data2 = bytes(str(str(data1) + '\n'), 'utf8')
	return data2


#请求节能信息
def mtEnergyReq_data(innerCode):
	data={
    "from":"vmBox",
    "to":"vms",
    "sn":123456,
    "needResend":True,
    "data":{
        "innerCode":innerCode,
        "msgType":"mtEnergyReq"
    	}
	}
	data['sn']=SN()
	data1 = json.dumps(data)
	data2 = bytes(str(str(data1) + '\n'), 'utf8')
	return data2

#请求开门密码
def openDoorReq_data(innercode):
	data={
    "from":"vms",
    "to":"vmBox",
    "sn":4543543,
    "needResend":False,
    "data":{
        "msgType":"openDoorPwd",
        "innerCode":innercode,
        "versionNumber":14786268917623
        }
	}
	data['sn']=SN()
	data1 = json.dumps(data)
	data2 = bytes(str(str(data1) + '\n'), 'utf8')
	return data2

#
def vmStates_data(innercode):
	data={
    "from":"vmBox",
    "to":"vms",
    "sn":1234567890,
    "needResend":True,
    "data":{
        "innerCode":innercode,
        "msgType":"vmStatus",
        "status":{
            "vmStatus":0,
            "printerStatus":0,
            "temps":[
                {
                    "tempBoxNo":1,
                    "tempValue":10
                }
            ],
            "dateTime":"2017-01-01 23:59:59",
            "serailPortStatus":True,
            "verticalStepperMoto":True,
            "horizontalMotoStepperMoto":True,
            "slotMoto":True,
            "leftPickMoto":True,
            "rightPickMoto":True,
            "leftRotateMoto":True,
            "rightRotateMoto":True,
            "shipSensor":True,
            "mdseOnPlatform":True,
            "outputSlot":True,
            "deviceDoor":True
            }
        }
	}
	data['sn'] = SN()
	data['data']['status']['dataTime']=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	data1 = json.dumps(data)
	data2 = bytes(str(str(data1) + '\n'), 'utf8')
	return data2

#请求webapp样式
def webappStyleReq_data(innercode):
	data={
    "from":"vmBox",
    "to":"vms",
    "sn":123456,
    "needResend":True,
    "data":{
        "innerCode":innercode,
        "msgType":"webappStyleReq",
        "versionNumber":14786268917623
        }
	}
	data['sn'] = SN()
	data1 = json.dumps(data)
	data2 = bytes(str(str(data1) + '\n'), 'utf8')
	return data2

#售货机设备信息上报
def vmDeviceInfo_data(innercode):
	data={
    "from":"vmBox",
    "to":"vms",
    "sn":1234567890,
    "needResend":True,
    "data":{
        "innerCode":innercode,
        "msgType":"vmDeviceInfo",
        "deviceInfo":{
            "buttonCount":4,
            "channelCount":[11,11,11,11,11],
            "versionInfo":[
                {
                    "type":1,
                    "version":"20170324"
                },
                {
                    "type":2,
                    "version":"1.0.1"
                },
                {
                    "type":3,
                    "version":"1.0.2"
                },
                {
                    "type":4,
                    "version":"1.0.3"
                }
                ]
            }
        }
	}
	data['sn'] = SN()
	data1 = json.dumps(data)
	data2 = bytes(str(str(data1) + '\n'), 'utf8')
	return data2

#请求售货机基础信息
def vmBaseInfo_data(innercode):
	data={
    "from":"vmBox",
    "to":"vms",
    "sn":123456,
    "needResend":True,
    "data":{
        "innerCode":innercode,
        "msgType":"vmBaseInfo"
        }
	}
	data['sn'] = SN()
	data1 = json.dumps(data)
	data2 = bytes(str(str(data1) + '\n'), 'utf8')
	return data2

#请求货架信息
def skuOrderPolicy_data(innercode):
	data={
		"from": "vmBox",
		"to": "vms",
		"sn": 1234567890,
		"needResend": True,
		"data":
			{
				"innerCode": innercode,
				"msgType": "skuOrderPolicy"
			}
		}
	data['sn']=SN()
	data1 = json.dumps(data)
	data2 = bytes(str(str(data1) +'\n'),'utf8')
	return data2


#通用状态回复
def commenResponse_data(sn):
	data={
    "from":"vmBox",
    "to":"kcs",
    "sn":sn,
    "success":0
	}
	# print(json.dumps(data),type(json.dumps(data)))
	data1=bytes((json.dumps(data).replace(' ','')+'\n'),'utf8')
	# print(data1)
	return (data1)

def canVendout(sn):
	data = {
		"from": "vmBox",
		"to": "kcs",
		"sn": sn,
		"success":0
	}
	# print(json.dumps(data),type(json.dumps(data)))
	data1 = bytes((json.dumps(data).replace(' ', '') + '\n'), 'utf8')
	# print(data1)
	return (data1)


def innerCode_req():
	data={
    "from":"vmBox",
    "to":"vms",
    "sn":1234567890,
    "needResend":False,
    "data":{
    "msgType":"innerCodeReq",
    "macAddress":"cad3370665f44e929bb54b7ee7d82cc6"}
     }
	data['sn'] = SN()
	data1 = json.dumps(data)
	data2 = bytes(str(str(data1) + '\n'), 'utf8')
	return data2

# r=register_data()
# print(r)

