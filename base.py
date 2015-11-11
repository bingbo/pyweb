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


