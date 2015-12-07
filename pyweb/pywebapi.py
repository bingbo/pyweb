#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    @file pywebapi.py
    @author bingbo(zhangbingbinge@126.com)
    @date 2015/11/05 11:57:00
    @brief pyweb 上下文信息接口
'''
import Cookie, urlparse, urllib

from utils import Map, ThreadMap
__all__ = [
    'config',
    'context',
    'header'
    'cookie',
    'setCookie'

]

config = Map()
config.__doc__ = '''
A configuration object for various aspects of pyweb
'''

context = ThreadMap()
context.__doc__ = '''
A `Map` object containing various information about the request:
`server` (k,v)
    : A dictionary containing the standard server environment variables.
`host`
`remote_ip`
`method`
`path`
`query`
`headers`
    : A list of 2-tuples to be used in the response.
`output`
'''

def header(head, value, unique = False):
    '''添加http响应头'''
    if unique is True:
        for h, v in context.headers:
            if h.lower() == head.lower():
                return
    context.headers.append((head, value))

def cookie():
    '''获取所有cookie信息'''
    http_cookie = context.server.get('HTTP_COOKIE', '')
    cookie = Cookie.SimpleCookie()
    cookie.load(http_cookie)
    cookies = dict([(k, urllib.unquote(v.value)) for k, v in cookie.iteritems()])
    return cookies

def setCookie(name, value, expires = '', domain = None, secure = False, httponly = False, path =
        None):
    '''设置一个cookie'''
    morsel = Cookie.Morsel()
    morsel.set(name, value, urllib.quote(value))
    if expires < 0:
        expires = -1000000000
    morsel['expires'] = expires
    morsel['path'] = path or context.homepath + '/'
    if domain:
        morsel['domain'] = domain
    if secure:
        morsel['secure'] = secure
    value = morsel.OutputString()
    if httponly:
        value += '; httponly'
    header('Set-Cookie', value)


