---
Title:   Linux用户需要了解的命令行技能
Summary: 下面介绍的都是一些命令行工具，这些工具在几位回答者的日常工作中都很有用。对于任何不了解的命令，请使用“man <COMMANDNAME>“查看，或者使用Google。有些命令需要先用 yum, apt-get install 命令安装。
Authors: Django Wong
Date:    2014-09-16
---

## 基本命令

#### 了解基本的bash

通读整个bash man page.

####  学习VIM

在Linux系统上，虽然你有Emacs和Eclipse，但是VIM仍然是无出其右的利器。

#### 了解SSH，基本的无密码验证方式。

例如通过ssh-agent, ssh-add等。 《灵犀志趣》平时都使用如下脚本完成无密码验证，省事省力。  
执行方式 sh nopasswd USER REMOTE_HOST  
执行此脚本前，请确认：   

- 本机上已有 id_dsa.pub ,若无。 使用命令 ssh-keygen -t dsa 获得  
- 远程机上登录用户家目录下，已经有 .ssh 文件夹，若无创建之。  

	$ cat  nopasswd 
	#!/bin/sh

	scp ~/.ssh/id_dsa.pub  $1@$2:~/
	ssh $1@$2 " touch ~/.ssh/authorized_keys ; cat ~/id_dsa.pub  >> ~/.ssh/authorized_keys; chmod 644 ~/.ssh/authorized_keys; exit"
	
#### 熟悉Bash中常用的任务管理命令

	&,Ctrl-Z,Ctrl-C,jobs,fg,bg,kill 等。
	
#### 基本的文件管理命令

	ls, ls-l, less, head, tail, tail -f, ln, ln -s, chmod, chown, du, du -sk *, df, mount
	
#### 基本的网络管理命令

	ipconfig, ifconfig, dig
	
#### 熟悉正则表达式，以及 grep，egrep用到的选项

	-o, -A, -B
	
#### 软件安装命令了解

	apt-get 和 yum
	
	cat -n可以帮助显示行号。
	
## 一些表达式

- `!!` 再次执行上一条命令  
- `!$` 上一条命令的最后一个单词  
- `{a..b}` 按照从a到b顺序的一个数字列表  
- `{a,b,c}` 三个词a,b,c. 可以这样使用 touch /tmp/{foo,bar,baz}  
- `{$1-$9}` 执行shell脚本时的命令行参数  
- `$0` 正在执行的命令名称  
- `$#` 当前启动的命令中传入的参数个数  
- `$?` 上一条命令的执行返回值。  
- `$$` 该shell的进程号。  
- `$*` 从$1开始，启动该shell脚本的所有参数。  

## 日常使用命令

Ctrl-R

	在bash中， Ctrl-R用于在历史命令中搜索
	
Ctrl-W, Ctrl-U, Alt-BackSpace 

	bash中，Ctrl-W删除最后一个词，Ctrl-U删除最后一行, Alt-BackSpace 删除光标前的一个词 man readline 中包含了大量bash中的默认热键绑定.
	
cd -  

	返回前一个工作路径  

xargs  

	非常强大的命令。如果你还不确定是否能正确的执行任务，可以先用xargs echo查看。下面是一个用该功能的例子:
	
	find . -name \*.py | xargs grep some_function
	cat hosts | xargs -l {} ssh root@{} hostname
	
parallel

	一个更加强大的命令. 可以实现并行执行任务,并可以分割输入文件, 指定多个节点同时运行命令等功能.详细的功能可以参考这个链接.

pstree -p

	打印进程树的得力工具
	
pgrep,pkil

	使用名字查找进程，或者直接向指定名字的进程发送信号。

nohup，disown,screen, tmux

	当你需要将进程永远处在后台运行是，这两个命令很有用。

lsof, netstat -lntp

	查询当前什么进程在监听什么端口。

set

	在bash脚本中， 使用 set -x 获得debug输出，使用 set -e 获得错误输出。

;

分号用于开启一个子shell并运行至结束后关闭。 例如：
	
	#在当前路径下执行一些命令
	(cd /some/other/dir; other-command)
	# 工作路径仍然是当前目录
	

## 数据处理

sort,uniq, uniq -u, uniq -d
了解这些排序命令

cut,paste, join   
了解这些文本文件的维护工具。很多人都在使用cut后，忘记join


使用sort/uniq进行集合的交、并、补运算=  
假设a和b是两个文本文件，其中的行都是唯一的。   

如下几个命令可以快速的实现一些集合操作。


	cat a b | sort | uniq > c   # c is a union b
	cat a b | sort | uniq -d > c   # c is a intersect b
	cat a b b | sort | uniq -u > c   # c is set difference a - b
	
awk,sed

这两个工具能实现复杂的数据替换和修改  
例如，下面的命令实现对文本文件中低三列的数据求总和。  
使用shell完成此运算比用Python快3倍

	awk '{ x += $3 } END { print x }'
	
制表符的输入

	在bash的命令行中，如若需要输入制表符，可以使用 Ctrl-V <tab> 或者 $’\t’ 实现
	
strings,grep

	可以帮助在二进制文件中寻找文本。
	
iconv,uconv

	可以帮助转换文本编码
	
split,csplit

	分别可以实现将文件按照大小分割，以及按照特定的模式分割。
	
## 系统调试


iostat,netstat,top,atop,htop,dstat

	可以帮助了解硬盘，CPU，内存，网络的状态。这能帮你对系统正在发生的情况有个第一认识。

free,vmstat

	如果想了解内存的状态，这两个命令很重要。其中cached是Linux内核中文件缓存的大小。
	
kill -3 <pid>

	在调试Java程序时，使用此命令，可以在stderr/logs中找到完整的stack trace，堆信息(包含垃圾收集的细节).
	
mtr,traceroute

	能够帮忙找到网络问题，前者比traceroute更好用。

iftop,nethogs

	这两个命令可以办刚找出哪个端口或者进程占用了多少网络带宽。

ab,siege

	这个Apache自带的工具能帮助快速检查web服务器的性能。

wireshark,tshark


	是进行更高级的网络调试的得力工具。

strace,ltrace

	这两个命令能帮你在一无所知的情况下，对程序运行失败，假死，崩溃等问题带来一些线索。另外，他们还能帮忙发现一些性能问题。比如 -c选项可以做profiling；-p选项可以挂到某个指定的进程上。
	
ldd

	检查共享库的情况

gdb

	了解如何利用GDB连接到一个正在运行的进程，并且得到其stack trace。

/proc/

	在做现场调试的时候很有用。比如 /proc/cpuinfo, /proc/XXX/cwd, /proc/XXX/exe, /proc/XXX/fd/, /proc/XXX/smaps

sar

	需要判断为何过去某个时间系统会出错时，这个命令能显示CPU，内存和网络的历史情况。

stap, perf

	当需要更深的分析系统，以及性能情况时，这两个工具很有用。

dmesg

	当系统出现一些很反常的现象时，比如可能是硬件或驱动问题时，这个很管用。

	