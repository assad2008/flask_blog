---
Title:   Python解压和压缩zip
Summary: zip文件是我们经常使用的打包格式之一，python解压和压缩zip效率非凡。
Authors: Django Wong
Date:    2013-11-28
---

zip文件是我们经常使用的打包格式之一，python解压和压缩zip效率非凡。
python解压zip文档：

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
	
python压缩文件夹为zip

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