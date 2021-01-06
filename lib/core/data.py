# !/usr/bin/python3
# -*-coding:utf-8-*-
# Author: Liang Ma
# CreatedDate: 2021/1/5 15:36
# Description:

from lib.core.datatype import AttribDict
from lib.core.log import LOGGER

logger = LOGGER

conf = AttribDict()

# Dictionary storing
# (1)targets, (2)registeredPocs, (3)bruteMode
# (4)results, (5)pocFiles
# (6)multiThreadMode \ threadContinue \ threadException
kb = AttribDict()

cmd_line_options = AttribDict()

merged_options = AttribDict()

paths = AttribDict()