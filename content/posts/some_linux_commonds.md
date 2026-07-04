---
Title:   一些关于linux的命令说明
Summary: 一些我们经常使用的命令，文中的每行为一条命令，文中有的命令可能在你的主机上敲不出来，因为它可能是在其他版本的linux中所使用的命令。
Authors: Django Wong
Date:    2014-01-22
---

## 如何查看系统类型

#### 系统是什么版本?

	cat /etc/issue
	cat /etc/*-release
	cat /etc/lsb-release
	cat /etc/redhat-release
	
#### 它的内核版本是什么？

	cat /proc/version  
	uname -a
	uname -mrs
	rpm -q kernel
	dmesg | grep Linux
	ls /boot | grep vmlinuz
	
#### 它的环境变量里有些什么？

	cat /etc/profile
	cat /etc/bashrc
	cat ~/.bash_profile
	cat ~/.bashrc
	cat ~/.bash_logout
	env
	set
	
## 应用与服务

#### 正在运行什么服务？什么样的服务具有什么用户权限？

	ps aux
	ps -ef
	top
	cat /etc/service
	
#### 哪些服务具有root的权限？

	ps aux | grep root
	ps -ef | grep root
	
#### 安装了哪些应用程序？他们是什么版本？哪些是当前正在运行的？

	ls -alh /usr/bin/
	ls -alh /sbin/
	dpkg -l
	rpm -qa
	ls -alh /var/cache/apt/archivesO
	ls -alh /var/cache/yum/
	
#### Service设置

	cat /etc/syslog.conf
	cat /etc/chttp.conf
	cat /etc/lighttpd.conf
	cat /etc/cups/cupsd.conf
	cat /etc/inetd.conf
	cat /etc/apache2/apache2.conf
	cat /etc/my.conf
	cat /etc/httpd/conf/httpd.conf
	cat /opt/lampp/etc/httpd.conf
	ls -aRl /etc/ | awk ‘$1 ~ /^.*r.*/
	
#### 主机上有哪些计划任务

	crontab -l
	ls -alh /var/spool/cron
	ls -al /etc/ | grep cron
	ls -al /etc/cron*
	cat /etc/cron*
	cat /etc/at.allow
	cat /etc/at.deny
	cat /etc/cron.allow
	cat /etc/cron.deny
	cat /etc/crontab
	cat /etc/anacrontab
	cat /var/spool/cron/crontabs/root
	
## 通信与网络

#### NIC(s)，系统有哪些？它是连接到哪一个网络？

	/sbin/ifconfig -a
	cat /etc/network/interfaces
	cat /etc/sysconfig/network
	
#### 网络配置设置是什么？网络中有什么样的服务器？DHCP服务器？DNS服务器？网关？

	cat /etc/resolv.conf
	cat /etc/sysconfig/network
	cat /etc/networks
	iptables -L
	hostname
	dnsdomainname
	
#### 其他用户主机与系统的通信？

	lsof -i
	lsof -i :80
	grep 80 /etc/services
	netstat -antup
	netstat -antpx
	netstat -tulpn
	chkconfig --list
	chkconfig --list | grep 3:on
	last
	w
	
#### 缓存？IP和/或MAC地址?

	arp -e
	route
	/sbin/route -nee
	
#### 数据包可能嗅探吗？可以看出什么？监听流量

	# tcpdump tcp dst [ip] [port] and tcp dst [ip] [port]
	tcpdump tcp dst 192.168.1.7 80 and tcp dst 10.2.2.222 21

## 信息和用户

#### 你是谁？哪个id登录？谁已经登录？还有谁在这里？谁可以做什么呢？

	id
	who
	w
	last
	cat /etc/passwd | cut -d:    # List of users
	grep -v -E "^#" /etc/passwd | awk -F: &#039;$3 == 0 { print $1}'   # List of super users
	awk -F: '($3 == "0") {print}&#039; /etc/passwd   # List of super users
	cat /etc/sudoers
	sudo -l
	
#### 用户做过什么？是否有任何密码呢？他们有没有编辑什么？

	cat ~/.bash_history
	cat ~/.nano_history
	cat ~/.atftp_history
	cat ~/.mysql_history
	cat ~/.php_history
	
#### 可以找到什么样的用户信息

	cat ~/.bashrc
	cat ~/.profile
	cat /var/mail/root
	cat /var/spool/mail/root


