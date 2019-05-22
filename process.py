#coding utf-8
from time import sleep,ctime

import multiprocessing

from oracle import oracle_handler
from sck_clinte import socket_demo

def data_prepare():
	#获取机器号
	innerCode=oracle_handler.select_innercode()
	# print(innerCode)
	#获取md5key
	key=oracle_handler.md5_key()
	# print(key)
	#定义一个空数组，接受字典
	lists=[]
	for i in range(0,len(key)):
		dict_parm={}
		dict_parm['innerCode']=innerCode[i]
		dict_parm['key']=key[i]
		lists.append(dict_parm)
	print(lists)
	return (lists)


def process():
	lists =data_prepare()
	threads=[]
	files=range(len(lists))

	for i in range(0,len(lists)):
		innerCode=lists[i]['innerCode']
		# print(innerCode)
		key=lists[i]['key']
		# print(key)
		t=multiprocessing.Process(target=socket_demo.connect,args=(innerCode,key))
		threads.append(t)
		# print(threads)
	# for innerCode,key in list1.items():
	# 	t=multiprocessing.Process(target=socket_demo.connect,args=(innerCode,key))
	# 	threads.append(t)

	for t in range(0,len(lists)):
		threads[t].start()
		print("start pid",threads[t].pid,ctime())
	for t in range(0,len(lists)):
		threads[t].join()
		# print("end pid",threads[t].pid,ctime())

if __name__ == '__main__':
	process()
