#/usr/bin/python
#coding=utf-8

import os,sys
import json
from flask import Blueprint
from blog.helper import render_templates
from blog.models.post import get_post

post = Blueprint('post',__name__)

@post.route("/posts/<filename>.html")
def viewpost(filename):
	file_path = 'blogs/' + filename + '.md'
	bloginfo = get_post(file_path)
	return render_templates("posts.htm",blog = bloginfo)