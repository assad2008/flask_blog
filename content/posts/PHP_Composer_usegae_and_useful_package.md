---
Authors: Django Wong
Date: 2017-02-13
Summary: composer是PHP中用来管理依赖(dependency)关系的工具。你可以在自己的项目中声明所依赖的外部工具库(libraries)，Composer会帮你安装这些依赖的库文件。
Title: PHP Compsoer使用以及常用的一些Package（2019-8-24更新）
seo_description: Composer是PHP的依赖管理工具，帮助开发者轻松安装和管理项目所需的库文件。本文详细介绍Composer的安装方法，并汇总了2019年常用的PHP
  Package，涵盖Web框架（Yaf、Laravel、Yii2等）、数据库、ORM、微信支付宝支付、网络请求、字符串处理及模板引擎等类别，是PHP开发者优化项目依赖的实用指南。
seo_keywords: PHP Composer, Composer安装, PHP依赖管理, 常用PHP Package, Composer包推荐
---

## Compsoer简介

Composer 是 PHP5以上 的一个依赖管理工具。它允许你申明项目所依赖的代码库，它会在你的项目中为你安装他们。Composer 不是一个包管理器。是的，它涉及 "packages" 和 "libraries"，但它在每个项目的基础上进行管理，在你项目的某个目录中（例如 vendor）进行安装。默认情况下它不会在全局安装任何东西。因此，这仅仅是一个依赖管理。

## Composer的安装

```php
curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer
```

或者：

```php
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
php composer-setup.php --install-dir=/usr/local/bin --filename=composer
```

然后执行：

```php
#composer -V
#Composer version 1.9.0
```

这样就说明Composer安装成功。

关于Compsoer的其他，请查看 <https://getcomposer.org/doc/>

##	我使用的Composer包

### Web FrameWorks

- `Yaf`，Yaf框架，简单易用，性能强大。访问：<https://github.com/assad2008/Yaf-Skeleton>
- `slim/slim`，Slim框架。访问：<https://packagist.org/packages/slim/slim>  
- `yiisoft/yii2`，Yii2框架。访问：<https://packagist.org/packages/yiisoft/yii2>  
- `laravel/laravel`，Laravel框架。访问：<https://packagist.org/packages/laravel/laravel>
- `codeigniter/framework`，Codeigniter框架。访问：<https://packagist.org/packages/codeigniter/framework>  

### Database

- `zf1/zend-db`，ZF1的数据库封装，很好使用。访问：<https://packagist.org/packages/zf1/zend-db>  
- `mongodb/mongodb`，Mongodb数据库驱动。访问：<https://packagist.org/packages/mongodb/mongodb>  
- `predis/predis`，Redis数据库访问，支持PHP和HHVM。访问：<https://packagist.org/packages/predis/predis>  
- `4k1r0/codeigniterdb`，Codeigniter框架的BD类，访问：<https://packagist.org/packages/4k1r0/codeigniterdb>  

### ORM

- `illuminate/database`，全功能的数据访问框架。访问：<https://packagist.org/packages/illuminate/database>  
- `doctrine/orm`，Doctrine的ORM库。访问：<https://packagist.org/packages/doctrine/orm>  
- `vrana/notorm`，ORM框架。访问：<https://packagist.org/packages/vrana/notorm>  
- `catfan/medoo`，强大高效ORM库，访问：<https://packagist.org/packages/catfan/medoo>  
- `propel/propel`，一个高效，自由的ORM库。访问：<https://packagist.org/packages/propel/propel>  
- `gabordemooij/redbean`。另一个ORM类。访问：<https://packagist.org/packages/gabordemooij/redbean>


### Wechat&Alipay

- `overtrue/wechat`，安的微信SDK，很全面，很好用。访问：<https://packagist.org/packages/overtrue/wechat>  
- `jiaweixs/weapp`，微信小程序SDK。访问：<https://packagist.org/packages/jiaweixs/weapp> 
- `yansongda/pay`，专注 Alipay 和 WeChat 的支付扩展包。访问：<https://packagist.org/packages/yansongda/pay>  
- `riverslei/payment`，支付宝，微信支，招商一网通支付SDK。访问：<https://packagist.org/packages/riverslei/payment>  
- `lokielse/omnipay-alipay`，支付宝支付网关。访问：<https://packagist.org/packages/lokielse/omnipay-alipay>  

