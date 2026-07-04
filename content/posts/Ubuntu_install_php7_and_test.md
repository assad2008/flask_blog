---
Title:   Ubuntu 14.04 LTS 上安装 PHP7以及性能测试
Summary: PHP7的进度越来越快了，网上关于PHP7的介绍和测试一大堆，但是我还是想自己编译安装一下，亲自体验一下PHP7的强大和高效。
Authors: Django Wong
Date:    2015-07-10
---

文章介绍：<http://php.net/archive/2015.php#id2015-06-25-1>

下载：<https://downloads.php.net/ab/>

这个是Zend官方的介绍：<http://php7.zend.com/install-ubuntu.php>

首先安装依赖：

	apt-get update && apt-get install -y \
	libcurl4-openssl-dev \
	libmcrypt-dev \
	libxml2-dev \
	libjpeg-dev \
	libfreetype6-dev \
	libmysqlclient-dev \
	libt1-dev \
	libgmp-dev \
	libpspell-dev \
	libicu-dev \
	librecode-dev \
	libxpm4

解压，然后进行configure

	./configure --prefix=/usr/local/php7 \
	--with-config-file-path=/usr/local/php7/etc \
	--with-mcrypt=/usr/include \
	--with-mysql=mysqlnd \
	--with-mysqli=mysqlnd \
	--with-pdo-mysql=mysqlnd \
	--with-gd \
	--with-iconv \
	--with-zlib \
	--enable-xml \
	--enable-bcmath \
	--enable-shmop \
	--enable-sysvsem \
	--enable-inline-optimization \
	--enable-mbregex \
	--enable-fpm \
	--enable-mbstring \
	--enable-ftp \
	--enable-gd-native-ttf \
	--with-openssl \
	--enable-pcntl \
	--enable-sockets \
	--with-xmlrpc \
	--enable-zip \
	--enable-soap \
	--without-pear \
	--with-gettext \
	--enable-session \
	--with-curl \
	--with-jpeg-dir \
	--with-freetype-dir \
	--enable-opcache
	
熟悉的提示出来了

	+--------------------------------------------------------------------+
	| License:                                                           |
	| This software is subject to the PHP License, available in this     |
	| distribution in the file LICENSE.  By continuing this installation |
	| process, you are bound by the terms of this license agreement.     |
	| If you do not agree with the terms of this license, you must abort |
	| the installation process at this point.                            |
	+--------------------------------------------------------------------+

	Thank you for using PHP.

	config.status: creating php7.spec
	config.status: creating main/build-defs.h
	config.status: creating scripts/phpize
	config.status: creating scripts/man1/phpize.1
	config.status: creating scripts/php-config
	config.status: creating scripts/man1/php-config.1
	config.status: creating sapi/cli/php.1
	config.status: creating sapi/fpm/php-fpm.conf
	config.status: creating sapi/fpm/www.conf
	config.status: creating sapi/fpm/init.d.php-fpm
	config.status: creating sapi/fpm/php-fpm.service
	config.status: creating sapi/fpm/php-fpm.8
	config.status: creating sapi/fpm/status.html
	config.status: creating sapi/cgi/php-cgi.1
	config.status: creating ext/phar/phar.1
	config.status: creating ext/phar/phar.phar.1
	config.status: creating main/php_config.h
	config.status: executing default commands
	configure: WARNING: unrecognized options: --with-mysql

随后开始进行`make && make install`

