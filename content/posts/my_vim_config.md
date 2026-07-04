---
Title:   我的VIM配置（代码补全，自动注释）
Summary: 特意整理了一番，现在分享一下，需装一下插件：neocomplcache,gvimfullscreen,DoxygenToolkit。
Authors: Django Wong
Date:    2013-11-30
---

特意整理了一番，现在分享一下，需装一下插件：`neocomplcache`,`gvimfullscreen`,`DoxygenToolkit`。  

	"常用设置
	set nu!
	set ts=2
	set sw=2
	set noai
	set nocp
	set history=100 "历史为100个
	set nocompatible  "去掉VIM键盘模式
	set noexpandtab
	set clipboard+=unnamed  "与windows共享剪贴板

	"在状态行上显示光标所在位置的行号和列号
	"set ruler
	"set rulerformat=%20(%2*%<%f%=\ %m%r\ %3l\ %c\ %p%%%)

	set nocin
	set nobackup  "禁止生成备份文件
	set paste
	set formatoptions=tcrqn
	set iskeyword+=_,$,@,%,#,-  "带有如下符号的单词不要被换行分割

	set guioptions-=T  "去掉工具条
	set guioptions-=m " 隐藏菜单栏
	set guioptions-=L " 隐藏左侧滚动条
	set guioptions-=r " 隐藏右侧滚动条
	set guioptions-=b " 隐藏底部滚动条
	set showtabline=0 " 隐藏Tab栏

	au GUIEnter * simalt ~x "自动最大化

	filetype on "检测文件类型
	filetype plugin on "载入文件类型插件

	syntax on "语法高亮

	source $VIMRUNTIME/vimrc_example.vim  
	source $VIMRUNTIME/mswin.vim  
	behave mswin

	"配色方案
	colors slate
	set guifont=Courier\ New\ Bold:h14
	set backspace=indent,eol,start

	"强制UTF-8字符
	set termencoding=utf-8  
	set fileencodings=utf-8,usc-bom,euc-jp,gb18030,gbk,gb2312,cp936

	if has("win32")  
		set fileencoding=chinese
	else  
		set fileencoding=utf-8  
	endif

	"底部状态栏
	highlight StatusLineNC guifg=Gray guibg=White
	set laststatus=2
	set statusline=%F%m%r%h%w\ [%{strftime(\"%m-%d\ %H:%M\")}\][格式:%Y]\[ASCII:%03.3b]\[HEX:%02.2B]\[位置:%l,%v][进度:%p%%]\[行数:%L]
	let &termencoding=&encoding

	"全屏
	if has('gui_running') && has("win32")
		map <F11> :call libcallnr("gvimfullscreen.dll", "ToggleFullScreen", 0)<CR>
	endif

	"自动提示
	let g:neocomplcache_enable_at_startup=1  "启动
	let g:neocomplcache_enable_smart_case = 1 
	let g:neocomplcache_enable_camel_case_completion = 1 
	let g:neocomplcache_min_syntax_length = 3
	let g:neocomplcache_lock_buffer_name_pattern = '\*ku\*' 
	let g:neocomplcache_max_keyword_width = 80
	let g:neocomplcache_max_filename_width = 255
	let g:neocomplcache_min_keyword_length = 3
	let g:neocomplcache_min_syntax_length = 3
	if !exists('g:neocomplcache_keyword_patterns')
	  let g:neocomplcache_keyword_patterns = {}
	endif
	let g:neocomplcache_keyword_patterns['default'] = '\h\w*'
	if !exists('g:neocomplcache_omni_patterns') 
	let g:neocomplcache_omni_patterns = {} 
	endif 
	autocmd FileType php set omnifunc=phpcomplete#CompletePHP
	let g:neocomplcache_omni_patterns.php = '[^. \t]->\h\w*\|\h\w*::'
	imap <expr><TAB> neocomplcache#sources#snippets_complete#expandable() ? "\<Plug>(neocomplcache_snippets_expand)" : pumvisible() ? "\<C-n>" : "\<TAB>"


	"doxygen toolkit 注释插件
	let g:DoxygenToolkit_briefTag_pre="@synopsis  "
	let g:DoxygenToolkit_paramTag_pre="@param "
	let g:DoxygenToolkit_returnTag="@returns   "
	let g:DoxygenToolkit_blockHeader="--------------------------------------------------------------------------"
	let g:DoxygenToolkit_blockFooter="----------------------------------------------------------------------------"
	let g:DoxygenToolkit_authorName="Yee, <assad2008@sina.com>"
	let g:DoxygenToolkit_licenseTag="GPL 2.0"

	let g:DoxygenToolkit_authorName="Yee, <assad2008@sina.com>"
	let s:licenseTag = "Copyright(C)\<enter>"
	let s:licenseTag = s:licenseTag . "For free\<enter>"
	let s:licenseTag = s:licenseTag . "All right reserved\<enter>"
	let g:DoxygenToolkit_licenseTag = s:licenseTag
	let g:DoxygenToolkit_briefTag_funcName="yes"
	let g:doxygen_enhanced_color=1