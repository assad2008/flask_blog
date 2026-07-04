---
Title:   树莓派搭建LNMP环境
Summary: 树莓派运行LINUX系统，其低功耗的高效率的特点可以用来做很多的事情，今天就给大家写一个LNMP服务的安装教程。需要注意的是，如果你想用树莓派来架设一个高并发的站点，这显然是不可取的，虽然树莓派的配置可以用来支持LNMP的运行，但是如果超过一定的并发会导致树莓派瘫痪或死机。所以，在树莓派上开设的站点只能用于支撑普通的学习研究站点。在本教程中，也会教大家如何配置Nginx、Mysql服务，使之在树莓派上更好地运作。
Authors: Django Wong
Date:    2013-12-01
---

树莓派运行LINUX系统，其低功耗的高效率的特点可以用来做很多的事情，今天就给大家写一个LNMP服务的安装教程。需要注意的是，如果你想用树莓派来架设一个高并发的站点，这显然是不可取的，虽然树莓派的配置可以用来支持LNMP的运行，但是如果超过一定的并发会导致树莓派瘫痪或死机。所以，在树莓派上开设的站点只能用于支撑普通的学习研究站点。在本教程中，也会教大家如何配置Nginx、Mysql服务，使之在树莓派上更好地运作。

树莓派镜像下载：<http://www.raspberrypi.org/downloads>

首先更新一下系统  

	sudo apt-get update
	
接着输入如下命令安装mysql服务：

	sudo apt-get install mysql-serve
	
首次安装mysql的时候会提示输入密码，密码不要忘记就行了。  

默认安装mysql的配置是基于1G以上X86 CPU，512M内存给Mysql独占的，自编译版提供多种配置文档，对于rapsberry pi选择small.cnf就行了，我们对/etc/mysql/my.cnf进行一些修改也行。另外mysql 5.5开始默认使用Innodb数据库引擎，这是一种对分布式和高并发优化的格式，其实老版本的MYISAM引擎也足够用了，关闭Innodb引擎也能节省大概6-10M的内存占用。  

	[mysqld]
	 
	character-set-server=utf8 #使用utf-8避免乱码
	 
	bind-address = ip #固定ip，便于局域网访问
	 
	key_buffer = 16k
	max_allowed_packet = 1M
	thread_stack = 64K
	thread_cache_size = 4
	query_cache_limit = 1M
	 
	default-storage-engine = MYISAM #默认数据库引擎改为MYISAM
	loose-skip-innodb #关闭Innodb支持
	
重启mysql 
 
	sudo /etc/init.d/mysql restart
	
开始安装PHP  

	sudo apt-get install php5-fpm php5-cli php5-curl php5-gd php5-mcrypt php5-mysql php5-cgi 
	
开始安装Nginx  

	sudo apt-get install nginx
	
开始配置Nginx  

	worker_processes 1;
	 
	worker_connections 256;
	 
	gzip on;
	gzip_disable 'msie6';
	 
	gzip_vary on;
	gzip_proxied any;
	gzip_comp_level 6;
	gzip_buffers 16 8k;
	gzip_http_version 1.1;
	gzip_types text/plain text/css application/json application/x-javascript text/xml application/xml application/xml+rss text/javascript;
	
打开/etc/nginx/sites-available/default

	server {
		listen 80;
		server_name raspiweb.ch; 
		root /media/usb/www/; 
	 
		access_log	/var/log/nginx/localhost.access.log;
		#error_page	404 /404.html;
	 
		if (!-e $request_filename)
		{
			rewrite ^(.*)$ /index.php$1 last;
		}
	 
		location / { 
			index  index.html index.htm index.php default.html default.htm default.php; 
		} 
	 
		location ~* ^.+.(jpg|jpeg|gif|css|png|js|ico|xml)$ {
			access_log	off;
			expires	1d;
		}
	 
		location ~ .*.php(/.*)*$ {
			fastcgi_split_path_info ^(.+.php)(/.+)$;
			fastcgi_pass unix:/var/run/php5-fpm.sock;
			fastcgi_index index.php;
			include fastcgi_params;
		}
	}
	
完成之后重新加载服务  

	service nginx restart
	service php5-fpm restart
	service mysql restart
	
安装phpmyadmin  

	cd /web/wwwroot/
	wget http://downloads.sourceforge.net/project/phpmyadmin/phpMyAdmin/3.5.7/phpMyAdmin-3.5.7-all-languages.zip
	unzip  phpMyAdmin-3.5.7-all-languages.zip
	mv phpMyAdmin-3.5.7-all-languages phpmyadmin
	
这样在本地访问http://树莓派IP/phpmyadmin 就可以访问phpmyadmin了
