#!/usr/bin/env python
# -*- coding: utf-8 -*-
##必须加上面一行，否则中文注释报错

'''
    @file webserver.py
    @author bingbo(zhangbingbinge@126.com)
    @date 2015/11/05 10:42:12
    @brief http server relative 
'''
import socket
import threading
import time 
import os
import sys
import json
import urllib
import urlparse

import pywebapi as pyweb
from utils import *

#print sys.path[0]
#print (sys.argv[1],sys.argv[2])
class HttpServer:
    '''web服务器，接收请求，返回响应结果等'''
    
    __server_address = None
    __app_handle = None
    __res_headers = None
    __res_data = None


    def __init__(self, handle = None, server_address = ('0.0.0.0', 8090)):
        '''构造函数，补始化'''
        if(len(sys.argv) == 2):
            server_address = Common.validip(sys.argv[1])
        self.__server_address = server_address
        self.__app_handle = handle

    def run(self):
        '''运行web服务器进行接收请求'''

        try:

            ##初始化soket
            ss=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ss.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            ss.bind(self.__server_address)
            ss.listen(5)


            ##处理请求
            while True:
                print 'waiting for connection...'
                cs, addr = ss.accept()
                print '...connected from:',addr
                
                thread = threading.Thread(target = self.handle, args = (cs, addr))
                thread.start()

            ss.close()

        except Exception ,e:
            print 'catch exception : ',e

    def handle(self, cs, addr):
        '处理一个请求在一个线程里.'

        evn = {}
        reqData = cs.recv(4096)
        reqHeaders = reqData.split('\r\n')

        evn['remote_addr'] = addr[0]
        evn['remote_port'] = addr[1]
        evn['server_name'] = socket.gethostname()
        evn['server_addr'] = socket.gethostbyname(socket.gethostname())
        evn['server_port'] = addr[1]
        evn['software'] = 'webserver 1.0'
        evn['querystring'] = None
        evn['body'] = None


        server = {}
        server['protocol'] = 'HTTP/1.1'
        evn['method'], evn['uri'], evn['req_protocol'] = reqHeaders[0].strip().split(' ',2)
        rp = int(evn['req_protocol'][5]), int(evn['req_protocol'][7])
        sp = int(server['protocol'][5]), int(server['protocol'][7])
        evn['res_protocol'] = 'HTTP/%s.%s' % min(rp, sp)
        for hd in reqHeaders[1:]:
            if hd in ' \t':
                v = hd.strip()
            else:
                try:
                    k, v = hd.split(':',1)
                except Exception as e:
                    print e
                k = k.strip().title()
                v = v.strip()
                evn[k] = v

        evn['scheme'], evn['authority'], evn['path'] = self.parse_request_uri(evn['uri'])
        if '?' in evn['path']:
            evn['path'], evn['querystring'] = evn['path'].split('?', 1)
        if evn['method'] == 'POST' :
            evn['body'] = reqHeaders[-1]

        

        self.__app_handle(evn, self.response)
        res_status, res_header = self.__res_headers
        self.send_response(cs, res_status)
        self.send_headers(cs, res_header)
        self.end_headers(cs)
        self.send_body(cs, self.__res_data)
        cs.close()



    def parse_request_uri(self, uri):
        '''解析请求url'''
        if uri == '*':
            return None, None, uri
        i = uri.find('://')
        if i> 0 and '?' not in uri[:i]:
            scheme, remainder = uri[:i].lower(), uri[i+3]
            authority, path = remainder.split('/',1)
            return scheme, authority, path
        if uri.startswith('/'):
            return None, None, uri
        else:
            return None, uri, None



    def response(self, status, res_header, data):
        '''响应结果'''
        self.__res_headers = (status, res_header)
        self.__res_data = data
        

    def send_response(self, cs, status):
        cs.send(status + '\r\n')
    def send_headers(self, cs, res_headers):
        headers = []
        for k,v in res_headers:
            headers.append(k + ': ' + v)
        rh = '\r\n'.join(headers)
        cs.send(rh.strip())
    def end_headers(self, cs):
        cs.send('\r\n\r\n')

    def send_body(self, cs, data):
        cs.send(data)

