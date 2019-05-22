# coding:utf-8
import socket
import threading
from time import ctime
import data_vb_vs
from vmboxDate import *


'''
模拟一个存活着的机器
'''

class Socket(object):
    def __init__(self):
        ip_port= ('47.94.179.118', 8031)
        self.client= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.client.connect_ex(ip_port)
        # print(self.client)

    def register_hear(self,innerCode,key):
        message=data_vb_vs.register_data(innerCode,key)
        self.client.sendall(message)

        while True:
            message1 = data_vb_vs.heart_data(innerCode)
            self.client.sendall(message1)
            time.sleep(10)

    def message_handler(self):
        while True:
            responseMessage=self.client.recv(40000)

            if not responseMessage == '':
                responseMessageTostring= responseMessage.decode('utf8').split('\n')
                for item in responseMessageTostring:
                    print(item)
                    if not item == '':
                        hasInnerCode = item.find("innerCode")
                        hasMsgType = item.find("msgType")
                        if hasInnerCode < 0 or hasMsgType < 0:
                            break
                        else:
                            messageRes = json.loads(item)

                            if not messageRes['data'] == '':
                                if not messageRes['data']['msgType'] == 'heart':
                                    if messageRes['data']['msgType'] == 'channelCfgs':
                                        channelData(messageRes)
                                        channelStateDate(messageRes)
                                        sn = messageRes['sn']
                                        messageSend = data_vb_vs.commenResponse_data(sn)
                                        print(messageSend, ctime())
                                        self.client.sendall(messageSend)
                                    elif messageRes['data']['msgType'] == 'channelPolicy':
                                        channelData(messageRes)
                                        channelStateDate(messageRes)
                                        sn = messageRes['sn']
                                        messageSend = data_vb_vs.commenResponse_data(sn)
                                        print(messageSend, ctime())
                                        self.client.sendall(messageSend)
                                    elif messageRes['data']['msgType'] == 'skuCfg':
                                        skuData(messageRes)
                                        sn = messageRes['sn']
                                        messageSend = data_vb_vs.commenResponse_data(sn)
                                        print(messageSend, ctime())
                                        self.client.sendall(messageSend)
                                    elif messageRes['data']['msgType'] == 'skuInfo':
                                        skuinfo(messageRes)

                                        sn = messageRes['sn']
                                        messageSend = data_vb_vs.commenResponse_data(sn)
                                        print(messageSend, ctime())
                                        self.client.sendall(messageSend)
                                    elif messageRes['data']['msgType'] == 'skuOrderPolicy':
                                        skuOrder(messageRes)
                                        sn = messageRes['sn']
                                        messageSend = data_vb_vs.commenResponse_data(sn)
                                        print(messageSend, ctime())
                                        self.client.sendall(messageSend)
                                    elif messageRes['data']['msgType'] == 'supplyPolicy':
                                        supplypolicy(messageRes)
                                        sn = messageRes['sn']
                                        messageSend = data_vb_vs.commenResponse_data(sn)
                                        print(messageSend, ctime())
                                        self.client.sendall(messageSend)
                                    elif messageRes['data']['msgType'] == 'canVendout':
                                        sn = messageRes['sn']
                                        messageSend = data_vb_vs.canVendout(sn)
                                        print(messageSend, ctime())
                                        self.client.sendall(messageSend)

                                    elif messageRes['data']['msgType'] == 'ask' or messageRes['data'][
                                        'msgType'] == 'outSku':
                                        sn = messageRes['sn']
                                        messageSend = data_vb_vs.commenResponse_data(sn)
                                        print(messageSend, ctime())
                                        self.client.sendall(messageSend)
                                    else:
                                        sn = messageRes['sn']
                                        messageSend=data_vb_vs.commenResponse_data(sn)
                                        print(messageSend, ctime())
                                        self.client.sendall(messageSend)

                                else:

                                    pass
    def test(self,innercode,key):
        threads = []
        t1 = threading.Thread(target=self.register_hear, args=(innercode, key))
        threads.append(t1)
        t2 = threading.Thread(target=self.message_handler)
        threads.append(t2)
        for t in range(0, len(threads)):
            threads[t].start()
        for t in range(0, len(threads)):
            threads[t].join()



if __name__ == '__main__':


    t=Socket()

    t.test('01000002', "c46236775fc703870e7ea71b03bbdfa5")



