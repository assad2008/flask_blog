---
Title: PHP安装Oracle扩展[重新整理]
Summary: 每次安装PHP的Oracle扩展，都要临时到网上找，还不一定能安装好，真是麻烦，这次重新整理一下PHP如何安装Oracle扩展！
Authors: Django Wong
Date:    2014-02-20
---

### 环境

System：CentOS 6  
PHP: 5.3.28

### 下载Oracle客户端

[32位系统](http://www.oracle.com/technetwork/topics/linuxsoft-082809.html)  
[64位系统](http://www.oracle.com/technetwork/topics/linuxx86-64soft-092277.html)

	oracle-instantclient-sqlplus-10.2.0.4-1.x86_64.rpm
	oracle-instantclient-jdbc-10.2.0.4-1.x86_64.rpm
	oracle-instantclient-devel-10.2.0.4-1.x86_64.rpm
	oracle-instantclient-basic-10.2.0.4-1.x86_64.rpm
	
执行安装:

	# rpm -ivh *.rpm
	
### 下载Oracle的PHP扩展

[官方下载](http://pecl.php.net/package/oci8)

	wget http://pecl.php.net/get/oci8-2.0.7.tgz
	# tar zxvf oci8-2.0.7.tgz
	# cd oci8-2.0.7
	# /usr/local/php/bin/phpize
	# ./configure --with-php-config=/usr/local/php/bin/php-config --with-oci8=shared,instantclient,/usr/lib/oracle/10.2.0.4/client64/lib/
	# make && make install
	
### 更改php.ini

	# vi /usr/local/php/etc/php.ini
	
增加 `extension = "oci8.so"`


### 重新启动PHP

	ps aux | grep php | grep root
	kill -USER2 php_root_pid

