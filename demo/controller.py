#!/usr/bin/env python
# -*- coding: utf-8 -*-
##必须加上面一行，否则中文注释报错

'''
    @file controller.py
    @author zhangbingbing
    @date 2015/11/03 17:51:23
    @brief 
   
'''

import json

from pyweb import base

import service

__all__ = [
    'User' 
]

class User(base.BaseController):
    '用户信息控制器类'

    #userService实例

    #__userService = None

    #def __init__(self,request):
    #    '构造函数，初始化service实例'
    #    self.__userService = service.User()
    #    self.__request = request

    def get(self):
        '获取用户信息'

        self.__userService = service.User()
        user = self.__userService.getUserById(self._request['GET']['id'])
        return json.dumps(user)

    def list(self):
        '获取用户列表'

        self.__userService = service.User()
        users = self.__userService.getUserList()
        return json.dumps(users)

    def update(self):
        '更新用户'
        self.__userService = service.User()
        result = self.__userService.updateUserById(self._request['GET'])
        return json.dumps(result)

    def delete(self):
        '删除用户'
        self.__userService = service.User()
        result = self.__userService.deleteUserById(self._request['GET']['id'])
        return json.dumps(result)

    def add(self):
        '添加用户'
        self.__userService = service.User()
        result = self.__userService.addUser(self._request['GET'])
        return json.dumps(result)


