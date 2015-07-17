#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-07-16 07:55:02

import urllib

'''
urllib提供一个访问Web内容的高层接口，在Python 3中，urllib被分解为urllib.request, urllib.parse和urllib.error，内置的urlopen()函数类似于内置函数open()，但是只能打开URL读数据，不能是用seek操作。
'''

# 几个高层接口

# urllib.urlopen(url[, data[, proxies[, context]]])
'''
如果没有制定scheme或者scheme是file:，urlopen()会打开本地文件，否则会从网络上打开一个socket连接，返回一个类似于file的对象，返回的对象支持这些方法：read()/readline()/readlines()/fileno()/close()/info()/getcode()/geturl()，除了info()/getcode()/geturl()，其它方法和file对象的接口相同，同时也支持迭代器操作。需要注意的是，对于read()方法，如果没有size参数或者size是负数，可能不会读取到数据流的末尾，目前并没有很好的方法用来确定一个socket的数据流读完了。

info() 返回mimetools.Message类的实例，对于HTTP地址，它包含了与URL关联的元数据，例如Content-Type和Content-Length，对于本地文件，它包含文件的最后修改时间等信息。

geturl() 这个页面的真实URL，urlopen()透明的处理重定向，geturl()会返回重定向后的URL。

getcode() 返回HTTP状态码，如果不是HTTP就返回None

对于HTTP，默认是GET请求，如果是POST请求，需要指定data，data必须是标准的application/x-www-form-urlencoded格式，可以参考urlencode()函数。

urlopen()默认支持不需要认证的代理，在Unix或Windows系统上，它会使用http_proxy或ftp_proxy环境变量的值，no_proxy环境变量可用于指定不使用代理的域名，目前不支持需要认证的代理。

对于Windows系统，如果没有设置代理环境变量，urlopen()会从注册表的Internet Setttings部分读取代理设置。

对于Mac OS X，urlopen()会读取系统的网络设置里读取代理信息。

proxies参数可用于显式指定代理，参数必须是一个协议名字：代理URL的字典，空字典表示不使用代理，None表示是用系统代理设置，默认是None。

例子：

# Use http://www.someproxy.com:3128 for http proxying
proxies = {'http': 'http://www.someproxy.com:3128'}
filehandle = urllib.urlopen(some_url, proxies=proxies)
# Don't use any proxies
filehandle = urllib.urlopen(some_url, proxies={})
# Use proxies from environment - both versions are equivalent
filehandle = urllib.urlopen(some_url, proxies=None)
filehandle = urllib.urlopen(some_url)

context参数可以设置为一个ssl.SSLContext对象，修改SSL配置选项。这个是2.7版增加的方法。

'''

# urllib.urlretrieve(url[, filename[, reporthook[, data]]])
'''
下载URL对应的网络数据到一个本地文件，返回一个元组(filename, headers)，filename是本地文件名，headers是info()方法返回的数据，内部使用的是urlopen()，异常也相同。

第二个参数filename是可选的，用于指定存储URL对应网络数据的文件路径，如果没有指定filename参数，会生成一个临时文件。

第三个参数用于指定一个hook函数，在网络连接建立的时候会被调用一次，每读完一块数据会被调用一次，会传递三个参数(blocksCount, blockSize, totalSize).

对于HTTP请求，data参数用于指定POST数据，格式同urlopen()。

'''

# urllib._urlopener
# 这个是urlopen()和urlretrieve()创建URLopener对象时使用的公用函数，可以是用它来定制一些参数，例如：
'''
import urllib
class AppURLopener(urllib.FancyURLopener):
    version = "App/1.7"
urllib._urlopener = AppURLopener()
'''

# urllib.urlcleanup()
# 清空前一次urlretrievve()调用产生的缓存


# 几个工具函数

# urllib.quote(string[, safe])
# 对字符编码，safe参数指定不需要编码的字符，'/'默认不会被编码，一般用于编码URL的path部分
print urllib.quote('/~me/profile')
# out:'/%7Eme/profile'
print urllib.quote('/~user/哇哈哈/profile')
# out: '/%7Euser/%CD%DB%B9%FE%B9%FE/profile'
print urllib.quote('/~user/some one/profile')
# out:'/%7Euser/some%20one/profile'

# urllib.quote_plus(string[, safe])
# 类似于quote()，但是会把空格替换为+号，而且'/'也会被编码，一般用于编码URL的query参数
print urllib.quote_plus('/~user/some one/profile')
# out: '%2F%7Euser%2Fsome+one%2Fprofile'

