#!/usr/bin/env python
# -*- coding: utf-8 -*-
##必须加上面一行，否则中文注释报错

'''
    @file User.py
    @author zhangbingbing(com@baidu.com)
    @date 2015/11/03 17:51:23
    @brief 
   
'''

__all__ = [
    'User' 
]

class User:
    '用户信息实体类'

    __name = ''
    __password = ''
    __email = ''

    version = '1.0'

    def __init__(self, name, password, email):
        '构造函数初始化'
        self.__name = name
        self.__password = password
        self.__email = email

    def sayHi(self):
        'test'
        print 'hello,' , self.__name





















