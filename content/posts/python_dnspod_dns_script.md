---
Title: Python实现DNSPod DNS动态解析脚本
Summary: 闲暇之余，在家里自建了个服务器，因为用的小区宽带，IP位动态分配。域名解析就是个问题，我的域名一般停放在DNSPod下。DNSPod有提供修改的API，就用Python简单的实现了一下动态解析。这样，就不用安装花生壳了。
Authors: Django Wong
Date: 2013-11-28
---

闲暇之余，在家里自建了个服务器，因为用的小区宽带，IP位动态分配。域名解析就是个问题，我的域名一般停放在DNSPod下。DNSPod有提供修改的API，就用Python简单的实现了一下动态解析。这样，就不用安装花生壳了。
废话不说，看代码：

	#!/usr/bin/env python
	#-*- coding:utf-8 -*-

	import httplib, urllib, urllib2
	import time
	import sys,os
	import re
	import json

	username = 'xxxx'  #账号
	password = 'xxx'  #密码
	format = 'json'

	domain = [u'www.youdomain.com']  #要解析的域名

	def get_domain_info(domain):
		domain_split = domain.split('.')
		domain_split_len = len(domain_split)
		maindomain = domain_split[domain_split_len - 2] + '.' + domain_split[domain_split_len - 1]
		return maindomain,domain

	params = {'login_email':username,'login_password':password,'format':format}

	def request(action, params, method = 'POST'):
		headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/json"}
		conn = httplib.HTTPSConnection("dnsapi.cn")
		conn.request(method, '/' + action, urllib.urlencode(params), headers)
		response = conn.getresponse()
		data = response.read()
		conn.close()
		if response.status == 200:
			return data
		else:
			return None

	def get_my_domain_id():
		data = request('Domain.List',params)
		data = json.loads(data)
		domainlist = data.get('domains')
		domaninfo = {}
		for d in domainlist:
			domaninfo[d.get('name')]  = d.get('id')
		return domaninfo

	def get_my_domain_record_id(domain_id):
		params['domain_id'] = domain_id
		data = request('Record.List',params)
		data = json.loads(data)
		if data.get('code') == '10':
			return None
		domainname = data.get('domain').get('name')
		record_list = data.get('records')
		record = {}
		for r in record_list:
			if r.get('type') == 'A':
				key = r.get('name') != '@' and r.get('name') + '.' + domainname or domainname
				record[key] = {'id':r.get('id'),'value':r.get('value')}
		return  record

	def changerecord(domain,domain_id,record_id,ip):
		params['domain_id'] = domain_id
		params['record_id'] = record_id
		params['record_type'] = 'A'
		params['record_line'] = '默认'
		params['sub_domain'] = domain
		params['ttl'] = 600
		params['value'] = ip
		data = request('Record.Modify',params)

	def getip():
		url = 'http://iframe.ip138.com/ic.asp'
		response = urllib2.urlopen(url)
		text = response.read()
		ip = re.findall(r'\d+.\d+.\d+.\d+', text)
		return ip[0] or None

	def updatedomaininfo(domain):
		m,sub_m = get_domain_info(domain)
		domain_id = my_domain_id_list.get(m)
		record_list = get_my_domain_record_id(domain_id)
		if record_list == None:
			return None
		rocord_info = record_list.get(sub_m)
		record_ip = rocord_info.get('value')
		record_id = rocord_info.get('id')
		return sub_m,record_ip,record_id,domain_id

	if __name__ == '__main__':
		my_domain_id_list = get_my_domain_id()
		try:
			for dm in domain:
				domaindata = updatedomaininfo(dm)
				if domaindata == None:
					continue
				dnsdomain,dnsdmainip,record_id,domain_id = domaindata
				domain_name = dnsdomain.split('.')[0]
				ip = getip()
				if ip == dnsdmainip:
					continue
				else:
					changerecord(domain_name,domain_id,record_id,ip)
		except:
			pass