---
Title:   Python apple PUSH APNSWrapper支持字典以及群发
Summary: APNSWrapper是苹果推送通知服务的Python包装。使用起来也不错。不过发现使用property的时候不支持字典
Authors: Django Wong
Date:    2013-11-30
---

`APNSWrapper`是苹果推送通知服务的Python包装。使用起来也不错。不过发现使用`property`的时候不支持字典，查阅代码：
notifications.py APNSProperty类中处理property数据

	if not isinstance(data, (int, str, list, tuple, float)):
		raise APNSValueError, "Data argument should be string, number, list of tuple"
		
可以看出，并不支持字典，由于业务需要，我们需要字典支持。

	if not isinstance(data, (int, str, list, dict, tuple, float)):
		raise APNSValueError, "Data argument should be string, number, list of tuple"

以支持字典。  
随后在`def _build(self)`方法中增加代码,需`json`支持:

	if isinstance(self.data, dict):
		return "%s%s" % (name, json.write(self.data))
		
这样我们可以定义类似如下的数据：  
{‘type’:’1′,’url’:'http://www.google.com.hk’}来支持我们的业务。  

经过查看代码，发现`APNSWrapper`支持单条发送，而APNS支持一次连接，多次发送的模式。  
修改`APNSNotificationWrapper`类

	class APNSNotificationWrapper(object):
		"""
		This object wrap a list of APNS tuples. You should use
		.append method to add notifications to the list. By usint
		method .notify() all notification will send to the APNS server.
		"""
		sandbox = True
		apnsHost = 'gateway.push.apple.com'
		apnsSandboxHost = 'gateway.sandbox.push.apple.com'
		apnsPort = 2195
		payloads = None
		connection = None
		debug_ssl = False
		kapnsconnection = None  #新建连接对象

		def __init__(self, certificate = None, sandbox = True, debug_ssl = False, \
						force_ssl_command = False):
			self.debug_ssl = debug_ssl
			self.force_ssl_command = False
			self.connection = APNSConnection(certificate = certificate, \
								force_ssl_command = self.force_ssl_command, debug = self.debug_ssl)
			self.sandbox = sandbox
			self.payloads = []


		def append(self, payload = None):
			"""Append payload to wrapper"""
			if not isinstance(payload, APNSNotification):
				raise APNSTypeError, "Unexpected argument type. Argument should be an instance of APNSNotification object"
			self.payloads.append(payload)


		def count(self):
			"""Get count of payloads
			"""
			return len(self.payloads)

			
		def notifyclose(self):  #增加关闭连接
			self.kapnsconnection.close()
		
		def notify(self):  #保持连接

			apnsConnection = self.connection

			if self.sandbox != True:
				apnsHost = self.apnsHost
			else:
				apnsHost = self.apnsSandboxHost
			if not self.kapnsconnection:
				self.kapnsconnection = apnsConnection.connect(apnsHost, self.apnsPort)
			
			return True

		def send(self):  #发送
			"""
			Send nofification to APNS:
				1) prepare all internal variables to APNS Payout JSON
				2) make connection to APNS server and send notification
			"""
			payloads = [o.payload() for o in self.payloads]
			payloadsLen = sum([len(p) for p in payloads])
			messages = []
			offset = 0

			if len(payloads) == 0:
				return False

			for p in payloads:
				plen = len(p)
				messages.append(struct.pack('%ds' % plen, p))
				offset += plen
			
			message = "".join(messages)
			self.kapnsconnection.write(message)

这样，我们就支持了连续发送的功能。  
使用方法：

	import sys,os,binascii
	import json
	import APNSWrapper

	dt = 'b9d98721 b5586b61 a00fbfa0 d61a0339 54e1bfb8 faaae3df c5a1382a 96e1a95a'
	deviceToken = binascii.unhexlify(dt.replace(' ',''))
	wrapper = APNSWrapper.APNSNotificationWrapper("/data0/pushservice/apns/certificates/wanjibaodiangaoshoupian_1122_production_push_certificates.pem", False)
	wrapper.notify()  #建立连接
	while True:
		message = APNSWrapper.APNSNotification()
		message.token(deviceToken)
		message.alert("抽烟去" + str(i))
		print("抽烟去" + str(i))
		message.sound()
		message.badge(1)
		cc = {'type':'1','url':'http://www.google.com.hk'}
		property = APNSWrapper.APNSProperty("fljt",cc)
		message.appendProperty(property)
		wrapper.append(message)
		wrapper.send() #发送
		i = i + 1
		if i == 10:
			break
	wrapper.notifyclose() #关闭连接

deviceToken可以为不同的。  
[下载](/static/attach/apns.zip)  
安装  

	python PATH/setup.py install