---
Title: "[译]NGINX缓存使用官方指南"
Summary: 我们都知道，应用程序和网站一样，其性能关乎生存。但如何使你的应用程序或者网站性能更好，并没有一个明确的答案。代码质量和架构是其中的一个原因，但是在很多例子中我们看到，你可以通过关注一些十分基础的应用内容分发技术（basic application delivery techniques），来提高终端用户的体验。其中一个例子就是实现和调整应用栈（application stack）的缓存。这篇文章，通过几个例子来讲述如何使用NGINX缓存，此外，结尾处还列举了一些常见问题及解答。
Authors: Django Wong
Date: 2015-08-07
---

## 基础

一个web缓存坐落于客户端和“原始服务器（origin server）”中间，它保留了所有可见内容的拷贝。如果一个客户端请求的内容在缓存中存储，则可以直接在缓存中获得该内容而不需要与服务器通信。这样一来，由于web缓存距离客户端“更近”，就可以提高响应性能，并更有效率的使用应用服务器，因为服务器不用每次请求都进行页面生成工作。

在浏览器和应用服务器之间，存在多种“潜在”缓存，如：客户端浏览器缓存、中间缓存、内容分发网络（CDN）和服务器上的负载平衡和反向代理。缓存，仅在反向代理和负载均衡的层面，就对性能提高有很大的帮助。

举个例子说明，去年，我接手了一项任务，这项任务的内容是对一个加载缓慢的网站进行性能优化。首先引起我注意的事情是，这个网站差不多花费了超过1秒钟才生成了主页。经过一系列调试，我发现加载缓慢的原因在于页面被标记为不可缓存，即为了响应每一个请求，页面都是动态生成的。由于页面本身并不需要经常性的变更，并且不涉及个性化，那么这样做其实并没有必要。为了验证一下我的结论，我将页面标记为每5秒缓存一次，仅仅做了这一个调整，就能明显的感受到性能的提升。第一个字节到达的时间降低到几毫秒，同时页面的加载明显要更快。

并不是只有大规模的内容分发网络（CDN）可以在使用缓存中受益——缓存还可以提高负载平衡器、反向代理和应用服务器前端web服务的性能。通过上面的例子，我们看到，缓存内容结果，可以更高效的使用应用服务器，因为不需要每次都去做重复的页面生成工作。此外，Web缓存还可以用来提高网站可靠性。当服务器宕机或者繁忙时，比起返回错误信息给用户，不如通过配置NGINX将已经缓存下来的内容发送给用户。这意味着，网站在应用服务器或者数据库故障的情况下，可以保持部分甚至全部的功能运转。

下一部分讨论如何安装和配置NGINX的基础缓存（Basic Caching）。

## 如何安装和配置基础缓存

我们只需要两个命令就可以启用基础缓存：[**proxy\_cache\_path**](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cache_path)和[**proxy\_cache**](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_cache)。**proxy\_cache\_path**用来设置缓存的路径和配置，**proxy\_cache**用来启用缓存。

```nginx
proxy_cache_path /path/to/cache levels=1:2 keys_zone=my_cache:10m max_size=10g inactive=60m
use_temp_path=off;
server {
  ...
  location / {
	proxy_cache my_cache;
	proxy_pass http://my_upstream;
  }
}
```

**proxy\_cache\_path**命令中的参数及对应配置说明如下：

1. 用于缓存的本地磁盘目录是**/path/to/cache/**   
2. **levels**在**/path/to/cache/**设置了一个两级层次结构的目录。将大量的文件放置在单个目录中会导致文件访问缓慢，所以针对大多数部署，我们推荐使用两级目录层次结构。如果**levels**参数没有配置，则NGINX会将所有的文件放到同一个目录中。  
3. **keys_zone**设置一个共享内存区，该内存区用于存储缓存键和元数据，有些类似计时器的用途。将键的拷贝放入内存可以使NGINX在不检索磁盘的情况下快速决定一个请求是**HIT**还是**MISS**，这样大大提高了检索速度。一个1MB的内存空间可以存储大约8000个key，那么上面配置的10MB内存空间可以存储差不多80000个key。  
4. **max_size**设置了缓存的上限（在上面的例子中是10G）。这是一个可选项；如果不指定具体值，那就是允许缓存不断增长，占用所有可用的磁盘空间。当缓存达到这个上线，处理器便调用**cache manager**来移除最近最少被使用的文件，这样把缓存的空间降低至这个限制之下。  
5. **inactive**指定了项目在不被访问的情况下能够在内存中保持的时间。在上面的例子中，如果一个文件在60分钟之内没有被请求，则缓存管理将会自动将其在内存中删除，不管该文件是否过期。该参数默认值为10分钟（10m）。注意，非活动内容有别于过期内容。NGINX不会自动删除由缓存控制头部指定的过期内容（本例中Cache-Control:max-age=120）。过期内容只有在**inactive**指定时间内没有被访问的情况下才会被删除。如果过期内容被访问了，那么NGINX就会将其从原服务器上刷新，并更新对应的**inactive**计时器。  
6. NGINX最初会将注定写入缓存的文件先放入一个临时存储区域， **use\_temp\_path=off**命令指示NGINX将在缓存这些文件时将它们写入同一个目录下。我们强烈建议你将参数设置为**off**来避免在文件系统中不必要的数据拷贝。**use\_temp\_path**在NGINX1.7版本和NGINX Plus R6中有所介绍。最终，**proxy\_cache**命令启动缓存那些URL与location部分匹配的内容（本例中，为**/**）。你同样可以将**proxy\_cache**命令添加到server部分，这将会将缓存应用到所有的那些location中未指定自己的**proxy\_cache**命令的服务中。

