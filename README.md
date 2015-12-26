# flask_blog

基于阿里云OSS为存储，采用`Flask`和`Tornado`以及`markdown`构建博客

首先在aliyun上创建一个OSS
然后创建两个目录，`blogs`用来存放博客，`topics`用来存放page页面。

然后在`/blog/settings.py`配置OSS

	OSS_ENDPOINT = "oss-cn-beijing-internal.aliyuncs.com"
	OSS_KEY = ""
	OSS_SECRET = ""
	OSS_BUCKET = ""
	
这样就不用数据库或者其他存储了。

然后配置Redis

	REDIS_HOST = '127.0.0.1'
	REDIS_PORT = 6000
	
博客业务使用Flask编写，请求处理使用的`Tornado`。端口默认为：8080

启动：

	python PATH/server.py --port=8080

博客文章示例：

见：<https://raw.githubusercontent.com/assad2012/flask_blog/master/awesome-php.md>

Nginx配置：

	log_format  blogaccess  '$remote_addr - $remote_user [$time_local] "$request" '
				 '$status $body_bytes_sent "$http_referer" '
				 '"$http_user_agent" $http_x_forwarded_for';
				 
	upstream blogserver
		{
			server 127.0.0.1:8080;
		}
		
	server
		{
			listen       80;
			server_name yourdomain.com;
			index index.html index.htm;
			
			location ^~ /static/ {
				root PATH/app/;
			}
			
			location / {
				proxy_read_timeout 1800;
				proxy_pass_header Server;
				proxy_set_header Host $host;
				proxy_redirect off;
				proxy_set_header X-Real-IP $remote_addr;
				proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
				proxy_set_header X-Scheme $scheme;
				proxy_pass http://blogserver;
			}

			location ~ .*\.(gif|jpg|jpeg|png|bmp|swf)$
			{
				expires      30d;
			}

			location ~ .*\.(js|css)?$
			{
				expires      12h;
			}
			access_log  blogaccess.log  blogaccess;
		}



