#/usr/bin/python
#coding=utf-8

import socket, struct
import markdown2

markdownext = ['wiki-tables','tables','codehilite','nl2br','toc','footnotes','wikilinks','metadata','code-color']
		
def gistcode(content):
	result = list(set(re.findall(r"(<a[^<>]*>\s*(https://gist.github.com/\d+)\s*</a>)", content)))
	for i,link in result:
		content = content.replace(i, '%s <script src="%s.js"></script>' % (i, link))
	return content

def mk2html(mk_content):
	html = markdown2.markdown(mk_content,extras = markdownext)
	return html
	
def get_mk_metadata(mk_content):
	mk_meta = markdown2.markdown(mk_content,extras = ['metadata'])
	return mk_meta

def ip2long(ip):
	return struct.unpack("!I",socket.inet_aton(ip))[0]

def long2ip(num):
	return socket.inet_ntoa(struct.pack("!I",num))
	
def makerss(bloglists,url,sitename):
	xml = ''
	xml += '<?xml version="1.0" encoding="utf-8" ?>' + "\n"
	xml += '<rss version="2.0">' + "\n"
	xml += '<channel>' + "\n"
	xml += '<title>%s</title>' % sitename + "\n"
	xml += '<link>%s</link>' % url + "\n"
	xml += '<description>Latest 20 threads of all Posts</description>' + "\n"
	xml += '<copyright>Copyright(C) %s</copyright>' % sitename + "\n"
	xml += '<generator>%s by River King.</generator>' % sitename + "\n"
	xml += '<lastBuildDate>' + datetime.datetime.now().strftime("%Y-%m-%d %X") + '</lastBuildDate>' + "\n"
	xml += '<ttl>3600</ttl>' + "\n"
	for l in bloglists:
		xml += '<item>' + "\n"
		xml += '<title>' + l.get('Title').encode('utf-8') + '</title>' + "\n"
		xml += '<link>http://blog.itmark.net/posts/' + l.get('filename').encode('utf-8') + '.html</link>' + "\n"
		xml += '<description><![CDATA[' + l.get('Summary').encode('utf-8') + ']]></description>' + "\n"
		xml += '<author>River King</author>' + "\n"
		xml += '<pubDate>' + l.get('createtime').encode('utf-8') + '</pubDate>' + "\n"
		xml += '</item>' + "\n"
	xml += '</channel>' + "\n"
	xml += '</rss>'
	return xml