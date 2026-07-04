---
Title:   Centos 6.4 64位版设置无线连接
Summary: 最近用台式机搞了个服务器，安装了最新的Centos6.4最新的64位版本。因为不想使用网线，因此买了一个PCI-E的无线网卡，使用无线连接。无线网卡型号为：腾达（TENDA）W311P 150M PCI无线网卡
Authors: Django Wong
Date:    2013-11-27
---

最近用台式机搞了个服务器，安装了最新的Centos 6.4最新的64位版本。因为不想使用网线，因此买了一个PCI-E的无线网卡，使用无线连接。
无线网卡型号为：腾达（TENDA）W311P 150M PCI无线网卡

开始认为可能在Linux下需要安装驱动才可以识别网卡，而腾达也提供了该网卡的Linux驱动。可是我编译了半天也没编译过去，很是郁闷。
最后查询资料，Centos 6.4支持该型号的网卡。能够直接激活使用。因为通过桌面安装系统，只要设置相应的账号和密码，就可以连接上无线。说明无需安装驱动。

因为我装的是服务器，因此是选择最小安装的。这样需要在命令行下设置无线网卡。

因为我的路由器使用的是WAP/WAP2方式。网上搜了一通，发现没一个能解决问题的。最后发现了一个`wpa_supplicant`工具，使用起来很方便。
首先：看是否安装了`wpa_supplicant`，如果没安装，则用yum install wpa_supplicant安装一下。
安装成功后，看看`NetworkManager`是否允许，如果允许，则关闭。/etc/init.d/NetworkManager stop
然后使用`wpa_supplicant`生成你的账户和密钥文件 wpa_passphrase ssid password，你会看到生成你的账户信息

	network={
		ssid="yeestation"
		#psk="xxxxxxx"
		psk=471b1b8078ce952e9c9ed70d19fa8b4fbca67673ee881c7806a9a7458a4f640d
	}

复制该文本到/etc/wpa_supplicant/wpa_supplicant.conf的尾部即可
然后启动 wpa_supplicant -iwlan0 -B -c /etc/wpa_supplicant/wpa_supplicant.conf
自动获取IP：dhclient wlan0

这时候，你会发现，你的无线已经连上了。

如果需要自动启动，则写个简单的BASH脚本即可
$vim wlan0.sh

	#!/bin/bash
	wpa_supplicant -iwlan0 -B -c /etc/wpa_supplicant/wpa_supplicant.conf
	dhclient wlan0

然后在/etc/rc.local中加上
sh PATH/wlan0.sh即可

这样，系统会在启动的时候，自动连上无线了