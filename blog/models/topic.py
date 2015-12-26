#/usr/bin/python
#coding=utf-8

import oss2
from blog.utils import mk2html
from blog.settings import OSS_KEY,OSS_SECRET,OSS_BUCKET,OSS_ENDPOINT

aliauth = oss2.Auth(OSS_KEY,OSS_SECRET)
buckets = oss2.Bucket(aliauth, OSS_ENDPOINT, OSS_BUCKET)

def get_topic(filepath):
	filecontent = buckets.get_object(filepath).read()
	return mk2html(filecontent)