突然出现编译错误

	ext/iconv/.libs/iconv.o:/data0/soft/php-7.0.0alpha2/ext/iconv/iconv.c:2630: more undefined references to `libiconv' follow
	ext/iconv/.libs/iconv.o: In function `php_iconv_string':
	/data0/soft/php-7.0.0alpha2/ext/iconv/iconv.c:579: undefined reference to `libiconv_open'
	/data0/soft/php-7.0.0alpha2/ext/iconv/iconv.c:591: undefined reference to `libiconv'
	/data0/soft/php-7.0.0alpha2/ext/iconv/iconv.c:609: undefined reference to `libiconv'
	/data0/soft/php-7.0.0alpha2/ext/iconv/iconv.c:619: undefined reference to `libiconv_close'
	ext/iconv/.libs/iconv.o: In function `_php_iconv_strpos':
	/data0/soft/php-7.0.0alpha2/ext/iconv/iconv.c:1004: undefined reference to `libiconv_open'
	/data0/soft/php-7.0.0alpha2/ext/iconv/iconv.c:1032: undefined reference to `libiconv'
	/data0/soft/php-7.0.0alpha2/ext/iconv/iconv.c:1146: undefined reference to `libiconv_close'
	ext/xmlrpc/libxmlrpc/.libs/encodings.o: In function `convert':
	/data0/soft/php-7.0.0alpha2/ext/xmlrpc/libxmlrpc/encodings.c:74: undefined reference to `libiconv_open'
	/data0/soft/php-7.0.0alpha2/ext/xmlrpc/libxmlrpc/encodings.c:82: undefined reference to `libiconv'
	/data0/soft/php-7.0.0alpha2/ext/xmlrpc/libxmlrpc/encodings.c:102: undefined reference to `libiconv_close'
	/data0/soft/php-7.0.0alpha2/ext/xmlrpc/libxmlrpc/encodings.c:102: undefined reference to `libiconv_close'
	collect2: error: ld returned 1 exit status
	
开始安装 libiconv (字符编码转换库)

网站地址: http://www.gnu.org/software/libiconv/  
当前版本: http://ftp.gnu.org/pub/gnu/libiconv/libiconv-1.14.tar.gz  

	$ wget http://ftp.gnu.org/pub/gnu/libiconv/libiconv-1.14.tar.gz
	$ tar zxf libiconv-1.14.tar.gz
	$ cd libiconv-1.14
	$ ./configure --prefix=/usr/local/lib/libiconv
	$ make && make install

出现

	./stdio.h:1010:1: error: 'gets' undeclared here (not in a function)

解决:

修改srclib/stdio.in.h 第695行  
如下:

	//_GL_WARN_ON_USE (gets, "gets is a security hole - use fgets instead");
	#if defined(__GLIBC__) && !defined(__UCLIBC__) && !__GLIBC_PREREQ(2, 16)
	_GL_WARN_ON_USE (gets, "gets is a security hole - use fgets instead");
	#endif

顺利编译通过`libiconv`

然后重新configure PHP7

	./configure --prefix=/usr/local/php7 \
	--with-config-file-path=/usr/local/php7/etc \
	--with-iconv=/usr/local/lib/libiconv \
	--with-mcrypt=/usr/include \
	--with-mysql=mysqlnd \
	--with-mysqli=mysqlnd \
	--with-pdo-mysql=mysqlnd \
	--with-gd \
	--with-iconv \
	--with-zlib \
	--enable-xml \
	--enable-bcmath \
	--enable-shmop \
	--enable-sysvsem \
	--enable-inline-optimization \
	--enable-mbregex \
	--enable-fpm \
	--enable-mbstring \
	--enable-ftp \
	--enable-gd-native-ttf \
	--with-openssl \
	--enable-pcntl \
	--enable-sockets \
	--with-xmlrpc \
	--enable-zip \
	--enable-soap \
	--without-pear \
	--with-gettext \
	--enable-session \
	--with-curl \
	--with-jpeg-dir \
	--with-freetype-dir \
	--enable-opcache

在Makeile的104行，加上：

	EXTRA_LIBS = -lcrypt -lz -lresolv -lcrypt -lrt -lmcrypt -lltdl -lpng -lz -ljpeg -lcurl -lz -lrt -lm -ldl -lnsl -lxml2 -lssl -lcrypto -lcurl -lxml2 -lssl -lcrypto -lfreetype -lz -lpng12 -lxml2 -lxml2 -lcrypt -lxml2 -lxml2 -lxml2 -lxml2 -lssl -lcrypto -lcrypt -liconv

编译完成：

	root@skyline:/# /usr/local/php7/bin/php -v
	PHP 7.0.0alpha2 (cli) (built: Jul 10 2015 15:19:38) 
	Copyright (c) 1997-2015 The PHP Group
	Zend Engine v3.0.0-dev, Copyright (c) 1998-2015 Zend Technologies

PHP 5.5.25的压力测试:

![](/static/attach/php5_benchmark.png)

PHP7的压力测试：

![](/static/attach/php7_benchmark.png)

同样的业务处理，PHP的性能几乎提高了一倍，看来PHP7在性能方面确实下了不少功夫，大大值得期待啊！
