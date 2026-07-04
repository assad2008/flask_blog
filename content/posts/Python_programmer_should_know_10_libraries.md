---
Title:   Python程序员应该知道的10个库
Summary: Python是优雅的，使用这些库可以使你的代码更简洁，并保持持久性。欢迎各位补充，并提出意见！
Authors: Django Wong
Date:    2013-12-11
---
Python是优雅的，使用这些库可以使你的代码更简洁，并保持持久性。欢迎各位补充，并提出意见！

- [Docopt](http://docopt.org/)。抛弃`optparse`和`argparse`吧，使用`docstrings`来构建优雅的，可读性强的，并且复杂（如果你需要的话）的命令行界面。IMO2013年创建的最好的库。  
- [Requests](http://www.python-requests.org/en/latest/)，或称为人类使用的HTTP，是一个处理HTTP请求更为pythonic的方法，比`urllib2`更更更好用。口碑可见，他在PyPI上下载已经超过5,000,000次 。  
- [lxml](http://lxml.de/)是`libxml2`和`libxslt`的合体。如果你要处理XML或HTML，lxml是最好的选择。  
- [Bottle](http://bottlepy.org/docs/dev/)是一个快速，简单，轻量级的`WSGI`微型web框架。几秒内就能构建小型站点和APIs。所有的框架只有一个py文件，你甚至可以放进任意目录。
- [sh](http://amoffat.github.io/sh/)是一个成熟的Python子进程界面工具，允许你像运行函数一样运行任何程序。超级好用。  
- [Structlog](http://www.structlog.org/en/0.4.0/)是一个先进的日志记录处理器。他集成了多个现存的日志记录工具，包含了Python标准库。你可以创建普通记录器，按你所想增加内容，使你的日志拥有持久性和可读性。  
- [Watchdog](http://pythonhosted.org/watchdog/)是一个跨平台的Python库和`shell`工具，可以监视文件系统事件。超级好用，并且容易上手。  
- [Delorean](http://delorean.readthedocs.org/en/latest/)可以是你用非常方便的方法来处理数据和时间。设置时区，截取到秒，分，小时，或者甚至使用特殊方法从一个数据迭代到另一个。浏览下文档，里面有很多示例。

原文：[http://blog.webwlan.cn/wordpress/?p=7951](http://blog.webwlan.cn/wordpress/?p=7951)  