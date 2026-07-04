---
Title:   RC4算法Python实现
Summary: RC4算法Python实现
Authors: Django Wong
Date:    2013-11-28
---

闲暇之时，用Python实现了一下`RC4`算法

编码 UTF-8

## class 方式

	#/usr/bin/python
	#coding=utf-8

	import sys,os,hashlib,time,base64
	class rc4:
		
		def __init__(self,public_key = None,ckey_lenth = 16):
			self.ckey_lenth = ckey_lenth
			self.public_key = public_key or 'none_public_key'
			key = hashlib.md5(self.public_key).hexdigest()
			self.keya = hashlib.md5(key[0:16]).hexdigest()
			self.keyb = hashlib.md5(key[16:32]).hexdigest()
			self.keyc = ''
		
		def encode(self,string):
			self.keyc = hashlib.md5(str(time.time())).hexdigest()[32 - self.ckey_lenth:32]
			string = '0000000000' + hashlib.md5(string + self.keyb).hexdigest()[0:16] + string
			self.result = ''
			self.docrypt(string)
			return self.keyc + base64.b64encode(self.result)
			
		def decode(self,string):
			self.keyc = string[0:self.ckey_lenth]
			string = base64.b64decode(string[self.ckey_lenth:])
			self.result = ''
			self.docrypt(string)
			result = self.result
			if (result[0:10] == '0000000000' or int(result[0:10]) - int(time.time()) > 0) and result[10:26] == hashlib.md5(result[26:] + self.keyb).hexdigest()[0:16]:
				return result[26:]
			else:
				return None
			
		def docrypt(self,string):
			string_lenth = len(string)
			result = ''
			box = list(range(256))
			randkey = []
			
			cryptkey = self.keya + hashlib.md5(self.keya + self.keyc).hexdigest()
			key_lenth = len(cryptkey)
			
			for i in xrange(255):
				randkey.append(ord(cryptkey[i % key_lenth]))
			
			for i in xrange(255):
				j = 0
				j = (j + box[i] + randkey[i]) % 256
				tmp = box[i]
				box[i] = box[j]
				box[j] = tmp
				
			for i in xrange(string_lenth):
				a = j = 0
				a = (a + 1) % 256
				j = (j + box[a]) % 256
				tmp = box[a]
				box[a] = box[j]
				box[j] = tmp
				self.result += chr(ord(string[i]) ^ (box[(box[a] + box[j]) % 256]))

测试：

	rc = rc4('nishidahuaidan')
	string = '我在这里呢，你在那里呢'
	print(string)
	str = rc.encode(string)
	print(str)
	str = rc.decode(str)
	print(str)
	
## function方式

	#/usr/bin/python
	#coding=utf-8

	import sys,os,hashlib,time,base64

	def rc4(string, op = 'encode', public_key = 'ddd', expirytime = 0):
		ckey_lenth = 4
		public_key = public_key and public_key or ''
		key = hashlib.md5(public_key).hexdigest()
		keya = hashlib.md5(key[0:16]).hexdigest()
		keyb = hashlib.md5(key[16:32]).hexdigest()
		keyc = ckey_lenth and (op == 'decode' and string[0:ckey_lenth] or hashlib.md5(str(time.time())).hexdigest()[32 - ckey_lenth:32]) or ''
		cryptkey = keya + hashlib.md5(keya + keyc).hexdigest()
		key_lenth = len(cryptkey)
		string = op == 'decode' and base64.b64decode(string[4:]) or '0000000000' + hashlib.md5(string + keyb).hexdigest()[0:16] + string
		string_lenth = len(string)
			
		result = ''
		box = list(range(256))
		randkey = []
			
		for i in xrange(255):
			randkey.append(ord(cryptkey[i % key_lenth]))
			
		for i in xrange(255):
			j = 0
			j = (j + box[i] + randkey[i]) % 256
			tmp = box[i]
			box[i] = box[j]
			box[j] = tmp
			
		for i in xrange(string_lenth):
			a = j = 0
			a = (a + 1) % 256
			j = (j + box[a]) % 256
			tmp = box[a]
			box[a] = box[j]
			box[j] = tmp
			result += chr(ord(string[i]) ^ (box[(box[a] + box[j]) % 256]))
		
		if op == 'decode':
			if (result[0:10] == '0000000000' or int(result[0:10]) - int(time.time()) > 0) and result[10:26] == hashlib.md5(result[26:] + keyb).hexdigest()[0:16]:
				return result[26:]
			else:
				return None
		else:
			return keyc + base64.b64encode(result)
			
测试：

	string = '我在这里呢，你在那里呢'
	print(string)
	str = rc4(string,'encode')
	print(str)
	rc = rc4(str,'decode')
	print(rc)