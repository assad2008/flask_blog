---
Title:   SVN提交代码自动同步到测试环境
Summary: 只想给自己做个记录，以备查询，网上查了一堆。也遇到些问题，搞得丈二和尚摸不着头脑。
Authors: Django Wong
Date:    2014-11-19
---

首先启动SVN服务

	svnserve -d --listen-port 9999 -r /opt/svn (以root用户在运行)
	
测试SVN服务

	[root@analysis wjtest]# svn checkout svn://192.168.1.xxx:9999 /var/www/wjtest/
	Authentication realm: <svn://192.168.1.xxx:9999> /var/svn/wjtest
	Password for 'root': 
	Authentication realm: <svn://192.168.1.xxx:9999> /var/svn/wjtest
	Username: username
	Password for 'password': 
	
提示

	-----------------------------------------------------------------------
	ATTENTION!  Your password for authentication realm:

	   <svn://192.168.1.xxx:9999> /var/svn/wjtest

	can only be stored to disk unencrypted!  You are advised to configure
	your system so that Subversion can store passwords encrypted, if
	possible.  See the documentation for details.

	You can avoid future appearances of this warning by setting the value
	of the 'store-plaintext-passwords' option to either 'yes' or 'no' in
	'/root/.subversion/servers'.
	-----------------------------------------------------------------------
	Store password unencrypted (yes/no)? yes
	A    /var/www/wjtest/index.php
	
SVN服务应该没什么问题了

配置Hooks post-commit，实现自动同步svn版本库文件到web目录

为了可以在修改完代码提交到SVN服务器后,WEB服务器直接同步.需要配置SVN的钩子,打开hooks目录,
可以看到有一个post-commit.tmpl文件,这是一个模板文件,
复制一份放在此目录下,命名为post-commit，并将其用户组设为www,并设置为可执行：

chown www:www post-commit
chmod +x post-commit这样就有了访问www目录的权限。
里面原有的代码全部注释掉.这里可以执行shell命令,每次commit完成后都会调用此文件.
*post-commit*必须为可执行的

文件内容为:

	export LANG=zh_CN.UTF-8
	REPOS="$1"
	REV="$2"
	SVN_PATH=/usr/bin/svn
	WEB_PATH=/web/project
	LOG_PATH=/tmp/svn_update.log
	#/usr/bin/svn update --username user --password password $WEB_PATH --no-auth-cache
	echo "nnn##########开始提交 " `date "+%Y-%m-%d %H:%M:%S"` '##################' >> $LOG_PATH
	echo `whoami`,$REPOS,$REV >> $LOG_PATH
	$SVN_PATH update --username user --password password $WEB_PATH --no-auth-cache >> $LOG_PATH
	chown -R www:www $WEB_PATH
	
说明:

1. #!/bin/sh 说明是执行shell命令  
2. export LANG=zh_CN.UTF-8 是为了解决svn post commit 中文乱码。如果你是GBK编码可能会提示：Error output could not be translated from the native locale to UTF-8。这是客户端和服务器编码的问题，默认是utf-8,可尝试设置export LANG=zh_CN.GBK或者export LANG=en_US.UTF-8  
#执行更新操作
3. svn update –username 你版本库的用户名 –password 用户名的密码 svn://你的IP地址:端口/repos/project /web/project  
4. chown -R www:www $WEB_PATH 更改文件夹属主为适合Web Server的  

这里可以执行shell命令,每次commit完成后都会调用此文件。

---

shell脚本来自：<http://blog.rekfan.com/articles/310.html>