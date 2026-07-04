---
Title: Ubuntu安装LNMP脚本出错解决
Summary: "在ubuntu电脑上安装lnmp环境，执行下面命令时sh ubuntu.sh，报错误：ubuntu.sh: 113: ubuntu.sh: Syntax error: \"(\" unexpected"
Authors: Django Wong
Date: 2015-02-12
---

Ubuntu版本：Ubuntu 14.04 LTS  
LNMP安装脚本：<http://lnmp.org/>

解压执行

	sudo sh ubuntu.sh
	
报错

	ubuntu.sh: 113: ubuntu.sh: Syntax error: "(" unexpected
	
原因

	兼容性问题，因为linux将sh默认指向了dash，而不是bash

解决办法

	sudo dpkg-reconfigure dash
	
在弹出的窗口选择no

然后就可以了
	
