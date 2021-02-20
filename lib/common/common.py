# !/usr/bin/python3
# -*-coding:utf-8-*-
# Author: Liang Ma
# CreatedDate: 2021/1/12 9:22
# Description:
import os
import re

from lib.core.data import paths


def desensitization(s):
    """
    Hide sensitive information..
    :param s:
    :return:
    """
    s = str(s)
    return s[:len(s) // 4 if len(s) < 30 else 8] + '***' + s[len(s) * 3 // 4:]


def is_needle_poc(poc_string):
    return True if 'POCBase' in poc_string else False


def get_filename(filepath, with_ext=True):
    base_name = os.path.basename(filepath)
    return base_name if with_ext else os.path.splitext(base_name)[0]


def parse_target_url(url):
    """
    Parse target URL
    :param url:
    :return:
    """
    ret = url
    if not re.search('^http[s]*://', ret, re.I) and not re.search("^ws[s]*://", ret, re.I):
        if re.search(':443[/]*$', ret):
            ret = "https://" + ret
        else:
            ret = "http://" + ret
    return ret


def set_paths(root_path):
    """
    Sets absolute paths for project directories and files
    """
    paths.NEEDLE_ROOT_PATH = root_path
    paths.NEEDLE_DATA_PATH = os.path.join(paths.NEEDLE_ROOT_PATH, "data")
    # paths.NEEDLE_PLUGINS_PATH = os.path.join(paths.NEEDLE_ROOT_PATH, "plugins")
    paths.NEEDLE_POCS_PATH = os.path.join(paths.NEEDLE_ROOT_PATH, "pocs")
    paths.USER_POCS_PATH = None

    paths.USER_AGENTS = os.path.join(paths.NEEDLE_DATA_PATH, "user-agents.txt")
    paths.WEAK_PASS = os.path.join(paths.NEEDLE_DATA_PATH, "password-top100.txt")
    paths.LARGE_WEAK_PASS = os.path.join(paths.NEEDLE_DATA_PATH, "password-top1000.txt")

    paths.NEEDLE_HOME_PATH = os.path.expanduser("~")
    _ = os.path.join(paths.NEEDLE_HOME_PATH, ".needle")

    # paths.API_SHELL_HISTORY = os.path.join(_, "api.hst")
    # paths.OS_SHELL_HISTORY = os.path.join(_, "os.hst")
    # paths.SQL_SHELL_HISTORY = os.path.join(_, "sql.hst")
    # paths.NEEDLE_SHELL_HISTORY = os.path.join(_, "needle.hst")
    # paths.NEEDLE_CONSOLE_HISTORY = os.path.join(_, "console.hst")

    paths.NEEDLE_TMP_PATH = os.path.join(_, "tmp")
    # paths.NEEDLE_RC_PATH = os.path.join(paths.NEEDLE_HOME_PATH, ".needlerc")
    paths.NEEDLE_OUTPUT_PATH = paths.get("NEEDLE_OUTPUT_PATH", os.path.join(_, "output"))
    # paths.SHELLCODES_DEV_PATH = os.path.join(paths.NEEDLE_ROOT_PATH, "shellcodes", "tools")
