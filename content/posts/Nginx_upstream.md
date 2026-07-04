---
Title:   Nginx upstream的几种分配方式
Summary: 1、轮询（默认）每个请求按时间顺序逐一分配到不同的后端服务器，如果后端服务器down掉，能自动剔除。2、weight指定轮询几率，weight和访问比率成正比，用于后端服务器性能不均的情况。
Authors: Django Wong
Date:    2013-11-27
---

## 轮询（默认）
每个请求按时间顺序逐一分配到不同的后端服务器，如果后端服务器down掉，能自动剔除。

## weight
指定轮询几率，weight和访问比率成正比，用于后端服务器性能不均的情况。
例如：

	upstream bakend {
	  server 192.168.1.10 weight=10;
	  server 192.168.1.11 weight=10;
	}

## ip_hash
每个请求按访问ip的hash结果分配，这样每个访客固定访问一个后端服务器，可以解决session的问题。
例如：

	upstream resinserver{
	  ip_hash;
	  server 192.168.1.10:8080;
	  server 192.168.1.11:8080;
	}
	
## fair（第三方）
按后端服务器的响应时间来分配请求，响应时间短的优先分配。

	upstream resinserver{
	  server server1;
	  server server2;
	  fair;
	}
## url_hash（第三方）
按访问url的hash结果来分配请求，使每个url定向到同一个后端服务器，后端服务器为缓存时比较有效。
例：在upstream中加入hash语句，server语句中不能写入weight等其他的参数，hash_method是使用的hash算法

	upstream resinserver{
	  server squid1:3128;
	  server squid2:3128;
	  hash $request_uri;
	  hash_method crc32;
	}

### 注意:

	upstream resinserver{  #定义负载均衡设备的Ip及设备状态
	  ip_hash;
	  server 127.0.0.1:8000 down;
	  server 127.0.0.1:8080 weight=2;
	  server 127.0.0.1:6801;
	  server 127.0.0.1:6802 backup;
	}
在需要使用负载均衡的server中增加
	proxy_pass http://resinserver/;

每个设备的状态设置为:

- `down` 表示单前的server暂时不参与负载
- `weight` 默认为1.weight越大，负载的权重就越大。
- max_fails ：允许请求失败的次数默认为1.当超过最大次数时，返回`proxy_next_upstream`模块定义的错误
- `fail_timeout:max_fails`次失败后，暂停的时间。
- `backup`:其它所有的非backup机器down或者忙的时候，请求backup机器。所以这台机器压力会最轻。

nginx支持同时设置多组的负载均衡，用来给不用的server来使用。
`client_body_in_file_only`设置为On 可以讲client post过来的数据记录到文件中用来做debug。
`client_body_temp_path`设置记录文件的目录 可以设置最多3层目录。
`location`对URL进行匹配.可以进行重定向或者进行新的代理 负载均衡。

本文出自"王伟" 博客，请务必保留此出处[http://wangwei007.blog.51cto.com/68019/1103727](http://wangwei007.blog.51cto.com/68019/1103727)