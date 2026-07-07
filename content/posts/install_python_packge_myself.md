---
Authors: Django Wong
Date: 2015-02-13
Summary: 一般配置完Python环境的时候，我自己经常会先安装一些自己常用的package或者会用到的package
Title: 我自己常用的一些Python Package
seo_description: 本文整理了作者常用的Python Package清单，涵盖Web框架（Tornado、Flask）、数据库（MySQL-Python、pymongo）、网络工具（requests、gevent）、爬虫（Scrapy、BeautifulSoup）及系统管理（Fabric、supervisor）等类别，为Python开发者提供实用参考。
seo_keywords: Python Package, 常用Python库, Python开发工具, Python框架, Python爬虫
---

一般安装完Python后，我会先装一些常用的Package。做个笔记，记录下来，以备查询

## Web FrameWorks

- Tornado，访问：<http://www.tornadoweb.org/en/stable/>  
- Flask，访问：<http://flask.pocoo.org/>  
- Web.py，访问：<http://webpy.org/>  

## Tools

- xlrd，Excel处理利器，访问：<http://www.python-excel.org/>  
- lxml，XML处理,访问：<http://lxml.de/>    
- configparser，ini文件解析，访问：<https://docs.python.org/2/library/configparser.html>  
- uuid，生成uuid，访问：<https://docs.python.org/2/library/uuid.html>   
- msgpack-python，类似JSON的一个数据序列化，访问：<https://pypi.python.org/pypi/msgpack-python/>  
- psutil，一个用于获得处理器和系统相关信息的模块，访问：<https://github.com/giampaolo/psutil>    
- Boltons 一个纯 Python 工具集，超过 100 个实用工具。 访问：<https://github.com/mahmoud/boltons>  

## Database

- MySQL-Python，Mysql库，访问：<https://pypi.python.org/pypi/MySQL-python>  
- pymongo，MongoDB库，访问：<https://github.com/mongodb/mongo-python-driver>  
- redis，Redis库，访问：<https://pypi.python.org/pypi/redis/>  
- cxOracle，Oracle库，访问：<https://pypi.python.org/pypi/cx_Oracle>  
- SQLAlchemy，SQL工具包及对象关系映射（ORM）工具，访问：<http://www.sqlalchemy.org/> 
- peewee， SQL工具包及对象关系映射（ORM）工具，访问：<https://pypi.python.org/pypi/peewee>  
- torndb，Tornado原装DB，访问：<https://github.com/bdarnell/torndb>

## Net

- requests，最好用的http工具，访问：<http://www.python-requests.org/>  
- grequests，Requests + Gevent，访问：<https://github.com/kennethreitz/grequests>
- gevent，一个高并发的网络性能库，访问：<http://www.gevent.org/>  
- twisted，基于事件驱动的网络引擎框架。访问：<https://twistedmatrix.com/trac/>  

## System

- sh，强大的系统系统管理神器，访问：<https://pypi.python.org/pypi/sh>

## SSH
  
- Fabric，是一个 Python (2.5 或更高) 库和命令行工具，用于连接到SSH服务器并执行命令。访问：<http://www.fabfile.org/>  
- paramiko，python语言写的一个模块，遵循SSH2协议，支持以加密和认证的方式，进行远程服务器的连接。访问：<http://www.paramiko.org/>

## Files

- Pathlib，文件和路径处理 <https://pathlib.readthedocs.org/en/pep428/>
- watchdog，Python库和Shell实用程序来监视文件系统事件，访问：<https://github.com/gorakhargosh/watchdog>

## Date

- Arrow，好用的时间处理库，访问：<http://crsmithdev.com/arrow/>  
- when.py，友好的时间日期库，访问：<https://github.com/dirn/When.py>  

## Image

- PIL，Python Imaging Library，处理图像，很强大，访问：<http://www.pythonware.com/products/pil/> 
- Pillow，是 PIL 的替代版本，PIL 软件包提供了基本的图像处理功能。访问：<http://python-pillow.github.io/>

## Spider

- PyQuery ，解析网页，访问：<https://pypi.python.org/pypi/pyquery>  
- beautifulSoup，分析网页，访问：<https://pypi.python.org/pypi/beautifulsoup4>  
- Scrapy，著名的爬虫框架，访问：<http://www.scrapy.org/>  

## Other

- Jinja2，模板引擎，<https://pypi.python.org/pypi/Jinja2> 
- virtualenv，Python虚拟环境，访问：<https://pypi.python.org/pypi/virtualenv/>  
- libmc，一个高效轻便的C++/Python Memcached 客户端库。访问：<https://github.com/douban/libmc>  
- Celery，分布式任务调度模块。访问：<http://www.celeryproject.org/>  
- supervisor，是用Python实现的一款非常实用的进程管理工具 访问：<http://supervisord.org/>
- Logbook，一个日志处理类 <https://pypi.python.org/pypi/Logbook>

## String

- xpinyin 一个汉字转拼音的库，访问：<https://github.com/lxneng/xpinyin>  
- shortuuid 生成简洁，明确，URL安全的UUID。访问 <https://github.com/stochastic-technologies/shortuuid>
- python-user-agents 一个Python库，提供了一个简单的方法通过解析（浏览器）用户代理字符串来确定，如移动电话，平板电脑及其能力的设备。 访问:<https://github.com/selwin/python-user-agents>  
- jieba "结巴"中文分词：做最好的 Python 中文分词组件，访问：<https://pypi.python.org/pypi/jieba/>

## Cryption

- pyDes DES处理，访问：<http://sourceforge.net/projects/pydes/>
- RSA python RSA处理库，访问：<https://pypi.python.org/pypi/rsa>

## RESTful APIs

- Eve 一款Python的REST API框架，用于构建和部署高可定制的、全功能的RESTful的Web服务。访问：<http://python-eve.org/>  
- Django REST 框架可以轻松部署web APIs，其是一个聚健壮性与弹性于一体的web工具包。访问：<http://www.django-rest-framework.org/>  
- Flask-RESTful 基于Flask框架开发的Rest APIs。访问：<https://github.com/flask-restful/flask-restful>