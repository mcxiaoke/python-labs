#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mcxiaoke
# @Date:   2015-08-05 23:12:15

if __name__ == '__main__':
    print "design document"

'''

饭否消息备份流程图

A. 备份消息
1. 如果没有token, 登录获取token，持久化保存
2. 读取token，获取user信息，获取statusesCount
3. 根据user_id查询数据库，有数据则读取最新的一条的status_id
4. 根据status_id从api批量读取数据，读取完后JSON写入数据
5. 循环执行，重复步骤四，直到全部获取完成
6. 遇到错误时从数据库读取，然后从步骤三重新开始执行步骤4

B. 备份图片
1. 从数据库读取消息，逐个下载图片，更新图片下载字段

C. 其它事项
1. 每次更新数据都记录LOG
2. 图片下载也记录LOG

'''

'''
饭否消息导出流程图

支持的导出格式为:
1. 模板生成，简单的HTML格式
2. 模板生成，简单的Markdown格式
3. 根据HTML和Markdown导出其它格式
'''
