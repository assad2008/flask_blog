---
Authors: Django Wong
Date: 2013-11-28
Summary: 原本想尝试一下PHP编写高性能网络服务，需要安装libevent扩展，没想到让人很费了点脑袋
Title: php安装libevent扩展
seo_description: 本文详细介绍了在PHP中安装libevent扩展的完整步骤，包括解决re2c版本过低和找不到libevent头文件等常见错误。通过编译安装libevent库和PHP扩展，帮助开发者实现高性能网络服务。适合PHP开发者参考。
seo_keywords: PHP安装libevent扩展, libevent扩展编译, PHP高性能网络服务, re2c错误解决, PHP扩展安装教程
---

原本想尝试一下PHP编写高性能网络服务，需要安装libevent扩展，没想到让人很费了点脑袋  
先下载libevent扩展:  
<http://pecl.php.net/package/libevent>  
解压后，开始编译

```php
$ cd libevent-version
$ /usr/local/php/bin/phpize
$ ./configure --with-php-config=/usr/local/php/bin/php-config
```

结果马上报错了，错误显示为re2c版本过低。

re2c，PHP的词法解析器，官网：http://re2c.org/，下载最新的版本，编译完成。  
继续编译刚才的PHP扩展  
结果还是报错

```php
error: Cannot find libevent headers
```

直到这里，肯定是没找到libevent的目录，  
本地查看是否安装了libevent,  
终于在一个目录下找到了libevent-2.0.12-stable目录。  
如果未安装，则先需安装libevent。  

```php
wget http://cloud.github.com/downloads/libevent/libevent/libevent-2.0.20-stable.tar.gz
tar zxvf libevent-2.0.20-stable.tar.gz
cd libevent-2.0.20-stable/
./configure --prefix=/usr/local/libevent-2.0.20-stable/
make
make install
cd ../
```

OK,继续编译扩展

```php
$ cd libevent-0.0.5
$ /usr/local/php/bin/phpize
$ ./configure --with-php-config=/usr/local/php/bin/php-config --with-libevent=/usr/local/libevent-2.0.20-stable
$ make && make install
```

顺利编译通过