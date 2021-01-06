# !/usr/bin/python3
# -*-coding:utf-8-*-
# Author: Liang Ma
# CreatedDate: 2021/1/5 11:37
# Description:

from collections import OrderedDict


class AttribDict(OrderedDict):
    """
    AttribDict 扩展了 Orderedict 以提供属性访问。
    以 _ 或 _OrderedDict__ 开头的项目不能作为属性访问。
    """
    __exclued_keys__ = set()

    def __getattr__(self, key):
        if key.startswith('__') or key.startswith('_OrderedDict__') or key in self.__exclued_keys__:
            return super(AttribDict, self).__getattribute__(key)
        else:
            try:
                return self[key]
            except KeyError:
                raise AttributeError(key)

    def __setattr__(self, key, value):
        if key.startswith('__') or key.startswith('_OrderedDict__') or key in self.__exclued_keys__:
            return super(AttribDict, self).__setattr__(name, value)
        else:
            self[key] = value
