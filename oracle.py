#coding=utf-8
import cx_Oracle  as cx
import sys  
import os  
import xlwt
import hashlib
import xlrd
import time

'''这个函数得功能是把售货机编号，mac地址，md5之后得mac地址，和以后要用到得key写入了一个售货机信息得文件中/'''
class  oracle_handler(object):

	def select_innercode():
		# os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.ZHS16GBK'
		# #连接数据库
		# db=cx.connect('vms5u2','12345670','60.205.220.93:1521/uatdb')
		# #定义一个游标
		# cr=db.cursor()
		# #执行一个查询操作
		# sql='select inner_code ,unique_code from t_mt_vm where vm_model_id=7002 and vm_status = 2'
		# cr.execute(sql)
		# #用rs来接受查询到得所有结果
		# rs=cr.fetchall()
		# # print(rs)
		# result=[]
		# for item in rs:
		# 	# innercode=str(item).replace('(','').replace(')','').replace(',','').replace("'","")
		# 	print(item,type(item))
		# 	# result.append(innercode)
		# 	# print(innercode,type(innercode))
		# cr.close()
		# db.close()
		# print(type(rs))
		#取出所有得结果
		# print(result)
		result=['01000002', '01000003', '01000004', '01000005', '01000006', '01000007', '01000008', '01000009', '010000010', '010000011']
		return result


	def read_mac():
		#读取mac生成文件
		f=open(r"D:\Documents\Downloads\newranmac_jb51\Mac.txt",'r')
		result=[]
		res=f.readlines()
		# for item in res:
		# 	result.append(item)
			# print(item,type(item))
		f.close()
		# print(result)
		return res


	def md5_mac():
		#获取到mac列表
		res=oracle_handler.read_mac()
		md5_mac_res=[]
		for item in res:
			# print(item)
			r=oracle_handler.Md5(item)
			# print(r)
			md5_mac_res.append(r)
		return md5_mac_res


	def Md5(src):
		m2 = hashlib.md5()   
		m2.update(src.encode('utf-8'))   
		return(m2.hexdigest())

	def md5_key():
		# innercode_list=oracle_handler.select_innercode()
		innercode_list=['01000002', '01000003', '01000004', '01000005', '01000006', '01000007', '01000008', '01000009', '010000010', '010000011']
		mac_md5_list=oracle_handler.md5_mac()
		key_result=[]
		for i in range(0,len(innercode_list)):
			str1=str(str(innercode_list[i])+str(mac_md5_list))
			re=oracle_handler.Md5(str1)
			# print(re)
			key_result.append(re)
		# print(key_result)
		return key_result


	def witer_re_to_xsl():
		#打开一个新excle
		file=xlwt.Workbook()
		#新建一个sheet
		table=file.add_sheet('innercode_码表')
		#写入表头
		# table.write(0,0,'innercode',style)
		#保存一下
		# file.save('demo.xls')
		#初始化样式
		style=xlwt.XFStyle()
		#定义字体
		font=xlwt.Font()
		font.name = 'Times New Roman'

		font.bold = True

		style.font = font 
		style2 = xlwt.easyxf('pattern: pattern solid, fore_colour yellow; font: bold on;')
		#带样式得写入

		table.write(0,0,'售货机编号',style)
		table.write(0,1,'售货机mac地址',style)
		table.write(0,2,'售货机mac地址md5值',style)
		table.write(0,3,'注册需要得key值加密后得md5',style)
		#售货机编号
		innercode=oracle_handler.select_innercode()
		#售货机mac地址
		Mac=oracle_handler.read_mac()
		#售货机mac地址md5值
		Mac_Md5=oracle_handler.md5_mac()
		#注册需要得key值加密后得md5
		Md5_key=oracle_handler.md5_key()
		i=0
		for i in range(0,len(innercode)):
			# print(innercode[i],type(innercode[i]))
			# table.write(i+1,0,'%s')%(str(innercode[i]))
			table.write(i+1,0,innercode[i])
			table.write(i+1,1,Mac[i])
			table.write(i+1,2,Mac_Md5[i])
			table.write(i+1,3,Md5_key[i])
			i+=1
		file.save('售货机信息.xls')

'''把机器号对应得mac地址写入数据库'''
class write_oracle(object):
	"""docstring for write_oracle"""
	# def __init__(self, arg):
	# 	super(write_oracle, self).__init__()
	# 	self.arg = arg
	def write_mac_to_oracle():
		#获取机器号
		innercode=oracle_handler.select_innercode()
		#获取mac得md5值
		Mac_Md5=oracle_handler.md5_mac()
		#定义Oracle数据库得编码
		os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.ZHS16GBK' 
		#连接数据库
		db=cx.connect('vms4uat','123456789','60.205.220.93:1521/uatdb')
		#定义一个游标
		cr=db.cursor()
		# print("%s,%s"%('a','n'))
		#执行一个查询操作
		i=0 
		for i in range(0,len(innercode)):
			# print(Mac_Md5[i],type(Mac_Md5[i]))
			inn=str(innercode[i]).replace('(','').replace(')','').replace(',','').replace("'","")
			# print(inn ,type(inn))
			sql=("update t_mt_vm set unique_code='%s' where inner_code ='%s'"%(Mac_Md5[i],inn))
			# print(sql)

			# sql1="select unique_code from t_mt_vm where inner_code ='01000015'"

			# cr.execute("update t_mt_vm set vm_status ='5' ,unique_code='111' where inner_code ='01000015'")
			cr.execute(sql)
			db.commit()
			#用rs来接受查询到得所有结果
			# cr.execute(sql1)-
			# rs=cr.fetchall()
			# print(rs)
			
			i+=1
			# time.sleep()
		cr.close()
		db.close()


		
if __name__ == '__main__':
	# oracle_handler.read_mac()
	# write_oracle.write_mac_to_oracle()
	# oracle_handler.witer_re_to_xsl()
	# oracle_handler.select_innercode()
	r=oracle_handler.md5_key()
	print(r)


