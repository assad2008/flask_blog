---
Title:   用python以及Inotify监控文件
Summary: 用python以及Inotify监控文件
Authors: Django Wong
Date:    2013-11-27
---

Inotify地址：[访问](https://github.com/seb-m/pyinotify)

	# -*- coding:utf-8 -*-

	import os
	import pyinotify
	from functions import *

	WATCH_PATH = '' #监控目录

	if not WATCH_PATH:
		wlog('Error',"The WATCH_PATH setting MUST be set.")
		sys.exit()
	else:
		if os.path.exists(WATCH_PATH):
			wlog('Watch status','Found watch path: path=%s.' % (WATCH_PATH))
		else:
			wlog('Error','The watch path NOT exists, watching stop now: path=%s.' % (WATCH_PATH))
			sys.exit()
		   
	class OnIOHandler(pyinotify.ProcessEvent):
		def process_IN_CREATE(self, event):
			wlog('Action',"create file: %s " % os.path.join(event.path,event.name))
			
		def process_IN_DELETE(self, event):
			wlog('Action',"delete file: %s " % os.path.join(event.path,event.name))
			
		def process_IN_MODIFY(self, event):
			wlog('Action',"modify file: %s " % os.path.join(event.path,event.name))
			
	def auto_compile(path = '.'):
		wm = pyinotify.WatchManager()
		mask = pyinotify.IN_CREATE | pyinotify.IN_DELETE | pyinotify.IN_MODIFY
		notifier = pyinotify.ThreadedNotifier(wm, OnIOHandler())
		notifier.start()
		wm.add_watch(path, mask,rec = True,auto_add = True)
		wlog('Start Watch','Start monitoring %s' % path)
		while True:
			try:
				notifier.process_events()
				if notifier.check_events():
					notifier.read_events()
			except KeyboardInterrupt:
				notifier.stop()
				break

	if __name__ == "__main__":
		 auto_compile(WATCH_PATH)