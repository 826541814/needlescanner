# !/usr/bin/python3
# -*-coding:utf-8-*-
# Author: Liang Ma
# CreatedDate: 2021/1/5 10:32
# Description:

import os

PATHS_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../')
PATHS_POCS = os.path.join(PATHS_ROOT, 'pocs')
PATHS_OUTPUT = os.path.join(PATHS_ROOT, 'output')
VERSION = 'V0.000001'
POCS = []
# MAX_NUMBER_OF_THREADS = 8

CONF = {
    'retry': 1,
    'pocs': [],
    'threads': 4,
    'requests': {
        'timeout': 30,
        'headers': {
            'User-Agent': 'hello needle!'
        }
    }
}
DEFAULT_LISTENER_PORT = 6666

DEFAULT_USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"
