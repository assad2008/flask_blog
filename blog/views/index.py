#/usr/bin/python
#coding=utf-8

import os,sys
from flask import Blueprint
from blog.helper import render_templates
from blog.models.post import get_blogs,get_page_lists
from blog.settings import PER_PAGE

index = Blueprint('index',__name__)

@index.route("/")
@index.route("/page/<int:page>.html")
def default(page = 1):
	blog_lists,blognum = get_blogs("blogs/")
	pages = get_page_lists(blognum,page)
	if page > 1:
		start = (page - 1) * PER_PAGE - 1
	else:
		start = 0
	end = page * PER_PAGE - 1
	return render_templates("index.htm",blogs = blog_lists[start:end],pages = pages)
	
@index.route("/archives.html")
def archives():
	blog_lists,blognum = get_blogs("blogs/")
	return render_templates("archives.htm",blogs = blog_lists)