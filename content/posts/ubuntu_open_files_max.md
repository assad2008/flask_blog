---
Title:   修改ubuntu系统的open files最大值
Summary: 本来是一个很简单事情，因为自己以前调优的时候修改，以前使用的CentOS，没注意研究，现在查了一下，作为备用。
Authors: Django Wong
Date:    2015-12-22
---

## 前言

本来是一个简单的事情，没想到弄了半天，还是没修改好。最后发现Ubuntu和CentOS似乎有一点点不一样。

首先修改：/etc/security/limits.conf，重启系统。发现依然是1024

再次修改：/etc/rc.local的末尾添加：`ulimit -SHn 65535`，重启系统，依然是1024，不起作用，郁闷。

查了半天，终于摆正姿势，Ubuntu下修改的步骤：


### 第一步：配置/etc/security/limits.conf

```bash
sudo vim /etc/security/limits.conf
```

文件尾追加  

```bash
* hard nofile 65535 
* soft nofile 65535
```

说明：

`limits.conf`文件实际是 Linux PAM（插入式认证模块，Pluggable Authentication Modules）中`pam_limits.so`的配置文件，而且只针对于单个会话。

limits.conf的格式如下：

```bash
username|@groupname type resource limit，
```

- username|@groupname：设置需要被限制的用户名，组名前面加@和用户名区别。也可以用通配符*来做所有用户的限制。  
- type：有 soft，hard 和 -，soft 指的是当前系统生效的设置值。hard 表明系统中所能设定的最大值。soft 的限制不能比har 限制高。用 - 就表明同时设置了 soft 和 hard 的值  
- resource，
	core - 限制内核文件的大小  
	date - 最大数据大小  
	fsize - 最大文件大小  
	memlock - 最大锁定内存地址空间  
	nofile - 打开文件的最大数目  
	rss - 最大持久设置大小  
	stack - 最大栈大小  
	cpu - 以分钟为单位的最多 CPU 时间  
	noproc - 进程的最大数目  
	as - 地址空间限制  
	maxlogins - 此用户允许登录的最大数目  
	
要使`limits.conf`文件配置生效，必须要确保`pam_limits.so`文件被加入到启动文件中。查看`/etc/pam.d/su`文件中有：
session required /lib/security/pam\_limits.so

### 第二步：/etc/pam.d/su或/etc/pam.d/common-session

在`/etc/pam.d/su`将`pam_limits.so`这一行注释去掉  重起系统，或者，`/etc/pam.d/common-session`加上以下一行`session required pam_limits.so`

我修改的是`/etc/pam.d/su`

### 第三步：配置/etc/profile

最后加上`ulimit -SHn 65535`

重启系统后。执行`ulimit -n`，发现已经是`65535`了




