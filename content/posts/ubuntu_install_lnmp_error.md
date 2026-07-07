---
Authors: Django Wong
Date: 2015-02-12
Summary: '在ubuntu电脑上安装lnmp环境，执行下面命令时sh ubuntu.sh，报错误：ubuntu.sh: 113: ubuntu.sh: Syntax
  error: "(" unexpected'
Title: Ubuntu安装LNMP脚本出错解决
seo_description: 'Ubuntu安装LNMP脚本时遇到Syntax error: ''('' unexpected错误？本文详细解析了Ubuntu
  14.04 LTS下执行sh ubuntu.sh报错的常见原因，即sh默认指向dash而非bash导致的兼容性问题。提供通过dpkg-reconfigure dash命令切换为bash的完整解决步骤，帮助您快速修复LNMP环境安装错误，顺利部署服务器。'
seo_keywords: Ubuntu安装LNMP脚本错误, Syntax error unexpected, dash与bash兼容性, dpkg-reconfigure
  dash, LNMP环境安装
---

Ubuntu版本：Ubuntu 14.04 LTS  
LNMP安装脚本：<http://lnmp.org/>

解压执行

```bash
sudo sh ubuntu.sh
```

报错

```bash
ubuntu.sh: 113: ubuntu.sh: Syntax error: "(" unexpected
```

原因

```bash
兼容性问题，因为linux将sh默认指向了dash，而不是bash
```

解决办法

```bash
sudo dpkg-reconfigure dash
```

在弹出的窗口选择no

然后就可以了