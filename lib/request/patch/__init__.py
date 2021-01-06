# !/usr/bin/python3
# -*-coding:utf-8-*-
# Author: Liang Ma
# CreatedDate: 2021/1/5 20:58
# Description:

from .remove_ssl_verify import remove_ssl_verify
from .remove_warings import disable_warnings
from .hook_request import patch_session
from .add_httpraw import patch_addraw
from .hook_request_redirect import patch_redirect


def patch_all():
    remove_ssl_verify()
    disable_warnings()
    patch_session()
    patch_addraw()
    patch_redirect()
