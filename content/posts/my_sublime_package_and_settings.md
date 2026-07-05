---
Title: 我的Sublime text 3使用的插件和配置
Summary: Sublime Text 3是一款强大而精巧的文本编辑器。从VIM到Sublime text，它使我的工作效率提高了很多。
Authors: Django Wong
Date: 2017-01-12
---

## 下载：

<https://www.sublimetext.com/3>

## 我的插件列表

- Align Arguments
- Alignment
- All Autocomplete
- AutoPEP8
- BrackeHighlighter
- ChineseLocalizations
- ConvertToUTF8
- DocBlockr
- Git
- HTML-CSS-JS prettify
- INI
- jedi - Python autoccompletion
- jQuery
- Kconfig Syntax Highlight
- MarkdownEditing
- Material Theme
- nginx
- Package Control
- phpfmt
- PHPIntel
- Pretty JSON
- SideBarEnhancements
- SublimeCodeIntel
- SublimeLinter
- TrailingSpaces
- Zephir


看起来真是太多了，应该重复的。

##  Package Control插件管理

首先我们要安装Package Control。使用`Ctrl` + `ESC下面的那个键`或者通过`View`->`Show Console`来打开命令行。将下面的代码复制到命令行里。敲击回车，网速快的话，几秒钟就可以安装成功了。

```json
import urllib.request,os,hashlib; h = 'df21e130d211cfc94d9b0905775a7c0f' + '1e3d39e33b79698005270310898eea76'; pf = 'Package Control.sublime-package'; ipp = sublime.installed_packages_path(); urllib.request.install_opener( urllib.request.build_opener( urllib.request.ProxyHandler()) ); by = urllib.request.urlopen( 'http://packagecontrol.io/' + pf.replace(' ', '%20')).read(); dh = hashlib.sha256(by).hexdigest(); print('Error validating download (got %s instead of %s), please try manual install' % (dh, h)) if dh != h else open(os.path.join( ipp, pf), 'wb' ).write(by)
```

如果安装成功，你就可以在`Preferences`菜单下看到`Package Settings`和`Package Control`。然后重启Sublime text 3。

## 进行汉化。

在Sublime Text 3中按下快捷键`Ctrl`+`Shift`+`P`,你可以看到一个下拉框。选择`Install Package`。选择完毕，等待一会，Sublime会下载package列表。弹出列表框后，输入`ChineseLocalizations`,点击安装即可，安装完成后，Sublime Text 3就会变成中文啦。

其他插件也是这样进行安装，很方便，也很快捷。Sublime Text的生态现在越来越不错，有很多插件。所以渐渐成为开发人员手中的利器。

## 插件说明


### Align Arguments

<https://packagecontrol.io/packages/Align%20Arguments>

一款自动格式化和参数对齐功能的插件。

### Alignment

<https://packagecontrol.io/packages/Alignment>

轻松对多个多行选择进行对齐。

### All Autocomplete

<https://packagecontrol.io/packages/All%20Autocomplete>

这个就不说了，自动完成功能，程序员基本都需要。

### AutoPEP8

<https://packagecontrol.io/packages/AutoPEP8>

能自动按照PEP8样式指南格式Python代码。

热键：`Command/Control + Shift + 8`，预览：`Ctrl + 8`

### BrackeHighlighter

<https://packagecontrol.io/packages/BracketHighlighter>

代码风格高亮

### ConvertToUTF8

<https://packagecontrol.io/packages/ConvertToUTF8>

`GBK`, `BIG5`, `EUC-KR`, `EUC-JP`, `Shift_JIS` 转UTF8，很强大。

### DocBlockr

<https://packagecontrol.io/packages/DocBlockr>

简单的代码注释，主要适用`Javascript`, `PHP`, `CoffeeScript`, `Actionscript`, `C` 和 `C++`。

### Git

<https://packagecontrol.io/packages/Git>

这就不说了，Git操作。喜欢用Git的人还是必须的。

### HTML-CSS-JS prettify

<https://packagecontrol.io/packages/HTML-CSS-JS%20Prettify>

前端开发人员拥有的。能让`HTML`,`CSS`,`JS`变得更美观。

### INI

<https://packagecontrol.io/packages/INI>

经常查看INI配置文件的，这个可以让文件内容高亮的

### Jedi - Python autocompletion

<https://packagecontrol.io/packages/Jedi%20-%20Python%20autocompletion>

很强大的Python自动完成，写Python的开发者可以试一试。

### jQuery

<https://packagecontrol.io/packages/jQuery>

前端开发人员拥有的。

### Kconfig Syntax Highlight

<https://packagecontrol.io/packages/Kconfig%20Syntax%20Highlight>

Kconfig language高亮。

### MarkdownEditing

<https://packagecontrol.io/packages/MarkdownEditing>

很强大的Markdown包。

### nginx

<https://packagecontrol.io/packages/nginx>

Nginx配置文件高亮。

### phpfmt

<https://packagecontrol.io/packages/phpfmt>

PHP代码格式化。

### PHPIntel

<https://packagecontrol.io/packages/PHPIntel>

PHP函数自动完成功能。

### Pretty JSON

<https://packagecontrol.io/packages/Pretty%20JSON>

JSON美化，验证，压缩，转XML。

### SublimeCodeIntel

<https://packagecontrol.io/packages/SublimeCodeIntel>

全功能的代码自动完成引擎。

### SublimeLinter

<https://packagecontrol.io/packages/SublimeLinter>

一个代码检测工具插件。

### TrailingSpaces

<https://packagecontrol.io/packages/TrailingSpaces>

使得代码中的空格高亮。

### Zephir

<https://packagecontrol.io/packages/Zephir>

写Zephird的语法高亮。
