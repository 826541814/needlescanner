# !/usr/bin/python3
# -*-coding:utf-8-*-
# Author: Liang Ma
# CreatedDate: 2021/1/5 20:59
# Description:

import ssl


def remove_ssl_verify():
    ssl._create_default_https_context = ssl._create_unverified_context
