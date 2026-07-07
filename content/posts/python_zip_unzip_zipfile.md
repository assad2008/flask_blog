---
Authors: Django Wong
Date: 2013-11-28
Summary: zip文件是我们经常使用的打包格式之一，python解压和压缩zip效率非凡。
Title: Python解压和压缩zip
seo_description: 学习如何使用Python解压和压缩zip文件，提高文件处理效率。本文提供详细的Python代码示例，演示通过zipfile模块轻松实现zip文件的解压与文件夹压缩，适合Python开发者参考。
seo_keywords: Python解压zip, Python压缩zip, zipfile模块, Python文件处理
---

zip文件是我们经常使用的打包格式之一，python解压和压缩zip效率非凡。
python解压zip文档：

```python
#/usr/bin/python
#coding=utf-8

import os,sys,time
import zipfile

filename = 'callofdutyblackopszombies_1349649132343_my.zip'  #要解压的文件
filedir = 'data/'  #解压后放入的目录
r = zipfile.is_zipfile(filename)
if r:
	starttime = time.time()
	fz = zipfile.ZipFile(filename,'r')
	for file in fz.namelist():
		print(file)  #打印zip归档中目录
		fz.extract(file,filedir)
	endtime = time.time()
	times = endtime - starttime
else:
	print('This file is not zip file')
print('times' + str(times))
```

python压缩文件夹为zip

```python
#/usr/bin/python
#coding=utf-8


import os
import zipfile
import sys

try:
	import zlib
	compression = zipfile.ZIP_DEFLATED
except:
	compression = zipfile.ZIP_STORED

path = 'data/'  #要进行压缩的文档目录
start = path.rfind(os.sep) + 1
filename = 'callofdutyblackopszombies_1349649132343_my.zip'  #压缩后的文件名

z = zipfile.ZipFile(filename,mode = "w",compression = compression)
try:
	for dirpath,dirs,files in os.walk(path):
		for file in files:
			if file == filename or file == "zip.py":
				continue
			print(file)
			z_path = os.path.join(dirpath,file)
			z.write(z_path,z_path[start:])
	z.close()
except:
	if z:
		z.close()
```