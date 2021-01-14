# !/usr/bin/python3
# -*-coding:utf-8-*-
# Author: Liang Ma
# CreatedDate: 2021/1/13 10:05
# Description:
import ast

from lib.core.data import logger
from lib.core.enums import CUSTOM_LOGGING


def str_to_dict(value):
    try:
        if value:
            return ast.literal_eval(value)
        else:
            return {}
    except ValueError as e:
        logger.log(CUSTOM_LOGGING.ERROR, "conv string failed : {}".format(str(e)))
