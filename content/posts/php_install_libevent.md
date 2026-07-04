---
Title:   php安装libevent扩展
Summary: 原本想尝试一下PHP编写高性能网络服务，需要安装libevent扩展，没想到让人很费了点脑袋
Authors: Django Wong
Date:    2013-11-28
---

原本想尝试一下PHP编写高性能网络服务，需要安装libevent扩展，没想到让人很费了点脑袋  
先下载libevent扩展:  
<http://pecl.php.net/package/libevent>  
解压后，开始编译

	$ cd libevent-version
	$ /usr/local/php/bin/phpize
	$ ./configure --with-php-config=/usr/local/php/bin/php-config
	
结果马上报错了，错误显示为re2c版本过低。

re2c，PHP的词法解析器，官网：http://re2c.org/，下载最新的版本，编译完成。  
继续编译刚才的PHP扩展  
结果还是报错

	error: Cannot find libevent headers
	
直到这里，肯定是没找到libevent的目录，  
本地查看是否安装了libevent,  
终于在一个目录下找到了libevent-2.0.12-stable目录。  
如果未安装，则先需安装libevent。  

	wget http://cloud.github.com/downloads/libevent/libevent/libevent-2.0.20-stable.tar.gz
	tar zxvf libevent-2.0.20-stable.tar.gz
	cd libevent-2.0.20-stable/
	./configure --prefix=/usr/local/libevent-2.0.20-stable/
	make
	make install
	cd ../
	
OK,继续编译扩展

	$ cd libevent-0.0.5
	$ /usr/local/php/bin/phpize
	$ ./configure --with-php-config=/usr/local/php/bin/php-config --with-libevent=/usr/local/libevent-2.0.20-stable
	$ make && make install
	
顺利编译通过