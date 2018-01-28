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


https://www.douban.com/doulist/3982978/






相册
http://www.douban.com/doulist/33731831/

豆瓣小组

http://www.douban.com/group/meituikong/
http://www.douban.com/group/haixiuzu/



'''

DOULIST_IDS = [u'39822487', u'41021833', u'39612960', u'2769298', u'3646098', u'3646108', u'4418139', u'38511005', u'41089196', u'6434058', u'1826325', u'12053706', u'2976304', u'3290619', u'40852721', u'3233612', u'1884644', u'2776548', u'40465901', u'40712576', u'40849138', u'36462621', u'1867090', u'3233612', u'4006461', u'41160111', u'41501314', u'40712576', u'40465901', u'2776548', u'1884644', u'38192986', u'1867090', u'3558429', u'40740385', u'3984778', u'14092210', u'4170185', u'3327085', u'3521192', u'2776548', u'36721277', u'13181538', u'13684390', u'4290193', u'40756835', u'40325606', u'4169222', u'3409812', u'14138152', u'4147044', u'36391321', u'40237608', u'4239656', u'2803429', u'13717556', u'13723323', u'18777404', u'3571124', u'39274966', u'4206757', u'11795671', u'3558429', u'2762341', u'1896370', u'4169222', u'2803041', u'2999084', u'19092210', u'3603887', u'13717559', u'37417823', u'2571839', u'2803041', u'37200578', u'1888895', u'1906992', u'14046196', u'33636911', u'2002106', u'19794721', u'3622313', u'13020339', u'39475640', u'1990842', u'1869091', u'1884895', u'1869134', u'2568148', u'1890399', u'3289084', u'2419805', u'1888616', u'4292880', u'3062780', u'3489104', u'3188077', u'3073218', u'2997232', u'40459637', u'3080545', u'3913534', u'1800924', u'23671721', u'38623244', u'39645853', u'1793336', u'1896370', u'2611165', u'2797756', u'3924757', u'13717581', u'38621746', u'1934496', u'2618868', u'3432185', u'3036381', u'1896370', u'2803041', u'2083011', u'37961129', u'2635313', u'3536420', u'36833544', u'4133474', u'3029642', u'31681919', u'2583736', u'1785338', u'2944598', u'1969549', u'1908841', u'3102807', u'37801076', u'2814474', u'3390308', u'1822805', u'14138543', u'1865114', u'1932871', u'39646388', u'40655378', u'1970049', u'2890981', u'3390221', u'1798107', u'33731831']

NEW_IDS = ['4138613', '1901061', '40830789', '42995211', '40333572', '44133259', '40830039', '42393057', '42278818', '44049149', '3491616']

def main():
    print(len(DOULIST_IDS))

if __name__ == '__main__':
    main()