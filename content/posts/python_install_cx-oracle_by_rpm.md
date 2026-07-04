---
Title:   python安装cx_Oracle(RPM)
Summary: python安装cx_Oracle(RPM)
Authors: Django Wong
Date:    2013-11-30
---

cx-oracle官网  
<http://cx-oracle.sourceforge.net/>  
下载相应版本的cx-oracle安装包  
然后执行：  

	rpm -ivh cx_Oracle-5.1.2-10g-py26-1.x86_64.rpm
	
安装成功后，在python的`site-packages`目录可以看到cx_Oracle.so  
这样表示已安装成功  

然后import cx_Oracle  
却发现出现错误： 
 
	ImportError: libclntsh.so.10.1: cannot open shared object file: No such file or directory

显然，我们在安装的时候并未指定oralce的路径，导致无法找到libclntsh.so.10.1文件  
找到libclntsh.so.10.1文件的目录：/usr/lib/oracle/10.2.0.4/client64/lib/  
然后编辑/etc/ld.so.conf文件  
加入该目录  
然后执行ldconfig即可  
这样，我们发现已经能顺利import cx_Oralce了！  

使用示例：

	import cx_Oracle

	connstr='user/pass@host/db'
	odb = cx_Oracle.connect(connstr)
	cursor = odb.cursor()
	cursor.execute("select * from table")
	print(cursor.fetchone())
	
具体说明见：<http://cx-oracle.sourceforge.net/html/index.html>