
# coding:utf-8
import socket
import json
import time
import random
from oracle import oracle_handler
import threading
from time import sleep,ctime
import multiprocessing

import data_vb_vs

class socket_demo(object):
	#函数解决随机发那个socket请求得问题
	def socket_random(innerCode,i):
		# i =random.randint(1,11)
		if i >12:
			message1=data_vb_vs.heart_data(innerCode)
			# print(message1)
			return (message1)
		elif i ==2:
			message1 = data_vb_vs.channelPolicy_data(innerCode)
			return (message1)
		elif i==3:
			message1 = data_vb_vs.supplyPolicy_data(innerCode)
			return (message1)
		elif i==4:
			message1 = data_vb_vs.spCfgReq_data(innerCode)
			return (message1)
		elif i==5:
			message1 = data_vb_vs.repeatTextReq_data(innerCode)
			return (message1)
		elif i==6:
			message1 = data_vb_vs.mtEnergyReq_data(innerCode)
			return (message1)
		elif i==7:
			message1 = data_vb_vs.openDoorReq_data(innerCode)
			return (message1)
		elif i==8:
			message1 = data_vb_vs.vmStates_data(innerCode)
			return (message1)
		elif i==9:
			message1 = data_vb_vs.webappStyleReq_data(innerCode)
			return (message1)
		elif i==10:
			message1 = data_vb_vs.vmDeviceInfo_data(innerCode)
			return (message1)
		elif i==11:
			message1 = data_vb_vs.vmBaseInfo_data(innerCode)
			return (message1)
		elif i==12:
			message1 = data_vb_vs.skuOrderPolicy_data(innerCode)
			return  (message1)

	def connect(innercode,key):#定义一个函数建立一个长连接
		ip_port=('47.94.179.118',8031)
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1) #在客户端开启心跳维护
		client.connect(ip_port)
		message=data_vb_vs.register_data(innercode,key)
		client.sendall(message)
		res=client.recv(1024)
		# print(res)
		num = 2
		while True:
			if num <=12:
				message1=socket_demo.socket_random(innercode,num)
				# print(message1)
				client.sendall(message1)
				returnMessage=client.recv(60000)
				print("reciver message :",returnMessage,ctime())
				if not returnMessage =='':
					message_string_list= returnMessage.decode('utf8').split('\n')
					print (message_string_list,ctime())
					for message_finaly in message_string_list:
						if not message_finaly =='':
							hasInnerCode = message_finaly.find("innerCode")
							hasMsgType = message_finaly.find("msgType")
							if hasInnerCode < 0 or hasMsgType < 0:
								break
							messageRes=json.loads(message_finaly)
							if not messageRes['data'] =='':
								if not messageRes['data']['msgType'] == 'heart' :
									# if messageRes['data']['msgType']=='ask':
									sn=messageRes['sn']
									messageSend=data_vb_vs.commenResponse_data(sn)
									# print(messageSend,ctime())
									client.sendall(messageSend)
									print("send-message:",messageSend, ctime())
								time.sleep(2)
			else:
				message1 = socket_demo.socket_random(innercode, num)
				# print(message1)
				client.sendall(message1)
				returnMessage = client.recv(60000)
				# print("reciver message :", returnMessage, ctime())
				if not returnMessage == '':
					message_string_list = returnMessage.decode('utf8').split('\n')
					print (message_string_list,ctime())
					for message_finaly in message_string_list:
						if not message_finaly == '':
							hasInnerCode = message_finaly.find("innerCode")
							hasMsgType = message_finaly.find("msgType")
							if hasInnerCode < 0 or hasMsgType < 0:
								break
							messageRes = json.loads(message_finaly)
							if not messageRes['data'] == '':
								if not messageRes['data']['msgType'] == 'heart':
									# if messageRes['data']['msgType']=='ask':
									sn = messageRes['sn']
									messageSend = data_vb_vs.commenResponse_data(sn)
									print(messageSend,ctime())
									client.sendall(messageSend)
								else:
									messageSend = data_vb_vs.heart_data(innercode)
									print("send-message:",messageSend, ctime())
								time.sleep(0.5)
			num+=1
			print(num)



			
if __name__ == '__main__':
    socket_demo.connect('01000003',"c3afea0993ce30e566ada5f967488105c3afea0993ce30e566ada5f967488105")