#/usr/bin/python
#coding=utf-8

import sys
from flask import Flask
from blog.views import index,post,topic
from blog.settings import APP_NAME, DEBUG
from blog.helper import render_templates

APP_MODULES = (index,post,topic)

def configure_modules(app, modules):
	for module in modules:
		app.register_blueprint(module)
	
def configure_errorhandlers(app):
	@app.errorhandler(404)
	def page_not_found(error):
		return render_templates("404.htm")

	@app.errorhandler(500)
	def server_error(error):
		return render_templates("500.htm")
		
def create_app(modules = None):
	if modules is None:
		modules = APP_MODULES   
	app = Flask(APP_NAME)
	app.debug = DEBUG
	configure_errorhandlers(app)
	configure_modules(app, modules)
	return app