---
Title:   Linux排错无碍乎，负载、内存、CPU、IO等
Summary: Linux排错无碍乎，负载、内存、CPU、IO等，现梳理一下，以备忘！
Authors: Django Wong
Date:    2013-11-27
---

### 现象，这个很重要
何时发现？是否可重现？是否有规律？有无线上更新？影响范围？等，有了现象，才好着手

### 非法登录？两个命令
	#w
	#last

### 误操作?
	#history

### 查看运行的进程
可查看正在运行的进程和用户

	#pstree -a 
	#ps aux

### 网络服务
	#netstat -antup 

### CPU和内存
还有空闲的内存吗？服务器在内存和磁盘之间swap?

	#free -m
	#uptime
	#top

### 硬件罢工了？

	#lspci
	#dmidecode
	#ethtool

### IO性能，这个很重要

IO使用率

	#iostat -kx 2
	# vmstat 2 10
	
CPU占用，系统进程？用户进程？

	#mpstat 2 10
	
查看占用IO的罪魁祸首

	#dstat -cdlmnpsy

### 内核、中断、网络
	#ss 或者ss -s
	#sysctl
查看CPU负载是否均衡
	

### 系统日志和内核消息
	# dmesg 
	#less /var/log/messages
	#less /var/log/secure
	#less /var/log/auth

### crontab过于频繁？

### 应用日志
	apache|nginx|mysql|php-fpm等