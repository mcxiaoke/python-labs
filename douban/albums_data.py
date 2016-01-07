#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-24 21:54:32


'''
相册API

获取相册    GET http://api.douban.com/v2/album/:id
获取相册图片列表    GET http://api.douban.com/v2/album/:id/photos
获得照片    GET http://api.douban.com/v2/photo/:id
照片回复列表  GET http://api.douban.com/v2/photo/:id/comments
获得照片单条回复    GET http://api.douban.com/v2/photo/:id/comment/:id
创建相册    POST    http://api.douban.com/v2/albums
更新相册    POST    http://api.douban.com/v2/album/:id
删除相册    DELETE  http://api.douban.com/v2/album/:id
喜欢相册    POST    http://api.douban.com/v2/album/:id/like
取消喜欢相册  DELETE  http://api.douban.com/v2/album/:id/like
上传照片    POST    http://api.douban.com/v2/album/:id
发送广播    POST    http://api.douban.com/v2/album/:id/miniblog
更新照片    PUT http://api.douban.com/v2/photo/:id
删除照片    DELETE  http://api.douban.com/v2/photo/:id
喜欢照片    POST    http://api.douban.com/v2/photo/:id/like
取消喜欢照片  DELETE  http://api.douban.com/v2/photo/:id/like
回复照片    POST    http://api.douban.com/v2/photo/:id/comment
删除单条回复  DELETE  http://api.douban.com/v2/photo/:id/comment/:id
获得用户相册列表    GET http://api.douban.com/v2/album/user_created/:id
获得用户喜欢的相册列表 GET http://api.douban.com/v2/album/user_liked/:id
获得用户最新上传的照片 GET http://api.douban.com/v2/photo/user_created/:id

获得Album的Photo列表
GET http://api.douban.com/v2/album/:id/photos
参数  意义  备注
start   起始  从0开始，默认为0
count   数量
order   排序  asc, desc, 默认为相册本身的排序
sortby  排序方式    time 上传时间，vote 推荐数，comment 回复数，默认为time
pos 包含位置信息  默认为false

'''

