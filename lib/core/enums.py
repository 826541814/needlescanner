# !/usr/bin/python3
# -*-coding:utf-8-*-
# Author: Liang Ma
# CreatedDate: 2021/1/5 15:32
# Description:

from lib.core.datatype import AttribDict


class LOGGING_LEVELS:
    NOTSET = 0
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class CUSTOM_LOGGING:
    SYSINFO = 21
    SUCCESS = 22
    ERROR = 23
    WARNING = 24


class OUTPUT_STATUS:
    SUCCESS = 1
    FAILED = 0


class HTTP_HEADER:
    ACCEPT = "Accept"
    ACCEPT_CHARSET = "Accept-Charset"
    ACCEPT_ENCODING = "Accept-Encoding"



