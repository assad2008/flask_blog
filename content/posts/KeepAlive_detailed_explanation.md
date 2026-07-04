---
Title:   KeepAlive的一些概念
Summary: 关于这个问题，是在面试中，面试官提出，nginx的KeepAlive和TCP的KeepAlive的区别是什么，经过想起搜索和总结。得出一个结果！
Authors: Django Wong
Date:    2014-11-05
---

## 为什么要有KeepAlive？

在谈KeepAlive之前，我们先来了解下简单TCP知识(知识很简单，高手直接忽略)。首先要明确的是在TCP层是没有“请求”一说的，经常听到在TCP层发送一个请求，这种说法是错误的。TCP是一种通信的方式，“请求”一词是事务上的概念，HTTP协议是一种事务协议，如果说发送一个HTTP请求，这种说法就没有问题。也经常听到面试官反馈有些面试运维的同学，基本的TCP三次握手的概念不清楚，面试官问TCP是如何建立链接，面试者上来就说，假如我是客户端我发送一个请求给服务端，服务端发送一个请求给我。。。这种一听就知道对TCP基本概念不清楚。下面是我通过wireshark抓取的一个TCP建立握手的过程。（命令行基本上用TCPdump,后面我们还会用这张图说明问题）:

TCP三次握手的完整建立过程，第一个报文SYN从发起方发出，第二个报文SYN,ACK是从被连接方发出，第三个报文ACK确认对方的SYN，ACK已经收到，如下图：

![](/static/attach/tcp.jpg)

但是数据实际上并没有传输，请求是有数据的，第四个报文才是数据传输开始的过程，细心的读者应该能够发现wireshark把第四个报文解析成HTTP协议，HTTP协议的GET方法和URI也解析出来，所以说TCP层是没有请求的概念，HTTP协议是事务性协议才有请求的概念，TCP报文承载HTTP协议的请求(Request)和响应(Response)。

现在才是开始说明为什么要有KeepAlive。链接建立之后，如果应用程序或者上层协议一直不发送数据，或者隔很长时间才发送一次数据，当链接很久没有数据报文传输时如何去确定对方还在线，到底是掉线了还是确实没有数据传输，链接还需不需要保持，这种情况在TCP协议设计中是需要考虑到的。TCP协议通过一种巧妙的方式去解决这个问题，当超过一段时间之后，TCP自动发送一个数据为空的报文给对方，如果对方回应了这个报文，说明对方还在线，链接可以继续保持，如果对方没有报文返回，并且重试了多次之后则认为链接丢失，没有必要保持链接。

下面是TCP数据报文的格式：

![](/static/attach/tcpdata.jpg)

## TCP KeepAlive和HTTP的Keep-Alive是一样的吗？

估计很多人乍看下这个问题才发现其实经常说的KeepAlive不是这么回事，实际上在没有特指是TCP还是HTTP层的KeepAlive，不能混为一谈。TCP的KeepAlive和HTTP的Keep-Alive是完全不同的概念。TCP层的KeepAlive上面已经解释过了。 HTTP层的Keep-Alive是什么概念呢？ 在讲述TCP链接建立的时候，我画了一张三次握手的示意图，TCP在建立链接之后， HTTP协议使用TCP传输HTTP协议的请求(Request)和响应(Response)数据，一次完整的HTTP事务如下图：

![](/static/attach/httpkeepalive.jpg)

这张图我简化了HTTP(Req)和HTTP(Resp)，实际上的请求和响应需要多个TCP报文。从图中可以发现一个完整的HTTP事务，有链接的建立，请求的发送，响应接收，断开链接这四个过程,早期通过HTTP协议传输的数据以文本为主，一个请求可能就把所有要返回的数据取到，但是，现在要展现一张完整的页面需要很多个请求才能完成，如图片,JS,CSS等，如果每一个HTTP请求都需要新建并断开一个TCP，这个开销是完全没有必要的，开启HTTP Keep-Alive之后，能复用已有的TCP链接，当前一个请求已经响应完毕，服务器端没有立即关闭TCP链接，而是等待一段时间接收浏览器端可能发送过来的第二个请求，通常浏览器在第一个请求返回之后会立即发送第二个请求，如果某一时刻只能有一个链接，同一个TCP链接处理的请求越多，开启KeepAlive能节省的TCP建立和关闭的消耗就越多。当然通常会启用多个链接去从服务器器上请求资源，但是开启了Keep-Alive之后，仍然能加快资源的加载速度。HTTP/1.1之后默认开启Keep-Alive, 在HTTP的头域中增加Connection选项。当设置为Connection:keep-alive表示开启，设置为Connection:close表示关闭。实际上HTTP的KeepAlive写法是Keep-Alive，跟TCP的KeepAlive写法上也有不同。所以TCP KeepAlive和HTTP的Keep-Alive不是同一回事情。

## Nginx的KeepAlive

在nginx中，对于http1.0与http1.1也是支持长连接的。什么是长连接呢？我们知道，http请求是基于TCP协议之上的，那么，当客户端在发起请求前，需要先与服务端建立TCP连接，而每一次的TCP连接是需要三次握手来确定的，如果客户端与服务端之间网络差一点，这三次交互消费的时间会比较多，而且三次交互也会带来网络流量。当然，当连接断开后，也会有四次的交互，当然对用户体验来说就不重要了。而http请求是请求应答式的，如果我们能知道每个请求头与响应体的长度，那么我们是可以在一个连接上面执行多个请求的，这就是所谓的长连接，但前提条件是我们先得确定请求头与响应体的长度。

服务端在输出完body之后，会可以考虑使用长连接。能否使用长连接，也是有条件限制的。如果客户端的请求头中的connection为close，则表示客户端需要关掉长连接，如果为keep-alive，则客户端需要打开长连接，如果客户端的请求中没有connection这个头，那么根据协议，如果是http1.0，则默认为close，如果是http1.1，则默认为keep-alive。如果结果为keepalive，那么，nginx在输出完响应体后，会设置当前连接的keepalive属性，然后等待客户端下一次请求。当然，nginx不可能一直等待下去，如果客户端一直不发数据过来，岂不是一直占用这个连接？所以当nginx设置了keepalive等待下一次的请求时，同时也会设置一个最大等待时间，这个时间是通过选项keepalive_timeout来配置的，如果配置为0，则表示关掉keepalive，此时，http版本无论是1.1还是1.0，客户端的connection不管是close还是keepalive，都会强制为close。

如果服务端最后的决定是keepalive打开，那么在响应的http头里面，也会包含有connection头域，其值是”Keep-Alive”，否则就是”Close”。如果connection值为close，那么在nginx响应完数据后，会主动关掉连接。所以，对于请求量比较大的nginx来说，关掉keepalive最后会产生比较多的time-wait状态的socket。一般来说，当客户端的一次访问，需要多次访问同一个server时，打开keepalive的优势非常大，比如图片服务器，通常一个网页会包含很多个图片。打开keepalive也会大量减少time-wait的数量。

---------------------------------

以上部分内容来自互联网，如有侵权，敬请联系我
