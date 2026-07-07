---
Authors: Django Wong
Date: 2013-11-30
Summary: python安装cx_Oracle(RPM)
Title: python安装cx_Oracle(RPM)
seo_description: 本文详细介绍了在Linux系统下通过RPM包安装Python cx_Oracle模块的完整步骤，包括下载安装包、执行rpm命令、解决libclntsh.so.10.1库文件缺失问题，以及配置ld.so.conf和ldconfig。最后提供Python连接Oracle数据库的示例代码，帮助开发者快速实现Python与Oracle的集成。
seo_keywords: Python安装cx_Oracle, cx_Oracle RPM安装, Python连接Oracle, libclntsh.so.10.1错误解决,
  Oracle数据库Python
---

cx-oracle官网  
<http://cx-oracle.sourceforge.net/>  
下载相应版本的cx-oracle安装包  
然后执行：  

```python
rpm -ivh cx_Oracle-5.1.2-10g-py26-1.x86_64.rpm
```

安装成功后，在python的`site-packages`目录可以看到cx_Oracle.so  
这样表示已安装成功  

然后import cx_Oracle  
却发现出现错误： 
 
```python
ImportError: libclntsh.so.10.1: cannot open shared object file: No such file or directory
```

显然，我们在安装的时候并未指定oralce的路径，导致无法找到libclntsh.so.10.1文件  
找到libclntsh.so.10.1文件的目录：/usr/lib/oracle/10.2.0.4/client64/lib/  
然后编辑/etc/ld.so.conf文件  
加入该目录  
然后执行ldconfig即可  
这样，我们发现已经能顺利import cx_Oralce了！  

使用示例：

```python
import cx_Oracle

connstr='user/pass@host/db'
odb = cx_Oracle.connect(connstr)
cursor = odb.cursor()
cursor.execute("select * from table")
print(cursor.fetchone())
```

具体说明见：<http://cx-oracle.sourceforge.net/html/index.html>