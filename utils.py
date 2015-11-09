#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    @file utils.py
    @author bingbo(zhangbingbinge@126.com)
    @date 2015/11/05 10:42:12
    @brief General Utilities 
'''

__all__ = [
    'Map',
    'ThreadMap'        
]

from threading import local

class Map(dict):
    '''
        A Map object is like a dictionary
    '''

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError, k:
            raise AttributeError, k

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError, k:
            raise AttribteError, k

    def __repr__(self):
        return '<Map ' + dict.__repr__(self) + '>'


class ThreadMap(local):
    '''
    thread local storage
    '''

    _instances = set()

    def __init__(self):
        ThreadMap._instances.add(self)

    def __del__(self):
        ThreadMap._instances.remove(self)

    def __hash__(self):
        return id(self)

    def clear_all():
        '''clear all thread local instance'''
        for t in list(ThreadMap._instances):
            t.clear()

    clear_all = staticmethod(clear_all)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __delitem__(self, key):
        del self.__dict__[key]

    def __contains__(self, key):
        return key in self.__dict__

    has_key = __contains__

    def clear(self):
        self.__dict__.clear()

    def copy(self):
        return  self.__dict__.copy()

    def get(self, key, default = None):
        return self.__dict__.get(key, default)

    def items(self):
        return self.__dict__.items()

    def iteritems(self):
        return self.__dict__iteritems()

    def keys(self):
        return self.__dict__.keys()

    def iterkeys(self):
        return self.__dict__iterkeys()

    iter = iterkeys

    def values(self):
        return self.__dict__.values()

    def itervalues(self):
        return self.__dict__itervalues()

    def pop(self, key, *args):
        return self.__dict__.pop(key, *args)

    def popitem(self):
        return self.__dict__.popitem()

    def setdefault(self, key, default = None):
        return self.__dict__.setdefault(key, default)

    def update(self, *args, **kwargs):
        self.__dict__.update(*args, **kwargs)

    def __repr__(self):
        return '<ThreadMap %r>' % self.__dict__

    __str__ = __repr__



