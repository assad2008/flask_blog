---
Title:	Python Web开发中常用的第三方库
Summary: 经常有朋友问，如果用Python来做Web开发，该选用什么框架？用Pyramid开发Web该选用怎样的组合等问题？在这里我将介绍一些Python Web开发中常用的第三方库。基本适用于Django以外的Web框架(Pyramid, Flask, Tornado, Web.py, Bottle等).
Authors: Django Wong
Date:    2013-12-27
---
![](/static/attach/post-196.jpg)

## TL;DR

经常有朋友问，如果用Python来做Web开发，该选用什么框架？用Pyramid开发Web该选用怎样的组合等问题？在这里我将介绍一些Python Web开发中常用的第三方库。基本适用于[Django](https://www.djangoproject.com/)以外的Web框架([Pyramid](http://www.pylonsproject.org/), [Flask](http://flask.pocoo.org/), [Tornado](http://www.tornadoweb.org/en/stable/), [Web.py](http://webpy.org/), [Bottle](http://bottlepy.org/docs/dev/)等).

## ORM

- [SQLAlchemy](http://www.sqlalchemy.org/)， 在ORM方面，首选SQLAlchemy，没有之一!

	支持SQLite, PostgreSQL, MySQL, Oracle, MS-SQL, Firebird, Sybase等主流关系数据库系统  
	支持的Python环境有Python2、Python3，PyPy以及Jython。  
	主要的特性请移步 [Key Features of SQLAlchemy](http://www.sqlalchemy.org/features.html)
	推荐和数据库迁移工具[Alemic](http://alembic.readthedocs.org/en/latest/)搭配使用  
	
- [MongoEngine](http://mongoengine.org/)， 如果你用MongoDB，推荐MongoEngine

## Template Engine

在模板引擎方便选择也是比较多，有[Chameleon](http://chameleon.readthedocs.org/en/latest/)、[Jinja2](http://jinja.pocoo.org/docs/)、[Mako](http://www.makotemplates.org/)等可供选择。

## Form Engine

- [WTForms](http://wtforms.readthedocs.org/en/latest/) 推荐！

## Cache Engine & Session Store

[Beaker](http://beaker.readthedocs.org/en/latest/) 缓存和Session管理首选Beaker， 没有之一！ 可以搭配文件、dbm、memcached、内存、数据库、NoSQL等作为存储后端.如果你用Pyramid作为Web框架，那么可以直接使用[pyramid_beaker](https://github.com/Pylons/pyramid_beaker).

## Others

### 环境构建

- [buildout](http://www.buildout.org/en/latest/) 很强大，参考 [用Buildout来构建Python项目](http://lxneng.com/posts/192)  
- [virtualenv](http://www.virtualenv.org/en/latest/) 这个大家应该都用过，简单易用  

### 任务队列

- [Celery](https://github.com/celery/celery) （芹菜）一个分布式异步任务队列， 很强大！  
- [RQ](http://python-rq.org/) 这是一个轻量级的任务队列，基于Redis， 可以尝试一下。

### WebServer

- [Gunicorn](http://gunicorn.org/) , 推荐！  
- [uWSGI](http://projects.unbit.it/uwsgi/)  
- [mod_wsgi](https://code.google.com/p/modwsgi/)，搭配Apache一起使用  

### 工具

- [Fabric](http://fabfile.org/), 可以通过它完成自动化部署和常规的运维等工作。[《Fabric-让部署变得简单》_PPT](http://lxneng.com/posts/91)  
- [Supervisor](http://supervisord.org/) 一个强大的进程管理工具，用来管理各种服务（比如Gunicorn、Celery等），服务挂掉时 Supervisor 会帮自动重启服务

### 导出报表数据

- [Tablib](http://docs.python-tablib.org/en/latest/)，这个挺好用，支持导出Excel, JSON, YAML, HTML, TSV, CSV格式数据， 我创建了一个Pyramid插件可以集成到Pyramid项目中使用 [pyramid_tablib](https://github.com/lxneng/pyramid_tablib)   
- 导出PDF有[reportlab](http://www.reportlab.com/software/opensource/rl-toolkit/download/)、[PyPDF2](https://github.com/mstamy2/PyPDF2/)

### 第三方身份验证

- [velruse](https://github.com/bbangert/velruse), 支持各大网站的身份验证，国内部分我已经加入了Weibo、Douban、QQ、Taobao、Renren，并merge到主版本库中。欢迎使用！

### Helper

- [webhelpers](https://bitbucket.org/bbangert/webhelpers), 提供了一系列实用函数，[文档地址](http://sluggo.scrapping.cc/python/WebHelpers/index.html)

原文：[http://lxneng.com/posts/196](http://lxneng.com/posts/196)