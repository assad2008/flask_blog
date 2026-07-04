---
Title:   实践Nginx+Lua+Redis高性能方案
Summary: 为了寻找一个高性能的Web处理方案，尝试过PHP，Python，PyPy，但是效果还是不怎么好，终于瞄上了Lua
Authors: Django Wong
Date:    2015-06-25
---

- Nginx，选择淘宝的[Tengine](http://tengine.taobao.org/)
- Lua，最好使用LuaJIT，这样，效率会更高。

因为Tengine本身支持Lua模块，在编译的时候选择Lua模块即可。

首先安装LuaJIT

	apt-get install libluajit-5.1-common
	apt-get install libluajit-5.1-dev
	
开始编译Tengine

	./configure --user=www --group=www --prefix=/usr/local/nginx --with-http_stub_status_module --with-http_ssl_module --with-http_gzip_static_module --with-ipv6 --with-http_lua_module --with-luajit-lib=/usr/lib/x86_64-linux-gnu/ --with-luajit-inc=/usr/include/luajit-2.0/ --add-module=/data0/soft/ngx_devel_kit-0.2.19 --add-module=/data0/soft/echo-nginx-module-0.58
	make
	make install

在编译选项中，

	--with-http_lua_module --with-luajit-lib=/usr/lib/x86_64-linux-gnu/ --with-luajit-inc=/usr/include/luajit-2.0/ --add-module=/data0/soft/ngx_devel_kit-0.2.19

指定了`LuaJIT`的 Lib和include路径，顺便我把ngx\_devel\_kit也编译进去了。

重新启动Nginx

	/etc/init.d/nginx restart
	
写一个简单的Lua脚本，在Nginx里。

	server
		{
			listen 80 default_server;
			index index.html index.htm index.php;
			root  /home/www/default;
			
			location /testlua
			{
				default_type text/plain;
				content_by_lua 'ngx.say("i am lua")';
			}
			
			access_log  /home/wwwlogs/access.log  access;
		}
	
进行ab测试

	ab -n 1000000 -c10000 http://192.168.31.181/luatest

QPS达到4W多啊，很牛啊

![](/static/attach/qps4w.png)

开始编写一个Lua脚本，redislua.lua，来进行简单的Redis操作，来测试性能。

	local redis = require("redis")
	local cache = redis.new()

	local ok, err = cache.connect(cache, '127.0.0.1', '6000')
	if not ok then
		ngx.say("failed to connect redis:", err)
		return
	end

	cache:set_timeout(3000)

	res, err = cache:set("key1", "nginx test lua")

	if not ok then
		ngx.say("failed to set key1: ", err)
		return
	end

	ngx.say("set result: ", res)

	local res, err = cache:get("key1")
	 
	if not res then
		ngx.say("failed to get key1: ", err)
		return
	end
	  
	if res == ngx.null then
		ngx.say("key1 not found.")
		return
	end 
	  
	ngx.say("key1: ", res)

	local ok, err = cache:close()
	  
	if not ok then
		ngx.say("failed to close redis:", err)
		return
	end 

Lua Redis使用的：<https://github.com/agentzh/lua-resty-redis.git>

重写 Nginx配置文件：

	server
		{
			listen 80 default_server;
			index index.html index.htm index.php;
			root  /home/www/default;

			#error_page   404   /404.html;

			location /lr
			{
				default_type text/plain;
				content_by_lua_file /data0/luaproject/redislua.lua;	
			}
			
			location /echo
			{
				default_type text/plain;
				echo 'hello world';
			}
			access_log  /home/wwwlogs/access.log  access;
		}
	
然后在http里写上lua项目地址：

	lua_package_path "/data0/luaproject/?.lua;;"; 
	
重启Nginx

再进行ab测试

QPS依然达到1W多啊，性能依然强筋的很！

![](/static/attach/qps1w.png)
