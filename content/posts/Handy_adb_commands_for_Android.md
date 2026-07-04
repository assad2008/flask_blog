---
Title:   一些有用的 Android adb 命令
Summary: 一些常用的 Android adb 命令
Authors: Django Wong
Date:    2014-01-23
---

下面是一些我找到Android的ADB有用的命令。可以手动或使用自动构建和测试过程。

### 查看设备

	adb devices
	
如果多个设备连接则使用 `use adb -s DEVICE_ID`连接到目标设备

### 安装应用

使用install命令安装一个apk包，如果应用已安装到了该设备，则使用`-r`重新安装和保持原来的应用数据

	adb install -r APK_FILE
	
	#example
	adb install -r com.feiliu.wjbd
	
### 卸载一个应用

	adb uninstall APK_FILE
	
	#example
	adb uninstall com.feiliu.wjbd
	
### 启动一个页面

	adb shell am start PACKAGE_NAME/ACTIVITY_IN_PACKAGE
	adb shell am start PACKAGE_NAME/FULLY_QUALIFIED_ACTIVITY

	# example
	adb shell am start -n com.feiliu.wjbd/.MainActivity
	adb shell am start -n com.feiliu.wjbd/com.feiliu.wjbd.MainActivity
	
### 进入设备的shell界面

	adb shell
	
### 截屏

[Sergei Shvetsov](https://plus.google.com/113036707377007500168/)想出了一个很好方法，获得一个屏幕截图且使用`shell screencap`通过perl输出到本地目录。具体查看[他的博客](http://blog.shvetsov.com/2013/02/grab-android-screenshot-to-computer-via.html)给出的解释

	adb shell screencap -p | perl -pe 's/\x0D\x0A/\x0A/g' > screen.png
	
### 解屏

这个命令会发送一个解屏事件到锁屏的设备上

	adb shell input keyevent 82
	
### 日志

命令行显示Log

	adb logcat
	
#### 根据tagname过滤

	adb logcat -s TAG_NAME
	adb logcat -s TAG_NAME_1 TAG_NAME_2

	#example
	adb logcat -s TEST
	adb logcat -s TEST MYAPP
	
#### 优先过滤

显示一个特定的优先级警告及以上的日志。

	adb logcat "*:PRIORITY"

	# example
	adb logcat "*:W"
	
优先级:

- V — 细则 (最低优先级)
- D — 调试
- I — 信息
- W — 警告
- E — 错误
- F — 致命
- S — 静默 (最高优先级，不会打印任何信息)

#### 使用grep过滤


这个很像在Linux上使用管道命令一样，需系统支持

	adb logcat | grep "SEARCH_TERM"
	adb logcat | grep "SEARCH_TERM_1\|SEARCH_TERM_2"

	#example
	adb logcat | grep "Exception"
	adb logcat | grep "Exception\|Error"

#### 清除日志块
	
使用来清除旧的日志

	adb logcat -c


- - - - - - -

继续阅读：[official adb reference site](http://developer.android.com/tools/help/adb.html)