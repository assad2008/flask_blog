#/usr/bin/python
#coding=utf-8

import time,datetime
import oss2
from blog.settings import OSS_KEY,OSS_SECRET,OSS_BUCKET,OSS_ENDPOINT
from blog.utils.rediscache import cache
from blog.utils import get_mk_metadata,mk2html

aliauth = oss2.Auth(OSS_KEY,OSS_SECRET)
buckets = oss2.Bucket(aliauth, OSS_ENDPOINT, OSS_BUCKET)

def get_unixtimestamp(dates):
	ndate = dates.split('-')
	dateC = datetime.datetime(int(ndate[0]),int(ndate[1]),int(ndate[2]),00,00,00)
	timestamp = time.mktime(dateC.timetuple())
	return int(timestamp)

def get_pages(total,curpage):
	from pypages import Paginator
	per_page = 10
	total = int(total)
	objects = range(1,int(total / per_page) + 2)
	page = Paginator(total, per_page, curpage)
	page.objects = objects
	return page
	
def get_page_lists(postsnum,curpage):
	pagelist = get_pages(postsnum,int(curpage))
	return pagelist

def get_post(filepath):
	filecontent = buckets.get_object(filepath).read()
	return mk2html(filecontent)
	
def get_blogs(dir):
	bloglists = []
	blogmums = 0

	bloglist_and_nums = cache.get("allblogs")
	if bloglist_and_nums is not None:
		return bloglist_and_nums.get("bloglists"),bloglist_and_nums.get("blognum")
		
	for object_info in oss2.ObjectIterator(buckets):
		filedata = dict()
		filename = object_info.key
		isexist = filename.find(dir)
		if isexist >= 0:
			if filename == dir:
				continue
			else:
				filecontent = buckets.get_object(filename).read()
				file_metadata = get_mk_metadata(filecontent)
				filedata['filename'] = filename.split('/')[1].split(".")[0]
				filedata['createtimes'] = get_unixtimestamp(file_metadata.metadata.get('Date'))
				filedata['filepath'] = filename
				filedata['Title'] = file_metadata.metadata.get("Title")
				filedata["Date"] = file_metadata.metadata.get('Date')
				filedata["Summary"] = file_metadata.metadata.get('Summary')
				bloglists.append(filedata)
				blogmums = blogmums + 1
				
	def createtime(s):
		return s['createtimes']

	bloglists = sorted(bloglists,key = createtime,reverse = True)
	cache.set("allblogs",{'bloglists' : bloglists, 'blognum' : blogmums})
	return bloglists,blogmums
	