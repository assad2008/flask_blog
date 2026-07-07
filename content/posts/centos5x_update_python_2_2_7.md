---
Authors: Django Wong
Date: 2013-11-28
Summary: centos5.x升级python至python2.7
Title: centos5.x升级python至python2.7
seo_description: 本文详细介绍了在CentOS 5.x系统上将Python升级至Python 2.7的完整步骤，包括下载编译安装Python 2.7.3、备份旧版本并创建软链接、修复yum工具兼容性以及安装easy_install包管理器。适合需要在老系统上使用新版Python的开发者参考。
seo_keywords: CentOS 5.x升级Python, Python 2.7安装教程, yum兼容性修复, easy_install安装
---

### 首先到官网下载python2.7.3版本，编译安装

```python
$wget http://www.python.org/ftp/python/2.7.3/Python-2.7.3.tgz
$tar zxvf Python-2.7.3.tgz
$cd Python-2.7.3
$./configure
$make && make install
```

### 然后备份原来的python，并把python2.7做软连接到新的位置

```python
$mv /usr/bin/python /usr/bin/python.bak
$ln -s /usr/local/bin/python2.7 /usr/bin/python
$python -V

版本提示为2.7.3
```

### 更改yum,使其能正常运行

```python
$vim vim /usr/bin/yum
```

把#/usr/bin/python改成#/usr/bin/python2.4
这样yum可以正常运行了

### 安装easy_install

```python
$yum install python-setuptools
```

然后安装python-setuptools
到pypi网站下载python-setuptools,版本要和yum的时候版本一致，不然运行的时候会出现:

```python
$ easy_install rsa
Traceback (most recent call last):
  File "/usr/bin/easy_install", line 5, in <module>
	from pkg_resources import load_entry_point
ImportError: No module named pkg_resources
```

然后：

```python
$wget http://pypi.python.org/packages/source/s/setuptools/setuptools-0.6c5.tar.gz
$tar zxvf setuptools-0.6c5.tar.gz
$cd setuptools-0.6c5
$python setup.py install
```

安装成功
这样就可以方便的使用easy_install来安装python的库了