# 这两个是对应的解码函数
# urllib.unquote(string)
# urllib.unquote_plus(string)

# urllib.urlencode(query[, doseq])
# 将一个字典对象或二元组序列转换为百分号编码字符串，符合urlopen()中data参数的要求，可用于传递一个form参数字典给POST请求，返回的字符串是以&分割的key=value对，key和value都是是用quote_plus()编码的，当使用二元组序列时，元组的第一个元素作为key，第二个作为value。urlparse模块提供了两个函数parse_qs()和parse_qsl()，用于将query字符串解析为Python数据结构。

# urllib.pathname2url(path)
# 将本地路径转换为合法的URL的path部分，返回值是是用quote()编码过的。
print urllib.pathname2url('C://Users/python/Documents')
# out: '///C:///Users/python/Documents'
print urllib.pathname2url('/usr/local/share/doc/python.html')
# out: '/usr/local/share/doc/python.html'

# urllib.url2pathname(path)
# 将URL的path部分转换为本地路径
print urllib.url2pathname('///C:///Users/python/Documents')
# out: 'C:\\Users\\python\\Documents'

# urllib.getproxies()
# 返回一个代理列表的字典，会从系统读取代理设置


# URLopener对象
# class urllib.URLopener([proxies[, context[, **x509]]])
'''
用于打开URL并读取数据的基类，除非你要支持http/ftp/file以外的协议，一般情况都应该使用FancyURLopener。
默认情况下，URLopener发送urllib/version这样的User-Agent，应用可以在URLopener的子类中修改version属性来改变它。
可选的proxies参数是一个代理和域名关系的映射，一个空字典表示完全不使用代理，默认是None，表示使用系统代理。

context参数必须是一个ssl.SSLContext对象，可以使用它提供一些SSL配置参数，用于HTTPS连接。

其它的参数都放在x509中，可被用于HTTPS的客户端认证，key_file和cert_file用于提供SSL的key和certificate。

open(fullurl[, data])
使用合适的协议打开完整的URL，可以指定缓存和代理信息，data参数的含义同urlopen()
open_unknown(fullurl[, data])
用户可以在子类中定义未知类型URL的打开方式
retrieve(url[, filename[, reporthook[, data]]])
抓取URL的数据并存入文件中，如果URL是远程地址并且没有提供filename，会生成一个临时文件名。

'''

# class urllib.FancyURLopener(...)
'''
FancyURLopener是URLopener的之类，提供HTTP协议的一些默认处理。对于30x的状态码，可以从Location中获取到真实URL；对于401状态码，使用默认的Basic认证。对于其它的状态码，方法http_error_default()会被调用，你可以在子类中重写这个方法提供合适的错误处理。
注意：按照RFC2616的规定，如果POST请求遇到301和302，不能未经用户确认就自动重定向。
构造函数的参数和URLopener相同。
提示：当进行Basic认证时，prompt_user_passwd()方法会被调用，默认实现是让用户在可控的终端中输入需要的信息。可以在子类中提供更合适的行为。
'''

# urllib的限制
'''
1. 目前只支持HTTP/FTP/FILE三种协议
2. urlretrieve不支持缓存
3. 不支持查询一个特定的URL是否在缓存中
4. 如果指向本地文件的URL无法打开，会尝试用FTP协议重试
5. 等待网络连接建立的时候，urlopen()和urlretrieve()可能会导致不确定的长时间延迟，使用这些函数不适合用来构建交互式的Web客户端
6. urlopen()和urlretrieve()返回的服务端返回的原始数据，可能是二进制数据、文本数据或者HTML，HTTP协议在Content-Type中提供了类型信息，如果是HTML，可以使用htmllib解析
7. 处理FTP协议时存在不少问题，建议使用ftplib或者继承FancyURLopener自己处理
8. 不支持需要认证的代理
9. 操作URL字符串建议使用urlparse
'''

# 简单的示例

# HTTP GET
params = urllib.urlencode(
    {"key1": 123, "value": "98%", "verion": "1.0.1-beta"})
# out: verion=1.0.1-beta&key1=123&value=98%25
f = urllib.urlopen("https://api.douban.com/v2/user/1000001?%s" % params)
# print f.read()

# HTTP POST
f = urllib.urlopen("https://api.douban.com/v2/user/1000001?%s", params)
print f.getcode(), '\n', f.info()
'''
output:
400
Server: nginx
Date: Fri, 17 Jul 2015 00:26:51 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 71
Connection: close
Expires: -1
'''