### Networks

- `guzzlehttp/guzzle`，HTTP客户端，很强大。访问：<https://packagist.org/packages/guzzlehttp/guzzle>  
- `rmccue/requests`，另一个HTTP客户端。访问：<https://packagist.org/packages/rmccue/requests>  
- `nategood/httpful`，对REST友好的HTTP客户端。访问：<https://github.com/nategood/httpful>  
- `php-curl-class/php-curl-class`，基于curl的HTTP访问请求。访问：<https://github.com/php-curl-class/php-curl-class>  

### String

- `danielstjules/stringy`，很强大的字符串处理。访问：<https://packagist.org/packages/danielstjules/stringy>  
- `cebe/markdown`，高效的Markdown解析库。访问：<https://packagist.org/packages/cebe/markdown>  
- `michelf/php-markdown`，PHP的markdown库。访问：<https://packagist.org/packages/michelf/php-markdown>  
- `paragonie/random_compat`，随机字符串生成。访问：<https://packagist.org/packages/paragonie/random_compat>  
- `hashids/hashids`，生成不重复的随机字符串。访问：<https://packagist.org/packages/hashids/hashids>  
- `ramsey/uuid` ，生成UUID，支持V1,3,4,5等版本。访问：<https://packagist.org/packages/ramsey/uuid>  
- `wyrihaximus/html-compress`，HTML压缩，去掉空格，行等。访问：<https://packagist.org/packages/wyrihaximus/html-compress>  
- `sabre/uri`，Url解析类。访问：<https://packagist.org/packages/sabre/uri>  
- `league/uri`，URI操作类。访问：<https://packagist.org/packages/league/uri>  
- `ua-parser/uap-php`，UserAgent解析类。访问：<https://packagist.org/packages/ua-parser/uap-php> 
- `jwage/purl`。URL管理类。访问：<https://packagist.org/packages/jwage/purl>    
- `ezyang/htmlpurifier`，HTML白名单过滤。访问：<https://packagist.org/packages/ezyang/htmlpurifier>  
- `overtrue/pinyin`，中文转拼音方案。访问：<https://packagist.org/packages/overtrue/pinyin>  

### Temppate

- Twig，`twig/twig`，高效的摸模板引擎。访问：<https://packagist.org/packages/twig/twig>  
- Smarty,`smarty/smarty`,Smarty模板引擎。访问：<https://packagist.org/packages/smarty/smarty>  

### Files

- `league/flysystem`，很强大的文件操作，支持S3等。访问：<https://packagist.org/packages/league/flysystem>  
- `codeguy/upload`，上传类。访问：<https://packagist.org/packages/codeguy/upload>  
- `fuelphp/upload`，上传类。访问：<https://packagist.org/packages/fuelphp/upload>  

### Caching

- `doctrine/cache`，强大的Cache类。访问：<https://packagist.org/packages/doctrine/cache>  
- `zendframework/zend-cache`，ZF的cache类。访问：<https://packagist.org/packages/zendframework/zend-cache>  
- `illuminate/cache`。laravel的cache类。访问：<https://packagist.org/packages/illuminate/cache>  

### Image

- `imagine/imagine`，图片处理类。访问：<https://packagist.org/packages/imagine/imagine>  
- `intervention/image`，强大的图片处理类。访问：<https://packagist.org/packages/intervention/image>  
- `kosinix/grafika`，很好用的图片处理类。访问：<https://packagist.org/packages/kosinix/grafika>  
- `gregwar/image`，图片处理。访问：<https://packagist.org/packages/gregwar/image>  
- `aferrandini/phpqrcode`，二维码生成。访问：<https://packagist.org/packages/aferrandini/phpqrcode>  
- `endroid/qr-code`，二维码生成。访问：<https://packagist.org/packages/endroid/qr-code>  
- `laravolt/avatar`，根据名称或者邮箱生成头像。访问：<https://packagist.org/packages/laravolt/avatar>

### Captcha

