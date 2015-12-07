#!/usr/bin/env python
# -*- coding: utf-8 -*-
##必须加上面一行，否则中文注释报错

'''
    @file service.py
    @author zhangbingbing(com@baidu.com)
    @date 2015/11/03 17:51:23
    @brief 
   
'''

import dao

__all__ = ['User']
class User:
    '用户信息service类'

    __userDao = None


    def __init__(self):
        '构造函数初始化'
        self.__userDao = dao.User()

    def getUserById(self, id = 0):
        '根据用户ID获取用户信息'
        conds = [('id = ',id)]
        user = self.__userDao.getUser(conds)
        return user

    def getUserList(self):
        '获取用户信息列表'
        appends = ['order by id desc']
        users = self.__userDao.getUsers(None, appends)
        return users;

    def updateUserById(self, params):
        '更新用户信息'
        conds = [('id = ',params['id'])]
        rows = [('name', "'"+params['name']+"'")]
        result = self.__userDao.updateUser(rows, conds)
        return result;
    
    def deleteUserById(self, id):
        '删除用户'
        conds = [('id = ',id)]
        result = self.__userDao.deleteUser(conds)
        return result

    def addUser(self, params):
        '添加用户'
        user = {
            'id':'',
            'name':params['name']
        }
        result = self.__userDao.addUser(user)
        return result

        




















