# !/usr/bin/python3
# -*-coding:utf-8-*-
# Author: Liang Ma
# CreatedDate: 2021/1/5 11:27
# Description:

import time
import requests


def verify(arg):
    time.sleep(3)
    r = requests.get(arg)
    return {'url': arg, 'json': r.json()}
