---
Authors: Django Wong
Date: 2020-03-23
Summary: composer是PHP中用来管理依赖(dependency)关系的工具。官方的镜像在国内使用起来很慢，特别整理了国内的一些著名的composer镜像站点。
Title: 国内可用的composer镜像
seo_description: Composer是PHP的依赖管理工具，但官方镜像在国内访问缓慢。本文整理了国内可用的Composer镜像站点，包括腾讯云、阿里云、华为云、上海交通大学和Packagist中国全量镜像，提供详细设置方法，帮助PHP开发者加速依赖安装，提升开发效率。
seo_keywords: Composer镜像, PHP依赖管理, 国内镜像站点, 腾讯云, 阿里云
---

## Composer简介

Composer 是 PHP5以上 的一个依赖管理工具。它允许你申明项目所依赖的代码库，它会在你的项目中为你安装他们。Composer 不是一个包管理器。是的，它涉及 "packages" 和 "libraries"，但它在每个项目的基础上进行管理，在你项目的某个目录中（例如 vendor）进行安装。默认情况下它不会在全局安装任何东西。因此，这仅仅是一个依赖管理。

## Composer的安装

```php
curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer
```

或者：

```php
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
php composer-setup.php --install-dir=/usr/local/bin --filename=composer
```

然后执行：

```php
#composer -V
#Composer version 1.9.0
```

这样就说明Composer安装成功。

关于Compsoer的其他，请查看 <https://getcomposer.org/doc/>

## 镜像站点

### 腾讯云镜像

访问：<https://mirrors.cloud.tencent.com/composer/>

设置：

```php
composer config -g repos.packagist composer https://mirrors.cloud.tencent.com/composer/
```

### 阿里云镜像

访问： <https://developer.aliyun.com/composer>

设置：

```php
composer config -g repo.packagist composer https://mirrors.aliyun.com/composer/
```

### 华为云镜像

访问： <https://mirrors.huaweicloud.com/repository/php/>

设置：

```php
composer config -g repo.packagist composer https://mirrors.huaweicloud.com/repository/php/
```

### 上海交通大学镜像

访问： <https://packagist.mirrors.sjtug.sjtu.edu.cn/>

设置：

```php
composer config -g repos.packagist composer https://packagist.mirrors.sjtug.sjtu.edu.cn
```

### Packagist 中国全量镜像

访问： <https://php.cnpkg.org/> 

设置：

```php
composer config -g repos.packagist composer https://php.cnpkg.org
```