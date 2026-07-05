---
Title: 如何安装PHP7.2
Summary: PHP 7.2经过很长时间的开发，官方终于释出了正式版，带来了一些很大的变化，和安全改进。
Authors: Django Wong
Date:    2017-12-08
---

### 下载：

<http://www.php.net/downloads>


### Changelogs

<http://php.net/ChangeLog-7.php#7.2.0>


[PHP 7.2已经发布](https://secure.php.net/releases/7_2_0.php)，带来一些大的新功能和安全增强功能语言，比如object类型提示，更加理智count()的行为，以及[更多](https://secure.php.net/manual/en/migration72.php)。

下面介绍PHP 7.2在各个操作系统上的安装简单指南。


## Ubuntu 14.04, 16.04 17.04和17.10

可以使用[Ondřej Surý](https://launchpad.net/~ondrej/+archive/ubuntu/php)的PPA安装PHP 7.2：

```php
sudo add-apt-repository ppa:ondrej/php
sudo apt-get update
sudo apt-get install php7.2-cli
```

[在这里查看可用软件包的完整列表](https://launchpad.net/~ondrej/+archive/ubuntu/php/+packages?field.name_filter=php7.2&field.status_filter=published)

## Debian 8（Jessie）和9（Stretch）

`Ondřej Surý`还为`Debian`提供[PHP 7.2软件包](https://packages.sury.org/php/)，可以使用这些命令进行安装：

```php
sudo apt-get install apt-transport-https lsb-release ca-certificates
sudo wget -O /etc/apt/trusted.gpg.d/php.gpg https://packages.sury.org/php/apt.gpg
echo "deb https://packages.sury.org/php/ $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/php.list
sudo apt-get update
sudo apt-get install php7.2-cli
```

## Debian 7（Wheezy）

可以按照以下说明的指示从源代码编译PHP 7.2：在[Debian Wheezy上安装PHP 7](https://github.com/drj-io/php7-debian-build)。git checkout在克隆php-src版本库之后，确保你有相应的标签。


## CentOS / RHEL 6+和Fedora 25+

`Remi Collet`是PHP 7.2的发布经理之一，他也为这个新版本发布了RPM软件包。您可以使用[配置向导](https://rpms.remirepo.net/wizard/)确定准确的设置步骤，或者参阅[Remi的网站](https://blog.remirepo.net/post/2017/11/30/PHP-version-7.2.0-is-released)以获取关于7.2.0版本的更多详细信息。


## Mac OS X

PHP 7.2可以通过[Liip的php-osx](https://php-osx.liip.ch/)工具轻松安装：

```php
curl -s https://php-osx.liip.ch/install.sh | bash -s 7.2
```

或者，如果你更喜欢使用brew软件：

```php
brew tap homebrew/homebrew-php
brew install php72
```

## Windows平台

Windows的PHP 7.2发行版可以在[windows.php.net](http://windows.php.net/)网站上找到：[http//windows.php.net/download#php-7.2](http://windows.php.net/download#php-7.2)

您可以在这里找到安装发行版的说明：[https://www.webtechgadgetry.com/install-php-7-windows/](https://www.webtechgadgetry.com/install-php-7-windows/)

## phpbrew

[phpbrew](https://github.com/phpbrew/phpbrew)是一个非常好的工具，可以帮助您下​​载，编译和管理多个版本的PHP。假设您已经按照[安装说明](https://github.com/phpbrew/phpbrew#requirement)进行了[安装](https://github.com/phpbrew/phpbrew#requirement)，并启动了phpbrew，PHP 7.2.0可以安装两个简单的命令：

```php
phpbrew update
phpbrew install -j $(nproc) 7.2.0 +default
```

##

转自：<https://www.colinodell.com/blog/201711/installing-php-72>

