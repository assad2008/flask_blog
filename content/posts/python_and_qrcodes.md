---
Title:   如何用Python生成QR二维码[双语]
Summary: Few days ago, I decided to try to generate QRCodes. 前几天，我有一些数据要生成QR码。
Authors: Django Wong
Date:    2014-01-15
---

Few days ago, I decided to try to generate QRCodes.  

前几天，我有一些数据要生成QR码。  

This article just shows a possibility using Python. 
 
本文提供了一种使用Python生成QR码的方法。  

## 工具

Googling for QRCodes generation I found some websites proposing to generate QRCodes for you.  

通过Google搜索“QRCodes generation”，我找到了一些在线生成QR码的网站

The ZXing Generator and the Kaywa Generator seem really powerful and complete, but I was looking for a way of integring QRCode-generation in an piece of software without requiring an Internet access.  

其中，ZXing Generator和Kaywa Generator的功能都很强大，但我想找的是一种无需网络就可以离线生成QR码的方法。  

A guy (MarkTraceur) commented my post on reddit, talking about a tool he built : QRustom ! Thanks to him !  

我把这个需求发布到了Reddit上，MarkTraceur在评论中提到来他创建的一个工具： QRustom ！非常感谢他提供了这个工具。  

With python, you can use pyqrcode but it works using a C/C++ encoder and a Java decoder...  

对于Python，你可以使用pyqrcode，但它的编码器是基于C/C++的，而解码器却是用Java写的。  

I also found the PyQRNative lib that seems to be a rewriting of this javascript generator (pretty sure great things can be done using this JS lib and Node.js).  

我也发现了PyQRNative库，这似乎是一个对javascript generator的重写 （非常肯定，使用这个JS库和Node.js可以做很多有趣的事 ）  

The code (that you can wget here) would need a serious rewriting to become PEP8 compliant and documented but it works (here's a QR containing URL for this post generated using PyQRNative).  

虽然它的代码（您可以使用wget 在 这里 下载）需要大量的改写才能兼容PEP8，但它的确工作（上图是一个使用PyQRNative生成的包含本文URL链接的的QR码）。

EDIT : After my post on reddit, Chris Beaven told me he did the rewriting. His version is available on Pypi. I've also rewritten this article using his lib.  

编辑：当我把文章发布到Reddit上后，Chris Beaven告诉我它重写了qrcode库。可以在PyPI 找到他的库。我也相应的改写了这篇文章。

Note that you'll have also to install the Python Imaging Library (PIL) in order to generate the images themselves. 
 
注意，为了生成图像，必须安装Python图像库 （PIL）


Just run:

运行：

	$ sudo pip install pil qrcode
	
使用方法:

	from qrcode import *
	 
	qr = QRCode(version=20, error_correction=ERROR_CORRECT_L)
	qr.add_data("http://blog.matael.org/")
	qr.make() # Generate the QRCode itself
	 
	# im contains a PIL.Image.Image object
	im = qr.make_image()
	 
	# To save it
	im.save("filename.png")
	
At line 3, we instanciate a new qrcode.QRCode object using two parameters.
This class has other parameters that we don't use here (box_size, border, etc...).  

在第3行中，我们使用两个参数实例化了一个新的qrcode.QRCode对象。这个类还有一些其他我们没有使用的参数（box_size，border等）。

The first one is the QR version, an integer between 0 and 40 which define the size of the barcode and the amount of data we'll be able to store.  

第一个参数是QR版本，介于0和40之间，定义了QR码的大小及能够存储数据量的大小（译者注：修正水平愈高， QR 码图形面积愈大）。

The second is the correction level (redundancy).As said on Wikipedia, you can choose between :  

第二个参数是修正水平（错误冗余）。正如维基百科所说，你可以选择以下几个参数：

	ERROR_CORRECT_L  
		7% of codewords can be restored  
		7%的字码可被修正  
	ERROR_CORRECT_M (default)  
		15% can be restored  
		15%的字码可被修正  
	ERROR_CORRECT_Q  
		25% can be restored  
		25%的字码可被修正  
	ERROR_CORRECT_H  
		30% can be restored  
		30%的字码可被修正  
	
It's this redundancy phenomenon that enables decoding even if the code is damaged.  

正是这种容错能力，使得即便被破坏的QR码依然可以解码。

## 版本自动推测

The qrcode module add the fit parameter to the QRCode.make() method. If fit is used and QRCode.version is set to None, qrcode will guess the right version.  

qrcode模块的QRCode.make()方法有一个缺省为False的fit参数。当fit设置为True，并且QRCode.version设置为None，qrcode会自动推测合适的版本。

## 更快的方法

This rewriting bring a short version for fast generation :  

上述代码有更简单的方法：

	import qrcode
	img = qrcode.make("your awesome data")
	
Chris, thank you for that great work !  

非常感谢Chris的伟大工作！

## 结论

QR Codes are an elegant way of share data between devices.  

QR码是一种优雅的在不同设备间共享数据的方式。

They can be used for a lot of applications, from product tracking inside a factory to blog post URL. 
 
它们可用于包括从工厂内部产品跟踪到博客文章URL在内的大量应用。

The redundancy phenomenon allow artistic use or deformation of QR Codes and things like that :  

QR码的容错能力允许美化图片、部分信息缺失以及诸如下图这样的修改：

![](/static/attach/qr_matael.png)

I really think that these codes are powerful.  

我真心觉得QR码很强大。

Note also that, using processing and QR Codes, you can do Augmented Reality.  

另外，使用processing和QR码可以实现增强现实（Augmented Reality）。

译注：本文原文见[python and qrcodes](http://blog.matael.org/writing/python-and-qrcodes/)

[feisky（盛大云·软件开发）](http://feisky.42qu.com/)

