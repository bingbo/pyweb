#!/usr/bin/env python
# -*- coding: utf-8 -*-
##必须加上面一行，否则中文注释报错

'''
    @file dao.py
    @author zhangbingbing(com@baidu.com)
    @date 2015/11/03 17:51:23
    @brief 
   
'''
import json
import time 
import MySQLdb as mdb

from pyweb import base


__all__ = [
    'User' 
]

class User(base.SqlClient):
    '用户信息dao类'

    __table = 'user'
    __fields = ['id', 'name']


    def getUsers(self, conds = None, appends = None):
        '获取用户列表'
        rows = self._select(self.__table, self.__fields, conds, appends)
        return rows


    def getUser(self, conds):
        '获取用户'
        rows = self._select(self.__table, self.__fields, conds)
        return rows[0]

    def updateUser(self, data, conds):
        '更新用户'
        result = self._update(self.__table, data, conds)
        return result

    def deleteUser(self, conds):
        '删除用户'
        result = self._delete(self.__table, conds)
        return result

    def addUser(self, data):
        '添加用户'
        result = self._insert(self.__table, self.__fields, data)
        return result



















