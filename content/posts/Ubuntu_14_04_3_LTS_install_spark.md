---
Authors: Django Wong
Date: 2015-10-15
Summary: 准备学习使用spark，主要用来分析日志文件，借此来学习一下大数据分析技术的一些入门知识。本文是基于Ubuntu 14.04服务器版本完成的。
Title: Ubuntu 14.04.3 LTS下安装Spark环境
seo_description: 本文详细介绍了在Ubuntu 14.04.3 LTS服务器版本下安装Spark环境的完整步骤，包括Java、Scala和Spark的下载、配置与启动。适合大数据分析初学者，通过日志分析案例学习Spark入门技术。
seo_keywords: Ubuntu 14.04安装Spark, Spark环境配置, 大数据分析入门, Scala安装, Java安装
---

### 安装java

```bash
$apt-get install default-jre
$apt-get install default-jdk
```

### 安装Scala

下载地址： <http://www.scala-lang.org/>

```bash
$mkdir /usr/loca/scala
$cd /usr/loca/scala
$wget http://downloads.typesafe.com/scala/2.11.7/scala-2.11.7.tgz
$tar zxvf scala-2.11.7.tgz
$cd scala-2.11.7
$mv * ../
$cd -
```

在 /etc/profile中添加

```bash
$export PATH=/usr/loca/scala/bin:$PATH
```

重启电脑，使/etc/profile永久生效

### 测试scala是否安装成功

```bash
$scala -version
$Scala code runner version 2.11.7 -- Copyright 2002-2013, LAMP/EPFL
```

### 下载Spark

下载地址：<http://spark.apache.org/downloads.html>

选择Spark版本

![](/static/attach/chose_spark.png)

```bash
$mkdir /usr/loca/spark
$cd /usr/loca/spark
$wget http://apache.fayea.com/spark/spark-1.5.1/spark-1.5.1-bin-hadoop2.6.tgz
$cd spark-1.5.1-bin-hadoop2.6
$mv * ../
$cd -
```

### 启动Spark

![](/static/attach/start_spark.png)

启动成功

### 启动Pyspark

![](/static/attach/start_pyspark.png)

启动成功