# coding:utf-8
import socket
import json
import time
import threading
# from oracle import oracle_handler
import threading
from time import sleep, ctime
import multiprocessing
# from data_vb_vs import *
import data_vb_vs
from datetime import datetime
import os


#打开一个socket连接
ip_port = ('47.94.179.118', 8031)#定义端口号和IP地址
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)#开启一个心跳维护
client.connect(ip_port)#连接

#socket注册和心跳维护方法
def send_message(innerCode,key):
	message=data_vb_vs.register_data(innerCode,key)#定义一个message，返回一个注册机器的信息
	client.sendall(message)#发送信息给服务器端
	# res=client.recv(1024)
	# print(res,ctime())
	while True:
		# print('hh')
		message1=data_vb_vs.heart_data(innerCode)#定义一个message，返回一个心跳类的信息
		client.sendall(message1)#发送心跳信息到服务器
		# ret=client.recv(1024)
		# print(message1)
		time.sleep(50)#休眠50s

#接受socket消息的方法
def reserve_messsage():
	while True:
		# time.sleep(7)
		returnMessage=client.recv(40000)#用returnMessage 接受所有socket返回的消息
		if not returnMessage == '':#判断如果返回的消息不为空
			message_string_list = returnMessage.decode('utf8').split('\n')#返回的消息从byte类型转义成char类型，然后再通过‘\n’分割，用一个列表接受
			print(message_string_list, ctime())
			for message_finaly in message_string_list:#循环取出列表中的各个消息
				if not message_finaly == '':#如果消息不为空
					hasInnerCode = message_finaly.find("innerCode")#查找消息是否有"innerCode"字段
					hasMsgType = message_finaly.find("msgType")#查找消息是否有"msgType"字段
					if hasInnerCode < 0 or hasMsgType < 0:#如果message_finaly中没有"innerCode"或者"msgType"字段，跳出循环
						break
					else:
						messageRes = json.loads(message_finaly)#其他情况下，把message_fianly转化成字典格式
						if not messageRes['data'] == '':#如果messageRes的key-‘data’不为空
							if not messageRes['data']['msgType'] == 'heart':#如果收到的消息不是心跳消息
								if messageRes['data']['msgType'] == 'ask' or messageRes['data']['msgType'] == 'outSku':#如果收到的消息类型是‘ask’或者‘outSku’
									# time.sleep(7)#可以设置一个休眠
									sn = messageRes['sn']#取出收到消息中的sn
									messageSend = data_vb_vs.commenResponse_data(sn)#通过消息去把回复数据整理一下
									print(messageSend, ctime())
									client.sendall(messageSend)#发送处理后的消息
								else:
									#如果收到的消息是其他类型的消息
									sn = messageRes['sn']#获取sn
									messageSend = data_vb_vs.commenResponse_data(sn)#整理回复数据
									print(messageSend, ctime())
									client.sendall(messageSend)#发送数据

							else:
								#如果收到的消息是心跳消息，直接pass掉不用管
								pass

#定义一个多线程执行的方法
def test(innercode,key):
	threads=[]#定义一个空的线程组列表
	t1=threading.Thread(target=send_message,args=(innercode,key))#新建一个线程t1,执行send_message方法，
	threads.append(t1)#把线程t1加入threads列表
	t2=threading.Thread(target=reserve_messsage)#新建一个线程t2，执行reserve_messsage方法
	threads.append(t2)#把线程t2加入threads列表

	for t in range(0,len(threads)):
		#循环启动线程组中的线程
		threads[t].start()
	for t in range(0, len(threads)):
		#守护线程组中的线程
		threads[t].join()

if __name__ == '__main__':
	#调用方法需要两个参数，机器编号，和key
	test('01000003',"c3afea0993ce30e566ada5f967488105c3afea0993ce30e566ada5f967488105")


