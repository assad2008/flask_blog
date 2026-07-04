---
Title:   一键安装docker-gitlab
Summary: Docker Gitlab 是提供 Gitlab 环境的 Docker 映像，可方便的在 Docker 容器中运行 Gitlab 系统。
Authors: Django Wong
Date:    2015-04-28
---

很强大啊，比起自己一个个安装，那真是简单多了。

## 首先安装docker  

见官方：<https://docs.docker.com/installation/>

很详细了，我就不多说了

## 一键命令  

	docker run --name='gitlab' -it -d -e 'GITLAB_PORT=10080' -e 'GITLAB_SSH_PORT=10022' -p 10022:22 -p 10080:80 -v /var/run/docker.sock:/run/docker.sock -v $(which docker):/bin/docker sameersbn/gitlab:latest
	
然后运行：

	docker ps -a
	
全部运行起来了

	CONTAINER ID        IMAGE                         COMMAND                CREATED              SMES
	dc22cedea691        sameersbn/redis:latest        "/start"               About a minute ago   Udis-gitlab        
	a11a08ab6db0        sameersbn/postgresql:latest   "/start"               About a minute ago   Ustgresql-gitlab   
	4eb41366c03f        sameersbn/gitlab:latest       "/app/init app:start   About a minute ago   Utlab  

等几分钟，访问：http://localhost:10080，熟悉的页面出来啦

默认账户密码：

	username: root
	password: 5iveL!fe
	
## 对硬件要求如下

### CPU

- 1 core 可支持 100 以内用户，但可能访问不顺畅
- 2 cores 推荐用于 100 用户
- 4 cores 可支持 1,000 用户
- 8 cores 可支持 10,000 用户

### Memory

- 512MB 内存太小，Gitlab 会很慢，而且你还得使用额外 250 兆的交换分区
- 768MB 是最低要求，但我们建议得再多点
- 1GB 可支持 100 用户，每个仓库不多于 250MB
- 2GB 推荐使用，支持 1000 用户
- 4GB 可支持 10000 用户

### 支持的浏览器

- Chrome (Latest stable version)
- Firefox (Latest released version)
- Safari 7+ (Know problem: required fields in html5 do not work)
- Opera (Latest released version)
- IE 10+