- `gregwar/captcha`，很好使用的验证码生成类。访问：<https://packagist.org/packages/gregwar/captcha>  
- `google/recaptcha`，google的验证码类。访问：<https://packagist.org/packages/google/recaptcha>  

### GEO

- geoip2，`geoip2/geoip2`，GEOIP类。访问：<https://packagist.org/packages/geoip2/geoip2>  
- geocoder，`willdurand/geocoder`，Geo类库。访问：<https://packagist.org/packages/willdurand/geocoder>  

### Tools

- `fzaninotto/faker`，一些有用的函数处理。访问：<https://packagist.org/packages/fzaninotto/faker>  
- `lstrojny/functional-php`，一些有用的PHP函数。访问：<https://packagist.org/packages/lstrojny/functional-php>  
- `moneyphp/money`，货币适配处理。访问：<https://packagist.org/packages/moneyphp/money>  
- `ngfw/recipe`，一些有用的函数。访问：<https://packagist.org/packages/ngfw/recipe>  
- `zhuzhichao/ip-location-zh`，根据IP获得地理位置。访问：<https://packagist.org/packages/zhuzhichao/ip-location-zh>  

### Date

- `jimmiw/php-time-ago`，很人性的时间戳格式化。访问：<https://packagist.org/packages/jimmiw/php-time-ago>  
- `nesbot/carbon`，简单的日期处理库。访问：<https://packagist.org/packages/nesbot/carbon>  

### Secure

- `defuse/php-encryption`，加密解密类。访问：<https://packagist.org/packages/defuse/php-encryption>  
- `phpseclib/phpseclib`，加密解密类。访问：<https://packagist.org/packages/phpseclib/phpseclib>  
- `passwordlib/passwordlib`，密码生成类。访问：<https://packagist.org/packages/passwordlib/passwordlib>  
- `spatie/url-signer`，URL加密验证类。访问：<https://packagist.org/packages/spatie/url-signer>
- `tuupola/base62`，base62类。访问：<https://packagist.org/packages/tuupola/base62>  
- `hautelook/phpass`，密码生成类。访问：<https://packagist.org/packages/hautelook/phpass> 

### Mail&SMS

- `overtrue/easy-sms`，安的短信发送库，很强大，也很全。访问：<https://packagist.org/packages/overtrue/easy-sms>
- `swiftmailer/swiftmailer`，很好用的邮件发送。访问：<https://packagist.org/packages/swiftmailer/swiftmailer>  
- `phpmailer/phpmailer`，全功能的邮件发送类。访问：<https://packagist.org/packages/phpmailer/phpmailer>  
- `hbattat/verifyemail`，邮件地址真实性验证。访问：<https://packagist.org/packages/hbattat/verifyemail>  

### Queue

- `php-amqplib/php-amqplib`，RabbitMQ类库。访问：<https://packagist.org/packages/php-amqplib/php-amqplib>  
- `enqueue/redis`，基于redis队列服务。访问：<https://packagist.org/packages/enqueue/redis>  

### Debug

- `tracy/tracy`，很帮的调试工具。访问：<https://packagist.org/packages/tracy/tracy>  
- `filp/whoops`，错误调试工具，访问：<https://packagist.org/packages/filp/whoops>  

### Variables Dump

- `leeoniya/dump-r`，很棒的var_dump。访问：<https://packagist.org/packages/leeoniya/dump-r>  
- `digitalnature/php-ref`，很漂亮的Dump工具。访问：<https://packagist.org/packages/digitalnature/php-ref>  
- `symfony/var-dumper`，symfony的Dump工具。访问：<https://packagist.org/packages/symfony/var-dumper>  

### Other

- `phpoffice/phpspreadsheet`，PHP的excel解决方案。访问：<https://packagist.org/packages/phpoffice/phpspreadsheet>   
- `lusitanian/oauth`，Oauth1,2类库。访问：<https://packagist.org/packages/lusitanian/oauth>  
- `get-stream/stream`，一个Stream类库。访问：<https://packagist.org/packages/get-stream/stream>  
- `zf1/zend-registry`，ZF1的一个很好用的玩意。<https://packagist.org/packages/zf1/zend-registry>  
- `ddeboer/data-import`，支持多种数据格式的导入导出库。访问：<https://packagist.org/packages/ddeboer/data-import>