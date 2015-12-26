#/usr/bin/python
#coding=utf-8

from flask import render_template
from settings import THEME_NAME

def render_templates(template, **context):
	template_path = THEME_NAME + '/' + template
	return render_template(template_path, **context)

def request_wants_json(request):
	best = request.accept_mimetypes \
	.best_match(['application/json', 'text/html'])
	return best == 'application/json' and \
	request.accept_mimetypes[best] > \
	request.accept_mimetypes['text/html']