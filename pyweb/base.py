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
    'BaseController',
    'SqlClient'
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
                conds = self.__formatWhere(conds)
                query = query + ' where ' + conds
        if appends:
            query = query + ' ' + ' '.join(appends)

        self._execute(query)
        return self._fetchall()

    def _update(self, table, rows, conds = None):
        '更新数据'
        query = 'update %s set ' % table
        if rows:
            datas = []
            for row in rows:
                datas.append(' = '.join(row))
            query = query + ', '.join(datas)
        if conds:
                conds = self.__formatWhere(conds)
                query = query + ' where ' + conds
        
        self._execute(query);
        return self._getRowCount()

    def _delete(self, table, conds = None):
        '删除数据'
        query = 'delete from %s ' % table
        if conds:
            conds = self.__formatWhere(conds)
            query = query + ' where ' + conds
        self._execute(query)
        return self._getRowCount()

    def _insert(self, table, fields, row):
        '添加数据'
        query = 'insert into %s (%s) values %s' % (table ,', '.join(fields), tuple(row.values()))
        self._execute(query)
        return self._getRowCount()


    def _execute(self, sql):
        '原生执行sql'
        try:
            self.__cursor.execute(sql)
            self.__conn.commit()
        except:
            self.__conn.rollback()

    def _fetchone(self):
        '获取查询结果一行'
        return self.__cursor.fetchone()

    def _fetchall(self):
        '获取查询结果所有行'
        return self.__cursor.fetchall()

    def _getRowCount(self):
        '获取影响的行数'
        return self.__cursor.rowcount

    def __formatWhere(self, conds):
        if conds:
            cds = []
            for cond in conds:
                cds.append(''.join(cond))
            cds = 'and '.join(cds)
            return cds
