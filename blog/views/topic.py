#/usr/bin/python
#coding=utf-8

import sys,os
from flask import Blueprint
from blog.helper import render_templates
from blog.models.topic import get_topic

topic = Blueprint('topic',__name__)

@topic.route("/topic/<filename>.html", methods = ["GET"])
def viewtopic(filename):
	file_path = 'topics/' + filename + '.md'
	topicinfo = get_topic(file_path)
	return render_templates("topic.htm",topics = topicinfo)
