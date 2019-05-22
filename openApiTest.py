# coding=utf-8
import requests, json
import hashlib
import time

'''
openapitest 
'''
class openApiTEst(object):
    # 签名生成函数
    def sign(data):
        list1 = []
        for item in data:
            if item != 'sign' and item != 'skus' and item != 'cards' and item != "days":
                wd = str(str(item) + '=' + str(data[item]))
                list1.append(wd)
        list1.sort()
        str1 = str(list1)
        str2 = str1.replace("[", '').replace(']', '').replace("'", '').replace(',', '&').replace(' ', '')
        str3 = str2 + ('&key=test123456789')
        m = openApiTEst.Md5(str3)
        return (m.upper())


    def Md5(src):
        m2 = hashlib.md5()
        m2.update(src.encode('utf-8'))
        return (m2.hexdigest())

    def datahandlerOne(data):
        data1 = data
        data1["sign"] = openApiTEst.sign(data)
        return data1

    def apiRequest(data):
        try:
            url1 = 'https://open.touchfound.net/service'
            r = requests.post(url1, data=data)
            return (r.json())
        except requests.RequestException as e:
            print(e)

    # 创建订单得函数
    def testCreateOrder():
        # 要测试的数据
        data = {
            "sign": "1802CD2B54C12C5DBDA0094CCF34627A",
            "start_day": "2018-12-03",
            "end_day": "2018-12-03",
            "version": "v1",
            "skus": [
                {
                    "sku_id": "3427",
                    "sku_count": "1"
                }
            ],
            "vm_id": "01000287",
            "service": "order.create",
            "customer_id": "uH7eAtKmGNZ1Ngr0vWmh",
            "order_type": "immediate"
        }

        testcase = json.dumps(openApiTEst.datahandlerOne(data))
        result = openApiTEst.apiRequest(testcase)
        if result['return_code'] == 'SUCCESS':
            return (result)
        else:
            print('创建订单失败', result)

    def testVenout():

        data = {
            "service": "order.vendout",
            "pay_amount": "999",
            "pay_type": "k支付",
            "customer_id": "uH7eAtKmGNZ1Ngr0vWmh",
            "sign": "40B430582CEE1CD7578E95B62D804731",
            "order_seq": "35346902",
            "version": "v1",
            "notify_url": "http://xxxxxxxxx/xxx"
        }

        res1 = openApiTEst.testCreateOrder()
        print(res1, type(res1))
        if 'order_seq' in res1.keys():
            data["order_seq"] = res1['order_details'][0]['order_detail_id']
            data['sign'] = openApiTEst.sign(data)
            data1 = json.dumps(data)
            print(data1)
            res = openApiTEst.apiRequest(data1)
            print(res, time.ctime())
        else:
            orderlist = res1['detail_list']
            listorder = []
            i = 0
            for i in range(0, len(orderlist)):
                orderNum = orderlist[i]['order_detail_id']
                listorder.append(orderNum)
            print(listorder)

            for i in range(0, len(listorder)):
                data["order_seq"] = listorder[i]
                print(data)
                data['sign'] = openApiTEst.sign(data)
                testcase = json.dumps(data)
                # print(testcase,time.ctime())
                res = openApiTEst.apiRequest(testcase)
                print(res, time.ctime())

    def getVmlist():
        data = {
            "service": "list.vm",
            "version": "v1.1",
            "customer_id": "3k0p3jeS9sdksw8viHAp",
            "random_code": "f619b07c-e6c5-49a2-a224-586930909176",
            "sign": "8028D39CB745C0448000FDA4243A4643"
        }
        datahadle = json.dumps(openApiTEst.datahandlerOne(data))
        res = openApiTEst.apiRequest(datahadle)
        print(res)

    def getGoodlist():
        data = {
            "service": "list.sku",
            "version": "v1.1",
            "customer_id": "v2dDGKGNn8pkoLcgUbWJ",
            "vm_id": "01000137",
            "random_code": "f619b07c-e6c5-49a2-a224-586930909176",
            "sign": "8028D39CB745C0448000FDA4243A4643"
        }
        datahandle = json.dumps(openApiTEst.datahandlerOne(data))
        print(datahandle)
        res = json.dumps(openApiTEst.apiRequest(datahandle))
        print(res, type(res))

    def get_vm_list_detail():
        data = {
            "version": "v1",
            "sign": "1F02BC6A4A857A1B666D552C874BFFAB",
            "service": "order.query",
            "vm_id": "02000014",
            "sku_id": "21030",
            "order_seq": "39127518",
            "customer_id": "CoyFPdcsAJqhTTVL"
        }
        testcase = json.dumps(openApiTEst.datahandlerOne(data))
        print(type(testcase), testcase)



if __name__ == '__main__':
    openApiTEst.testCreateOrder()
