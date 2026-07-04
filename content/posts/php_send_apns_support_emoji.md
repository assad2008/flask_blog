---
Title:   让APNS支持发送Emoji表情符号
Summary: iOS设置是默认支持emoji表情的，如何让我们的Apple Push Notification Service的内容更加个性化呢，不要拘泥于文字形式，有时候表情会起到很好的作用
Authors: Django Wong
Date:    2013-11-28
---

iOS设置是默认支持emoji表情的，如何让我们的Apple Push Notification Service的内容更加个性化呢，不要拘泥于文字形式，有时候表情会起到很好的作用

![](http://yeebox.qiniudn.com/php-emoji.png)

首先我们要知道emoji表情来如何表示？

[http://www.unicode.org/~scherer/emoji4unicode/snapshot/full.html](http://www.unicode.org/~scherer/emoji4unicode/snapshot/full.html)

unicode网站给出了emoji表情的unicode表示方式以及对照表。

因为iOS设备中，
`iOS 5 Emoji`采用`Unicode6`标准来统一code points，而在`iOS4`中，是采用`SoftBank`编码的形式。
因此emoji在不同设备上的显示可以会出现方块等，比如在iOS5上可以显示的，在iOS4上也许无法显示，因为`unicode6`和`softbank`编码的不同。
iOS4到5，按理说应该兼容，也就是说，iOS应该自动判断如果是`softbank`编码，自动转成`unicode6`。但现在看来， iOS5.1（大陆版）好像只支持`unicode6`, 而不支持`softbank`。
因此，PUSH的时候，我们也一定要使用unicode的emoji表情，我个人意不推荐使用softbank编码，因为目前iOS设备，基本上都是5或者6了，所以不会出现大量无法显示的设备了。

有个很好的PHP library ：[http://code.iamcal.com/php/emoji/](http://code.iamcal.com/php/emoji/)，大家可以使用之处理emoji在不同编码模式下的转换

现在我们写短小代码，来做示范。

	<?php

	$mmap = array('smiling face with heart-shaped eyes','bouquet','clapping hands sign','thumbs up sign','multiple musical notes','face throwing a kiss','wrapped present','winking face','smirking face','grinning cat face with smiling eyes','face with stuck-out tongue and winking eye','face savouring delicious food','kissing face with closed eyes','ghost','extraterrestrial alien','rose','glowing star','black sun with rays','cloud','sun behind cloud','high voltage sign','beating heart','sparkles','tongue','four leaf clover','umbrella with rain drops','snowman without snow','cyclone','foggy','closed umbrella','night with stars','sunrise over mountains','sunrise','cityscape at dusk','sunset over buildings','rainbow','snowflake','bridge at night','water wave','volcano','milky way','earth globe asia-australia','new moon symbol','waxing gibbous moon symbol','first quarter moon symbol','crescent moon','full moon symbol','first quarter moon with face','shooting star','clock face one oclock','clock face two oclock','clock face three oclock','clock face four oclock','clock face five oclock','clock face six oclock','clock face seven oclock','clock face eight oclock','clock face nine oclock','clock face ten oclock','clock face eleven oclock','clock face twelve oclock','watch','watermelon','lipstick','baby angel','octopus');


	$mmapa = array("\xf0\x9f\x98\x8d","\xf0\x9f\x92\x90","\xf0\x9f\x91\x8f","\xf0\x9f\x91\x8d","\xf0\x9f\x8e\xb6","\xf0\x9f\x98\x98","\xf0\x9f\x8e\x81","\xf0\x9f\x98\x89","\xf0\x9f\x98\x8f","\xf0\x9f\x98\xb8","\xf0\x9f\x98\x9c","\xf0\x9f\x98\x8b","\xf0\x9f\x98\x9a","\xf0\x9f\x91\xbb","\xf0\x9f\x91\xbd","\xf0\x9f\x8c\xb9","\xf0\x9f\x8c\x9f","\xe2\x98\x80","\xe2\x98\x81","\xe2\x9b\x85","\xe2\x9a\xa1","\xf0\x9f\x92\x93","\xe2\x9c\xa8","\xf0\x9f\x91\x85","\xf0\x9f\x8d\x80","\xe2\x98\x94","\xe2\x9b\x84","\xf0\x9f\x8c\x80","\xf0\x9f\x8c\x81","\xf0\x9f\x8c\x82","\xf0\x9f\x8c\x83","\xf0\x9f\x8c\x84","\xf0\x9f\x8c\x85","\xf0\x9f\x8c\x86","\xf0\x9f\x8c\x87","\xf0\x9f\x8c\x88","\xe2\x9d\x84","\xf0\x9f\x8c\x89","\xf0\x9f\x8c\x8a","\xf0\x9f\x8c\x8b","\xf0\x9f\x8c\x8c","\xf0\x9f\x8c\x8f","\xf0\x9f\x8c\x91","\xf0\x9f\x8c\x94","\xf0\x9f\x8c\x93","\xf0\x9f\x8c\x99","\xf0\x9f\x8c\x95","\xf0\x9f\x8c\x9b","\xf0\x9f\x8c\xa0","\xf0\x9f\x95\x90","\xf0\x9f\x95\x91","\xf0\x9f\x95\x92","\xf0\x9f\x95\x93","\xf0\x9f\x95\x94","\xf0\x9f\x95\x95","\xf0\x9f\x95\x96","\xf0\x9f\x95\x97","\xf0\x9f\x95\x98","\xf0\x9f\x95\x99","\xf0\x9f\x95\x9a","\xf0\x9f\x95\x9b","\xe2\x8c\x9a","\xf0\x9f\x8d\x89","\xf0\x9f\x92\x84","\xf0\x9f\x91\xbc","\xf0\x9f\x90\x99");

写了短小代码，普通的字符串和emoji的对照表。(已采用unicode编码方式)

	$a = "今天天气真好啊sunset";
	$b = str_replace($mmap,$mmapa,$a);

这样，我们就把a中的内容替换成unicode的编码的内容的，推送到iOS设备中就可以显示出太阳升起的表情了。
至于更详细的对照表，大家看根据[http://code.iamcal.com/php/emoji/](http://code.iamcal.com/php/emoji/)中，继续更新。上面的对照表只列举了一些常用的！

参考资料:

<http://en.wikipedia.org/wiki/Mapping_of_Unicode_characters#Private_use_characters>