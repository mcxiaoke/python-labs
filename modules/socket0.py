#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-07-13 21:50:29


# socket协议簇
socket.AF_UNIX
socket.AF_INET
socket.AF_INET6

# 流类型
socket.SOCK_STREAM
socket.SOCK_DGRAM

# 打开socket连接
# socket.create_connection(address[, timeout[, source_address]])
# 如果host是主机名，会尝试解析为IPv4或IPv6地址
# source_address如果提供的话，必须是一个二元组(host, port)

# 解析socket五元组
# socket.getaddrinfo(host, port[, family[, socktype[, proto[, flags]]]])
# 解析为(family, socktype, proto, canonname, sockaddr)
# family, socktype, proto都是整数，sockaddr是一个二元组(address, port)
print socket.getaddrinfo("www.python.org", 80, 0, 0, socket.IPPROTO_TCP)
# out: [(2, 0, 6, '', ('103.245.222.223', 80))]

# 获取全称域名
print socket.getfqdn('www.douban.com')
# out:'32.4.147.211.in-addr.arpa'
print socket.getfqdn('www.python.org')
# out:'223.222.245.103.in-addr.arpa'

# 获取域名的IP地址
print socket.gethostbyname('www.douban.com')
# out:'211.147.4.49'
print socket.gethostbyname('www.python.org')
# out:'103.245.222.223'

# 获取IP地址扩展版
print socket.gethostbyname_ex('douban.com')
# out:('douban.com', [], ['211.147.4.32', '211.147.4.31', '211.147.4.49'])
print socket.gethostbyname_ex('baidu.com')
# out:('baidu.com', [], ['220.181.57.217', '123.125.114.144',
# '180.149.132.47'])

# 获取当前机器的主机名
print socket.gethostname()
# 获取当前机器的IP地址
print socket.gethostbyname(socket.gethostname())

# 获取主机地址
# socket.gethostbyaddr(ip_address)
# 返回三元组(hostname, aliaslist, ipaddrlist)

# 解析socket地址
# print socket.getnameinfo(sockaddr, flags)

# 获取协议类型
print socket.getprotobyname('icmp')  # 1
print socket.getprotobyname('tcp')  # 6

# 创建一个socket
# socket.socket([family[, type[, proto]]])

# 字节序转换
# n=network,l=local,l=long,s=short
# socket.ntohl(x) #32位，网络序转换为主机序
# socket.ntohs(x) #16位，网络序转换为主机序
# socket.htonl(x) #32位，主机序转换为网络序
# socket.htons(x) #16位，主机序转换为网络序

# IPv4地址转换为4字节二进制
# socket.inet_aton('192.168.1.1')

# 二进制地址转换为IPv4格式
# socket.inet_ntoa(packad_ip)

# socket对象的方法
# socket.accept() #接受一个连接
# socket.bind(address) #绑定到地址
# socket.close() #关闭socket连接
# socket.connect(address) #连接远程的socket
# socket.connect_ex(address) #同上，但是不抛异常
# socket.fileno() #返回文件描述符
# socket.getpeername() #获取远程socket的地址
# socket.getsockname() # 获取当前socket的地址
# socket.listen(backlog) #等待连接
# socket.makefile(mode,buffersize) #返回socket关联的file对象
# socket.recv(bufsize[, flags])  #从socket读取数据，返回字符串
# socket.recvfrom(bufsize[, flags]) #从socket读取数据，返回(string,address)
# 读取数据，写入到buffer，返回值是(nbytes, address)
# socket.recvfrom_into(buffer[, nbytes[, flags]])
# 读取最多n字节的数据写入到buffer
# socket.recv_into(buffer[, nbytes[, flags]])
# socket.send(string[, flags]) #发送数据
# socket.sendall(string[, flags]) #发送全部数据
# 发送数据给未连接的socket
# socket.sendto(string, address)
# socket.sendto(string, flags, address)
# 设置阻塞/非阻塞模式
# socket.setblocking(flag)
# 设置阻塞超时
# socket.setblocking(flag)
# s.setblocking(0)等价于s.settimeout(0.0);
# s.setblocking(1)等价于s.settimeout(None).
# socket.setsockopt(level, optname, value)  #设置socket可选参数
# socket.shutdown(how)  #断开连接
# 几个只读属性
# socket.family
# socket.type
# socket.proto
