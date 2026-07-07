---
Authors: Django Wong
Date: 2014-02-20
Summary: 每次安装PHP的Oracle扩展，都要临时到网上找，还不一定能安装好，真是麻烦，这次重新整理一下PHP如何安装Oracle扩展！
Title: PHP安装Oracle扩展[重新整理]
seo_description: 本文详细介绍了在CentOS 6系统下为PHP 5.3.28安装Oracle扩展的完整步骤，包括下载Oracle客户端、安装oci8扩展、配置php.ini及重启PHP服务。解决PHP连接Oracle数据库的常见问题，适合需要集成Oracle数据库的PHP开发者参考。
seo_keywords: PHP安装Oracle扩展, oci8扩展, CentOS安装Oracle客户端, PHP连接Oracle数据库
---

### 环境

System：CentOS 6  
PHP: 5.3.28

### 下载Oracle客户端

[32位系统](http://www.oracle.com/technetwork/topics/linuxsoft-082809.html)  
[64位系统](http://www.oracle.com/technetwork/topics/linuxx86-64soft-092277.html)

```php
oracle-instantclient-sqlplus-10.2.0.4-1.x86_64.rpm
oracle-instantclient-jdbc-10.2.0.4-1.x86_64.rpm
oracle-instantclient-devel-10.2.0.4-1.x86_64.rpm
oracle-instantclient-basic-10.2.0.4-1.x86_64.rpm
```

执行安装:

```php
# rpm -ivh *.rpm
```

### 下载Oracle的PHP扩展

[官方下载](http://pecl.php.net/package/oci8)

```php
wget http://pecl.php.net/get/oci8-2.0.7.tgz
# tar zxvf oci8-2.0.7.tgz
# cd oci8-2.0.7
# /usr/local/php/bin/phpize
# ./configure --with-php-config=/usr/local/php/bin/php-config --with-oci8=shared,instantclient,/usr/lib/oracle/10.2.0.4/client64/lib/
# make && make install
```

### 更改php.ini

```php
# vi /usr/local/php/etc/php.ini
```

增加 `extension = "oci8.so"`


### 重新启动PHP

```php
ps aux | grep php | grep root
kill -USER2 php_root_pid
```