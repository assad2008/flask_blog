#/usr/bin/python
#coding=utf-8

from flask.ext.script import Server,Manager
from blog import create_app

app = create_app()

if __name__ == "__main__":
	app.run()