'''
从豆列提取相册列表，然后按相册下载

http://www.douban.com/doulist/39822487/?sort=time&sub_type=12
http://www.douban.com/doulist/41021833/?sort=time&sub_type=12
http://www.douban.com/doulist/39612960/?sort=time&sub_type=12
http://www.douban.com/doulist/2769298/?sort=time&sub_type=12
http://www.douban.com/doulist/3646098/?sort=time&sub_type=12
http://www.douban.com/doulist/3646108/?sort=time&sub_type=12
http://www.douban.com/doulist/4418139/?sort=time&sub_type=12
http://www.douban.com/doulist/38511005/?sort=time&sub_type=12
http://www.douban.com/doulist/41089196/?sort=time&sub_type=12
http://www.douban.com/doulist/6434058/?sort=time&sub_type=12
http://www.douban.com/doulist/1826325/?sort=time&sub_type=12
http://www.douban.com/doulist/12053706/?sort=time&sub_type=12
http://www.douban.com/doulist/2976304/?sort=time&sub_type=12
http://www.douban.com/doulist/3290619/?sort=time&sub_type=12
http://www.douban.com/doulist/40852721/?sort=time&sub_type=12
http://www.douban.com/doulist/3233612/?sort=time&sub_type=12
http://www.douban.com/doulist/1884644/?sort=time&sub_type=12
http://www.douban.com/doulist/2776548/?sort=time&sub_type=12
http://www.douban.com/doulist/40465901/?sort=time&sub_type=12
http://www.douban.com/doulist/40712576/?sort=time&sub_type=12
http://www.douban.com/doulist/40849138/?sort=time&sub_type=12
http://www.douban.com/doulist/36462621/?sort=time&sub_type=12
http://www.douban.com/doulist/1867090/?sort=time&sub_type=12
http://www.douban.com/doulist/3233612/?sort=time&sub_type=12
http://www.douban.com/doulist/4006461/?sort=time&sub_type=12
http://www.douban.com/doulist/41160111/?sort=time&sub_type=12
http://www.douban.com/doulist/41501314/?sort=time&sub_type=12
http://www.douban.com/doulist/40712576/?sort=time&sub_type=12
http://www.douban.com/doulist/40465901/?sort=time&sub_type=12
http://www.douban.com/doulist/2776548/?sort=time&sub_type=12
http://www.douban.com/doulist/1884644/?sort=time&sub_type=12
http://www.douban.com/doulist/38192986/?sort=time&sub_type=12
http://www.douban.com/doulist/1867090/?sort=time&sub_type=12
http://www.douban.com/doulist/3558429/?sort=time&sub_type=12
http://www.douban.com/doulist/40740385/?sort=time&sub_type=12
http://www.douban.com/doulist/3984778/?sort=time&sub_type=12
http://www.douban.com/doulist/14092210/?sort=time&sub_type=12
http://www.douban.com/doulist/4170185/?sort=time&sub_type=12
http://www.douban.com/doulist/3327085/?sort=seq&sub_type=12
http://www.douban.com/doulist/3521192/?sort=time&sub_type=12
http://www.douban.com/doulist/2776548/?sort=seq&sub_type=12
http://www.douban.com/doulist/36721277/
http://www.douban.com/doulist/13181538/
http://www.douban.com/doulist/13684390/
http://www.douban.com/doulist/4290193/
http://www.douban.com/doulist/40756835/
http://www.douban.com/doulist/40325606/
http://www.douban.com/doulist/4169222/
http://www.douban.com/doulist/3409812/
http://www.douban.com/doulist/14138152/
http://www.douban.com/doulist/4147044/
http://www.douban.com/doulist/36391321/
http://www.douban.com/doulist/40237608/
http://www.douban.com/doulist/4239656/
http://www.douban.com/doulist/2803429/
http://www.douban.com/doulist/13717556/
http://www.douban.com/doulist/13723323/
http://www.douban.com/doulist/18777404/
http://www.douban.com/doulist/3571124/
http://www.douban.com/doulist/39274966/?sort=time&sub_type=12
http://www.douban.com/doulist/4206757/
http://www.douban.com/doulist/11795671/
http://www.douban.com/doulist/3558429/?sort=time&sub_type=12
http://www.douban.com/doulist/2762341/?sort=time&sub_type=12
http://www.douban.com/doulist/1896370/?sort=time&sub_type=12
http://www.douban.com/doulist/4169222/?sort=time&sub_type=12
http://www.douban.com/doulist/2803041/


http://www.douban.com/doulist/2999084/
http://www.douban.com/doulist/19092210/
http://www.douban.com/doulist/3603887/
http://www.douban.com/doulist/13717559/
http://www.douban.com/doulist/37417823/
http://www.douban.com/doulist/2571839/
http://www.douban.com/doulist/2803041/
http://www.douban.com/doulist/37200578/
http://www.douban.com/doulist/1888895/
http://www.douban.com/doulist/1906992/
http://www.douban.com/doulist/14046196/
http://www.douban.com/doulist/33636911/
http://www.douban.com/doulist/2002106/
http://www.douban.com/doulist/19794721/
http://www.douban.com/doulist/3622313/
http://www.douban.com/doulist/13020339/
http://www.douban.com/doulist/39475640/
http://www.douban.com/doulist/1990842/
http://www.douban.com/doulist/1869091/
http://www.douban.com/doulist/1884895/
http://www.douban.com/doulist/1869134/
http://www.douban.com/doulist/2568148/
http://www.douban.com/doulist/1890399/
http://www.douban.com/doulist/3289084/
http://www.douban.com/doulist/2419805/
http://www.douban.com/doulist/1888616/
http://www.douban.com/doulist/4292880/?sort=time&sub_type=12
http://www.douban.com/doulist/3062780/
http://www.douban.com/doulist/3489104/
http://www.douban.com/doulist/3188077/
http://www.douban.com/doulist/3073218/
http://www.douban.com/doulist/2997232/
http://www.douban.com/doulist/40459637/?sort=time&sub_type=12
http://www.douban.com/doulist/3080545/
http://www.douban.com/doulist/3913534/
http://www.douban.com/doulist/1800924/
http://www.douban.com/doulist/23671721/
http://www.douban.com/doulist/38623244/
http://www.douban.com/doulist/39645853/?sort=time&sub_type=12
http://www.douban.com/doulist/1793336/
http://www.douban.com/doulist/1896370/
http://www.douban.com/doulist/2611165/
http://www.douban.com/doulist/2797756/
http://www.douban.com/doulist/3924757/
http://www.douban.com/doulist/13717581/
http://www.douban.com/doulist/38621746/
http://www.douban.com/doulist/1934496/
http://www.douban.com/doulist/2618868/
http://www.douban.com/doulist/3432185/?sort=time&sub_type=12
http://www.douban.com/doulist/3036381/
http://www.douban.com/doulist/1896370/
http://www.douban.com/doulist/2803041/
http://www.douban.com/doulist/2083011/
http://www.douban.com/doulist/37961129/
http://www.douban.com/doulist/2635313/
http://www.douban.com/doulist/3536420/
http://www.douban.com/doulist/36833544/
http://www.douban.com/doulist/4133474/
http://www.douban.com/doulist/3029642/
http://www.douban.com/doulist/31681919/
http://www.douban.com/doulist/2583736/
http://www.douban.com/doulist/1785338/
http://www.douban.com/doulist/2944598/
http://www.douban.com/doulist/1969549/
http://www.douban.com/doulist/1908841/
http://www.douban.com/doulist/3102807/

http://www.douban.com/doulist/37801076/?sort=time&sub_type=12
http://www.douban.com/doulist/2814474/
http://www.douban.com/doulist/3390308/
http://www.douban.com/doulist/1822805/
http://www.douban.com/doulist/14138543/
http://www.douban.com/doulist/1865114/
http://www.douban.com/doulist/1932871/
http://www.douban.com/doulist/39646388/?sort=time&sub_type=12
http://www.douban.com/doulist/40655378/
http://www.douban.com/doulist/1970049/
http://www.douban.com/doulist/2890981/
http://www.douban.com/doulist/3390221/
http://www.douban.com/doulist/1798107/









相册
http://www.douban.com/doulist/33731831/

豆瓣小组

http://www.douban.com/group/meituikong/
http://www.douban.com/group/haixiuzu/



'''