## 陈旧总比没有强

NGINX[内容缓存](https://www.nginx.com/products/content-caching-nginx-plus/)的一个非常强大的特性是：当无法从原始服务器获取最新的内容时，NGINX可以分发缓存中的陈旧（stale，编者注：即过期内容）内容。这种情况一般发生在关联缓存内容的原始服务器宕机或者繁忙时。比起对客户端传达错误信息，NGINX可发送在其内存中的陈旧的文件。NGINX的这种代理方式，为服务器提供额外级别的容错能力，并确保了在服务器故障或流量峰值的情况下的正常运行。为了开启该功能，只需要添加[**proxy\_cache\_use\_stale**](http://nginx.org/en/docs/http/ngx_http_proxy_module.html?&_ga=1.14624247.1568941527.1438257987#proxy_cache_use_stale)命令即可：


```nginx
location / {
  ...
  proxy_cache_use_stale error timeout http_500 http_502 http_503           http_504;
}
```

按照上面例子中的配置，当NGINX收到服务器返回的error，timeout或者其他指定的5xx错误，并且在其缓存中有请求文件的陈旧版本，则会将这些陈旧版本的文件而不是错误信息发送给客户端。

## 缓存微调

NGINX提供了丰富的可选项配置用于缓存性能的微调。下面是使用了几个配置的例子：


```nginx
proxy_cache_path /path/to/cache levels=1:2 keys_zone=my_cache:10m max_size=10g inactive=60m
use_temp_path=off;
server {
  ...
  location / {
	proxy_cache my_cache;
	proxy_cache_revalidate on;
	proxy_cache_min_uses 3;
	proxy_cache_use_stale error timeout updating http_500 http_502   http_503 http_504;
	proxy_cache_lock on;
	proxy_pass http://my_upstream;
	}
}
```

这些命令配置了下列的行为：

1. [**proxy\_cache\_revalidate**](http://nginx.org/r/proxy_cache_revalidate?_ga=1.80437143.1235345339.1438303904)指示NGINX在刷新来自服务器的内容时使用**GET**请求。如果客户端的请求项已经被缓存过了，但是在缓存控制头部中定义为过期，那么NGINX就会在GET请求中包含**If-Modified-Since**字段，发送至服务器端。这项配置可以节约带宽，因为对于NGINX已经缓存过的文件，服务器只会在该文件请求头中**Last-Modified**记录的时间内被修改时才将全部文件一起发送。  
2. [**proxy\_cache\_min\_uses**](http://nginx.org/r/proxy_cache_min_uses?_ga=1.82886422.1235345339.1438303904)设置了在NGINX缓存前，客户端请求一个条目的最短时间。当缓存不断被填满时，这项设置便十分有用，因为这确保了只有那些被经常访问的内容才会被添加到缓存中。该项默认值为1。
3. [**proxy\_cache\_use\_stale**](http://nginx.org/en/docs/http/ngx_http_proxy_module.html?&_ga=1.13131319.1235345339.1438303904#proxy_cache_use_stale)中的**updating**参数告知NGINX在客户端请求的项目的更新正在原服务器中下载时发送旧内容，而不是向服务器转发重复的请求。第一个请求陈旧文件的用户不得不等待文件在原服务器中更新完毕。陈旧的文件会返回给随后的请求直到更新后的文件被全部下载。  
4. 当[**proxy\_cache\_lock**](http://nginx.org/en/docs/http/ngx_http_proxy_module.html?&_ga=1.86844376.1568941527.1438257987#proxy_cache_lock)被启用时，当多个客户端请求一个缓存中不存在的文件（或称之为一个**MISS**），只有这些请求中的第一个被允许发送至服务器。其他请求在第一个请求得到满意结果之后在缓存中得到文件。如果不启用**proxy\_cache\_lock**，则所有在缓存中找不到文件的请求都会直接与服务器通信。

## 跨多硬盘分割缓存

使用NGINX，不需要建立一个R**A**ID（磁盘阵列）。如果有多个硬盘，NGINX可以用来在多个硬盘之间分割缓存。下面是一个基于请求URI跨越两个硬盘之间均分缓存的例子：

```nginx
proxy_cache_path /path/to/hdd1 levels=1:2 keys_zone=my_cache_hdd1:10m max_size=10g
inactive=60m use_temp_path=off;
proxy_cache_path /path/to/hdd2 levels=1:2 keys_zone=my_cache_hdd2:10m max_size=10g
inactive=60m use_temp_path=off;
split_clients $request_uri $my_cache {
  50%          “my_cache_hdd1”;
  50%          “my_cache_hdd2”;
}
server {
  ...
  location / {
	proxy_cache $my_cache;
	proxy_pass http://my_upstream;
  }
}
```

上例中的两个**proxy\_cache\_path**定义了两个缓存（**my\_cache\_hdd1**和**my\_cache\_hd22**）分属两个不同的硬盘。**split\_clients**配置部分指定了请求结果的一半在**my\_cache\_hdd1**中缓存，另一半在**my\_cache\_hdd2**中缓存。基于**$request\_uri**（请求URI）变量的哈希值决定了每一个请求使用哪一个缓存，对于指定URI的请求结果通常会被缓存在同一个缓存中

## 常见问题解答

**Q**: 可以检测NGINX缓存状态吗？

**A**: 可以，使用[**add\_header**](http://nginx.org/en/docs/http/ngx_http_headers_module.html?&_ga=1.253128009.1568941527.1438257987#add_header)指令：
**add_header X-Cache-Status $upstream\_cache\_status**

1. **MISS**——响应在缓存中找不到，所以需要在服务器中取得。这个响应之后可能会被缓存起来。  
2. **BYP**A**SS**——响应来自原始服务器而不是缓存，因为请求匹配了一个**proxy\_cache\_bypass**（见下面[我可以在缓存中打个洞吗](https://www.nginx.com/blog/nginx-caching-guide/#caching-guide-faq-hole-punch)？）。这个响应之后可能会被缓存起来。  
3. **EXPIRED**——缓存中的某一项过期了，来自原始服务器的响应包含最新的内容。  
4. **ST**A**LE**——内容陈旧是因为原始服务器不能正确响应。需要配置**proxy\_cache\_use\_stale**。  
5. **UPD**A**TING**——内容过期了，因为相对于之前的请求，响应的入口（entry）已经更新，并且**proxy\_cache\_use\_stale**的**updating**已被设置。  
6. **REV**A**LID**A**TED**——**proxy\_cache\_revalidate**命令被启用，NGINX检测得知当前的缓存内容依然有效（**If-Modified-Since**或者**If-None-Match**）。  
7. **HIT**——响应包含来自缓存的最新有效的内容。  

**Q**: NGINX 如何决定是否缓存？

**A**：默认情况下，NGINX需要考虑从原始服务器得到的**Cache-Control**标头。当在响应头部中**Cache-Control**被配置为**Private**，**No-Cache**，**No-Store**或者**Set-Cookie**，NGINX不进行缓存。NGINX仅仅缓存GET和HE**A**D客户端请求。你也可以参照下面的解答覆盖这些默认值。

**Q**: Cache-Control头部可否被忽略？

**A**: 可以，使用**proxy\_ignore\_headers**命令。如下列配置：

```nginx
location /images/ {
	proxy_cache my_cache;
	  proxy_ignore_headers Cache-Control;
	  proxy_cache_valid any 30m;
	  ...
}
```

NGINX会忽略所有/images/下的**Cache-Control**头。[**proxy\_cache\_valid**](http://nginx.org/en/docs/http/ngx_http_proxy_module.html?&_ga=1.250506950.1568941527.1438257987#proxy_cache_valid)命令强制规定缓存数据的过期时间，如果忽略**Cache-Control**头，则该命令是十分必要的。NGINX不会缓存没有过期时间的文件。
	
**Q**: 当在头部设置了Set-Cookie之后NGINX还能缓存内容吗？

**A**: 可以，使用**proxy\_ignore\_headers**命令，参见之前的解答。

**Q**: NGINX能否缓存POST 请求？

**A**: 可以，使用[**proxy\_cache\_methods**](http://nginx.org/en/docs/http/ngx_http_proxy_module.html?&_ga=1.244788933.1568941527.1438257987#proxy_cache_methods)命令：
**proxy\_cache\_methods GET HE**A**D POST**;

这个例子中可以缓存POST请求。其他附加的方法可以依次列出来的，如PUT。

**Q**: NGINX 可以缓存动态内容吗？

**A**: 可以，提供的**Cache-Control**头部可以做到。缓存动态内容，甚至短时间内的内容可以减少在原始数据库和服务器中加载，可以提高第一个字节的到达时间，因为页面不需要对每个请求都生成一次。

**Q**: 我可以再缓存中打个洞（Punch a Hole）吗？

**A**: 可以，使用**proxy\_cache\_bypass**命令：


```nginx
location / {
  proxy_cache_bypass $cookie_nocache $arg_nocache;
  ...
}
```

这个命令定义了哪种类型的请求需要向服务器请求而不是尝试首先在缓存中查找。有些时候又被称作在内存中“打个洞”。在上面的例子中，NGINX会针对**nocache cookie**或者参数进行直接请求服务器，如：http://www.example.com/?nocache=true。NGINX依然可以为将那些没有避开缓存的请求缓存响应结果。

**Q**: NGINX 使用哪些缓存键？

**A**: NGINX生成的键的默认格式是类似于下面的[NGINX变量](http://nginx.org/en/docs/varindex.html?_ga=1.49172198.1568941527.1438257987)的MD5哈希值: **$scheme$proxy\_host$request\_uri**，实际的算法有些复杂。


```nginx
proxy_cache_path /path/to/cache levels=1:2 keys_zone=my_cache:10m max_size=10g inactive=60m
use_temp_path=off;
server {
  ...
  location / {
	proxy_cache $my_cache;
	proxy_pass http://my_upstream;
  }
}
```

按照上面的配置，http://www.example.org/my\_image.jpg的缓存键被计算为md5("http://my\_upstream:80/my\_image.jpg")。
注意，[**$proxy\_host**](http://nginx.org/en/docs/http/ngx_http_proxy_module.html?&_ga=1.245124677.1568941527.1438257987#var_proxy_host)变量用于哈希之后的值而不是实际的主机名（www.example.com）。**$proxy_hos**t被定义为**proxy_pass**中指定的代理服务器的主机名和端口号。  

为了改变变量（或其他项）作为基础键，可以使用**proxy\_cache\_key**命令（下面的问题会讲到）。
	
**Q**: 可以使用Cookie作为缓存键的一部分吗？

**A**: 可以，缓存键可以配置为任意值，如： 
**proxy\_cache\_key** $proxy\_host$request\_uri$cookie\_jessionid;

**Q**: NGINX使用Etag头部吗？

**A**: 在NGINX 1.7.3和[NGINX Plus R5](https://www.nginx.com/blog/nginx-plus-r5-released/)及之后的版本，配合使用**If-None-Match**， **Etag**是完全支持的。

**Q**: NGINX 如何处理字节范围请求？

**A**: 如果缓存中的文件是最新的，NGINX会对客户端提出的字节范围请求传递指定的字节。如果文件并没有被提前缓存，或者是陈旧的，那么NGINX会从服务器上下载完整文件。如果请求了单字节范围，NGINX会尽快的将该字节发送给客户端，如果在下载的数据流中刚好有这个字节。如果请求指定了同一个文件中的多个字节范围，NGINX则会在文件下载完毕时将整个文件发送给客户端。

一旦文件下载完毕，NGINX将整个数据移动到缓存中，这样一来，无论将来的字节范围请求是单字节还是多字节范围，NGINX都可以在缓存中找到指定的内容立即响应。

**Q**: NGINX 支持缓存清洗吗？

**A**: [NGINX Plus](https://www.nginx.com/products/content-caching-nginx-plus/)支持有选择性的清洗缓存。当原始服务器上文件已经被更新，但是NGINX Plus缓存中文件依然有效（Cache-Control:max-age依然有效，proxy\_cache\_path命令中inactive参数设置的超时时间没有过期），这个功能便十分有用。使用NGINX Plus的缓存清洗特性，这个文件可以被轻易的删除。详细信息，参见[Purging Content from the Cache](https://www.nginx.com/products/content-caching-nginx-plus/#purging)。

**Q**: NGINX如何处理Pragma 头部？

**A**: 当客户端添加了**Pragma:no-cache**头部，则请求会绕过缓存直接访问服务器请求内容。NGINX默认不考虑**Pragma**头部，不过你可以使用下面的**proxy\_cache\_bypass**的命令来配置该特性：


```nginx
location /images/ {
  proxy_cache my_cache;
  proxy_cache_bypass $http_pragma;
  ...
}
```

**Q**: NGINX支持Vary 头部吗？

**A**: 是的，在[NGINX Plus R5](https://www.nginx.com/blog/nginx-plus-r5-released/)、NGINX1.7.7和之后的版本中是支持的。看看这篇不错的文章： [good overview of the Vary header。](https://www.fastly.com/blog/best-practices-for-using-the-vary-header/)

-----
译文：<http://www.jointforce.com/jfperiodical/article/949>  
原文：<https://www.nginx.com/blog/nginx-caching-guide/>  
