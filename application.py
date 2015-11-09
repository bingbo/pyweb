#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urlparse

import pywebapi as pyweb
import utils
import webserver
import controller


__all__ = [
    'Application'
]

class Application:
    '''
    框架应用入口
    '''

    def run(self):
        '''启动应用框架'''
        utils.ThreadMap.clear_all()
        server = webserver.HttpServer(self.handle)
        server.run()

    def load(self, cxt):
        '''应用框架的初始化工作'''
        pyweb.context.clear()
        #初始化响应头信息
        pyweb.context.headers = [
            ('Proxy-Connection', 'Keep-Alive'), 
            ('Connection', 'Keep-Alive'),
            ('Keep-Alive', 'max=5, timeout=120'),
            ('Via', '1.1 JA-ISA02'),
            ('Date', 'Fri, 18 May 2022 09:05:56 GMT'), 
            ('Server', 'nginx version 2.6'),
            ('Cache-Control', 'max-age=3600'),
            ('Last-Modified', 'Fri, 18 May 2015 09:05:56 GMT'), 
            ('ETag', 'v2.6')
        ]
        #整理环境变量
        pyweb.context.server = {
            'HTTP_HOST':'',
            'HTTP_PROTOCOL': cxt['req_protocol'],
            'RESPONSE_PROTOCOL': cxt['res_protocol'],
            'REMOTE_ADDR': cxt['remote_addr'],
            'REMOTE_PORT': cxt['remote_port'],
            'SERVER_NAME': cxt['server_name'],
            'SERVER_ADDR': cxt['server_addr'],
            'SERVER_PORT': cxt['server_port'],
            'REQUEST_METHOD': cxt['method'],
            'PATH_INFO': cxt['path'],
            'SERVER_SOFTWARE': cxt['software'],
            'REQUEST_URI': cxt['uri'],
            'QUERY_STRING':cxt['querystring'],
        }
        #处理请求参数数据
        pyweb.context.request = {}
        if cxt['body']:
            params = urlparse.parse_qs(cxt['body'])
        elif cxt['querystring']:
            params = urlparse.parse_qs(cxt['querystring'])
        else:
            params = {}

        pyweb.context.request[cxt['method']] = {}
        for k in params.keys():
            if len(params[k]) > 1:
                pyweb.context.request[cxt['method']][k] = params[k]
            else:
                pyweb.context.request[cxt['method']][k] = params[k][0]

        #解析controller,action
        if cxt['path'] == '/':
            pyweb.context.controller = 'Index'
            pyweb.context.action = 'index'
        else:
            arr = cxt['path'][1:].split('/')
            if len(arr) == 1:
                pyweb.context.controller = arr[0].title()
                pyweb.context.action = 'index'
            else:
                pyweb.context.controller = arr[0].title()
                pyweb.context.action = arr[1]

        


    def handle(self, context, resp_fun):
        '''处理请求'''
        self.load(context)
        cls = getattr(controller,pyweb.context.controller)
        method = getattr(cls(pyweb.context.request), pyweb.context.action)
        data = method()
        pyweb.header('Content-Type','text/json')
        pyweb.header('Content-Length',str(len(data)))
        resp_fun('HTTP/1.1 200 OK', pyweb.context.headers, data)



