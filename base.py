#!/usr/bin/env python
# -*- coding: utf-8 -*-
##必须加上面一行，否则中文注释报错

'''
    @file base.py
    @author bingbo(zhangbingbinge@126.com)
    @date 2015/11/03 17:51:23
    @brief based something 
   
'''

import json
import MySQLdb as mdb
from config import db

__all__ = [
    'BaseController' 
]

class BaseController:
    '控制器基类'

    #请求参数
    _request = None

    def __init__(self, request):
        '构造函数，初始化request'
        self._request = request


class SqlClient:
    '操作数据库蕨类'

    __conn = None
    __cursor = None

    def __init__(self):
        '构造函数，初始化工作'
        self.__conn = mdb.connect(db['host'],db['username'],db['password'],db['database'],db['port'])
        self.__cursor = self.__conn.cursor()
        
    def _select(self, table, fields, conds = None, appends = None):
        '查询数据'
        query = 'select %s from %s' % (', '.join(fields), table)
        if conds:
            query = query + ' where ' + 'and '.join(conds)
        if appends:
            query = query + ' ' + ' '.join(appends)

        return self._execute(query)

    def _execute(self, sql):
        '原生执行sql'
        self.__cursor.execute(sql)
        rows  = self.__cursor.fetchall()
        return rows
