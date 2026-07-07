---
Authors: Django Wong
Date: 2013-11-27
Summary: Linux排错无碍乎，负载、内存、CPU、IO等，现梳理一下，以备忘！
Title: Linux排错无碍乎，负载、内存、CPU、IO等
seo_description: 本文详细介绍了Linux系统排错的常见方法，涵盖负载、内存、CPU、IO等核心性能问题的诊断技巧。从现象分析、非法登录检查、误操作排查，到进程查看、网络服务监控、硬件故障检测，再到IO性能优化和系统日志分析，全面梳理了Linux运维中的关键排错步骤。适合系统管理员和运维人员参考，帮助快速定位和解决服务器性能瓶颈。
seo_keywords: Linux排错, 系统性能, CPU负载, IO性能, 内存管理
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

```bash
#pstree -a 
#ps aux
```

### 网络服务
	#netstat -antup 

### CPU和内存
还有空闲的内存吗？服务器在内存和磁盘之间swap?

```bash
#free -m
#uptime
#top
```

### 硬件罢工了？

```bash
#lspci
#dmidecode
#ethtool
```

### IO性能，这个很重要

IO使用率

```bash
#iostat -kx 2
# vmstat 2 10
```

CPU占用，系统进程？用户进程？

```bash
#mpstat 2 10
```

查看占用IO的罪魁祸首

```bash
#dstat -cdlmnpsy
```

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