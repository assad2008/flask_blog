---
Authors: Django Wong
Date: 2013-11-30
Summary: 简单的一个python日志处理类
Title: python简单日志处理
seo_description: 本文介绍了一个简单的Python日志处理类，包含完整的代码示例。通过logsys类实现日志写入、格式化时间戳和自定义通知功能，适合Python开发者快速集成日志记录到项目中。代码简洁易用，支持UTF-8编码和多种数据类型处理。
seo_keywords: Python日志处理, Python日志类, 日志记录代码, Python日志示例
---

简单的一个python日志处理类

```python
#/usr/bin/python
#coding=utf-8

import time,types

class logsys:
	
	def __init__(self, project, logfilename = 'sys_log.txt'):
		self.project = project
		self.logfilename = logfilename
		
	def get_log_time(self):
		return time.strftime("%Y-%m-%d %X", time.localtime())
	
	def write2file(self, *formart):
		s = self.formart_string(*formart)
		if s:
			encoding = 'utf8'
			out = open(self.logfilename, 'a+')
			out.write(s + "\n")
			out.close()
		else:
			pass
	
	def formart_string(self, *formart):
		string = ''
		encoding = 'utf8'
		for str in formart:
			if not type(str) in [types.UnicodeType, types.StringTypes, types.StringType]:
				s = repr(str)
			else:
				s = str
			if type(s) == type(u''):
				string += s.encode(encoding) + "\t"
			else:
				string += s + "\t"
		return string
	
	def w(self,notice,*formart):
		self.write2file(self.get_log_time(), '[' + notice + ']', self.project, *formart)
```