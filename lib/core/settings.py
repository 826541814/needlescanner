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
MAX_NUMBER_OF_THREADS = 8

CONF = {
    'requests': {
        'timeout': 30,
        'headers': {
            'User-Agent': 'hello needle!'
        }
    }
}
