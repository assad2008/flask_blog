#/usr/bin/python
#coding=utf-8

from blog.settings import REDIS_HOST,REDIS_PORT
from rc import Cache

cache = Cache(host = REDIS_HOST, port = REDIS_PORT)