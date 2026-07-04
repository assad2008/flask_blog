---
Title:   Python脚本POST上传数据以及文件
Summary: 查了众多，发现都不满意，不是这里有问题，就是那里有问题，真是郁闷，最后参照新浪微博Python SDK写了一个。花了我两个小时，毕竟初学Python，写的不好，分享一下
Authors: Django Wong
Date:    2013-11-30
---

	#/usr/bin/python
	#author Yee <rlk002@gmail.com>
	#coding=utf-8

	import sys,os,urllib2
	import mimetypes
	import mimetools

	def get_content_type(filepath):
		return mimetypes.guess_type(filepath)[0] or 'application/octet-stream'

	def encode_multipart_formdata(fields, files = {}):
		boundary = mimetools.choose_boundary()
		CRLF = '\r\n'
		data = []
		for key in fields:
			data.append('--' + boundary)
			data.append('Content-Disposition: form-data; name="' + key + '"')
			data.append('')
			data.append(fields[key])
		for key in files:
			data.append('--' + boundary)
			data.append('Content-Disposition: form-data; name="'+ key +'"; filename="'+ files[key]['filename'] + '"')
			data.append('Content-Type: "' + files[key]['type'] + '"')
			data.append('')
			data.append(files[key]['filedata'])
		data.append('--' + boundary + '--')
		data.append('')
		body = CRLF.join(data)
		content_type = 'multipart/form-data; boundary=%s' % boundary
		return {'content_type':content_type,'body':body}

	def http_call(url,params,files = {}):
		params = encode_multipart_formdata(params, files)
		req = urllib2.Request(url, data = params['body'])
		if  params['content_type']:
			req.add_header('Content-Type',params['content_type'])   
		resp = urllib2.urlopen(req)
		body = resp.read()
		return body
		
	def httpopenfile(url):
		filedata = urllib2.urlopen(url)
		data = filedata.read()
		fileinfo = filedata.info()
		if fileinfo.has_key("Content-Length"):
			filesize = fileinfo["Content-Length"]
		else:
			filesize = 0
		filename = os.path.basename(url)
		filetype = get_content_type(filename)
		fileInfo = {'filename':filename,'size':filesize,'type':filetype,'filedata':data}
		return fileInfo
		
		
	def sendwb(url,data,imgpath = ''):
		if imgpath != '':
			file = httpopenfile(imgpath)
			ret = http_call(url,data,files = {'file':file})
			return;
		ret = http_call(url,data)