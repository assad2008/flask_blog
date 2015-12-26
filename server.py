#/usr/bin/python
#coding=utf-8

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options,parse_command_line
from app.settings import WEB_LOG
from app import app

define("port", default = 8080, help = "miss port",type = int)
define("host", default = "0.0.0.0")
define("log_file_prefix",default = WEB_LOG)

def main():
	parse_command_line()
	http_server = HTTPServer(WSGIContainer(app))
	http_server.bind(options.port, options.host)
	http_server.start(1) 
	IOLoop.instance().start()
	
if __name__ == "__main__":
	main()