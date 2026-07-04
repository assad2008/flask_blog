---
Title:   Python Web 框架整理
Summary: 在各种语言平台中，python涌现的web框架恐怕是最多的,是一个百花齐放的世界，各种micro-framework、framework不可胜数；猜想原因应该是在python中构造框架十分简单，使得...
Authors: Django Wong
Date:    2014-10-21
---

## web.py

web.py 是一个轻量级Python web框架，它简单而且功能大。web.py是一个开源项目。该框架由美国作家、Reddit联合创始人、RSS规格合作创造者、著名计算机黑客Aaron Swartz开发。web.py目前已被很多家大型网站所使用。

web.py简单易学 ，掌握web.py非常容易。

代码示例：

	import web

	urls = (
		'/', 'index'
	)

	class index:
		def GET(self):
			return "Hello, world!"

	if __name__ == "__main__":
		app = web.application(urls, globals())
		app.run()
	
	
官网：[官方链接](http://webpy.org/)

## Flask

Flask是一个轻量级的Web应用框架, 使用Python编写。基于 WerkzeugWSGI工具箱和 Jinja2模板引擎。使用 BSD 授权。

Flask也被称为 “microframework” ，因为它使用简单的核心，用 extension 增加其他功能。Flask没有默认使用的数据库、窗体验证工具。然而，Flask保留了扩增的弹性，可以用Flask-extension加入这些功能：ORM、窗体验证工具、文件上传、各种开放式身份验证技术。最新版本为0.10.1

例子：

	from flask import Flask
	app = Flask(__name__)
	@app.route("/")
	def hello():    
		return "Hello World!"
	 
	if __name__ == "__main__":
		app.run()
		
官网：[官网链接](http://flask.pocoo.org/)  
相关文档：[中文文档](http://www.pythondoc.com/flask/index.html)，[Flask Mega 中文教程](http://www.pythondoc.com/flask-mega-tutorial/index.html)

## Tornado

Tornado全称Tornado Web Server，是一个用Python语言写成的Web服务器兼Web应用框架，由FriendFeed公司在自己的网站FriendFeed中使用，被Facebook收购以后框架以开源软件形式开放给大众。

- 作为Web框架，是一个轻量级的Web框架，类似于另一个Python web 框架Web.py，其拥有异步非阻塞IO的处理方式。  
- 作为Web服务器，Tornado有较为出色的抗负载能力，官方用nginx反向代理的方式部署Tornado和其它Python web应用框架进行对比，结果最大浏览量超过第二名近40%。

代码示例：

	import tornado.ioloop
	import tornado.web

	class MainHandler(tornado.web.RequestHandler):
		def get(self):
			self.write("Hello, world")

	application = tornado.web.Application([
		(r"/", MainHandler),
	])

	if __name__ == "__main__":
		application.listen(8888)
		tornado.ioloop.IOLoop.instance().start()

官网：[访问官网](http://www.tornadoweb.org/en/stable/)  
中文：[中文网站](http://www.tornadoweb.cn/)  
文档：[中文文档](http://www.tornadoweb.cn/documentation)，[英文文档](http://www.tornadoweb.org/en/stable/guide.html)

## Bottle

Bottle是一个Python Web框架，整个框架只有一个文件，几十K，却自带了路径映射、模板、简单的数据库访问等web框架组件，确实是个可用的框架。初学web开发可以拿来玩玩，其语法简单，部署也很方便。

代码示例：

	from bottle import route, run, template
	@route('/hello/:name')
	def index(name='World'):   
		 return template('<b>Hello {{name}}</b>!', name=name)
	 run(host='localhost', port=8080)
	 
官网：[访问官网](http://bottlepy.org/)  
文档：[英文文档](http://bottlepy.org/docs/0.12/)

## Pylons

Pylons是一个开放源代码的Web应用框架，使用python语言编写。它对WSGI标准进行了扩展应用，提升了重用性且将功能分割到独立的模块中。

Pylons是最新的Web应用框架中的典型，类似于Django和TurboGears。Pylons受Ruby on Rails影响很深：它的两个组件，Routes和WebHelpers是Rails特性的Python实现。

官网：[访问官网](http://www.pylonsproject.org/projects/pylons-framework/about)  
相关文章：[Python + Pylons环境安装](http://www.cnblogs.com/libingql/archive/2011/06/27/2091383.html)


## Pyramid

Pyramid是一个小型，快速，接地气的 Python web framework. 它是Pylons Project的一部分. 采用的授权协议是BSD-like license.

官网：[访问官网](http://www.pylonsproject.org/projects/pyramid/about)  
相关文章： 
 
- [用pyramid创建一个完整的WEB Project](http://luchanghong.com/python/2012/06/12/creater-a-complete-web-project.html)    
- [Python实战开发之Pyramid Web框架在商城项目中的应用实战资料](http://www.oschina.net/question/1181061_118365)


## Quixote

Quixote是由美国全国研究创新联合会（CNRI，Corporation for National Research Initiatives）的工程师A.M.Kuchling、Neil Schemenauer和Greg Ward开发的一个轻量级Web框架。和几乎所有的开源项目一样，Quixote也是为了满足实际需要而出世的

国内的最大的用Python开发的网`豆瓣网`是用Quixote开发的。我只简单翻了一下源代码，没有做过研究，不发表评论，有经验的来补充下。我只是在想，如果豆瓣网交到现在来开发，应该会有更多的选择。

官网：[访问官网](http://www.quixote.ca/)  
相关文章：[豆瓣动力核心——Quixote](http://www.cnblogs.com/bvbook/archive/2009/08/13/1545250.html)

## Zope2

Zope 2是一款基于Python的Web应用框架，是所有Python Web应用程序、工具的鼻祖，是Python家族一个强有力的分支。Zope 2的“对象发布”系统非常适合面向对象开发方法，并且可以减轻开发者的学习曲线，还可以帮助你发现应用程序里一些不好的功能。

官网：[访问官网](http://zope2.zope.org/)

## Django

Django是一个开放源代码的Web应用框架，由Python写成。采用了MVC的软件设计模式，即模型M，视图V和控制器C。它最初是被开发来用于管理劳伦斯出版集团旗下的一些以新闻内容为主的网站的，即是CMS（内容管理系统）软件。并于2005年7月在BSD许可证下发布。这套框架是以比利时的吉普赛爵士吉他手Django Reinhardt来命名的

官网：[访问官网](https://www.djangoproject.com/)  
中文社区：[中文社区](http://www.djangochina.cn/)


---------------------------------

以上部分内容来自互联网，如有侵权，敬请联系我
