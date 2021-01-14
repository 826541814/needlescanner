# !/usr/bin/python3
# -*-coding:utf-8-*-
# Author: Liang Ma
# CreatedDate: 2021/1/12 11:25
# Description:
import importlib
from importlib.abc import Loader

from lib.common.common import is_needle_poc, get_filename
from lib.core.data import kb, logger


class PocLoader(Loader):
    def __init__(self, fullname, path):
        self.fullname = fullname
        self.path = path
        self.data = None

    def set_data(self, data):
        self.data = data

    def get_filename(self, fullname):
        return self.path

    def get_data(self, filename: str):
        if filename.startswith('neddle://') and self.data:
            data = self.data
        else:
            with open(filename, encoding='utf-8') as f:
                code = f.read()
                data = code
        return data

    def exec_module(self, module) -> None:
        filename = self.path
        poc_code = self.get_data(filename)
        obj = compile(poc_code, filename, 'exec', dont_inherit=True, optimize=-1)
        exec(obj, module.__dict__)


def load_file_to_module(file_path, module_name=None):
    if '' not in importlib.machinery.SOURCE_SUFFIXES:
        importlib.machinery.SOURCE_SUFFIXES.append('')
    try:
        module_name = 'pocs_{0}'.format(get_filename(file_path, with_ext=False)) if module_name is None else module_name
        spec = importlib.util.spec_from_file_location(module_name, file_path, loader=PocLoader(module_name, file_path))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        poc_model = kb.registered_pocs[module_name]
    except KeyError:
        poc_model = None
    except ImportError:
        error_msg = "load module failed! '{}'".format(file_path)
        logger.error(error_msg)
        raise
    return poc_model


def load_string_to_module(code_string, fullname=None):
    try:
        module_name = 'pocs_{0}'.format(get_md5(code_string)) if fullname is None else fullname
        file_path = 'needle://{0}'.format(module_name)
        poc_loader = PocLoader(module_name, file_path)
        poc_loader.set_data(code_string)
        spec = importlib.util.spec_from_file_location(module_name, file_path, loader=poc_loader)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        poc_model = kb.registered_pocs[module_name]
    except KeyError:
        poc_model = None
    except ImportError:
        error_msg = "load module '{0}' failed!".format(fullname)
        logger.error(error_msg)
        raise
    return poc_model


def register_poc(poc_class):
    module = poc_class.__module__.split('.')[0]
    if module in kb.registered_pocs:
        kb.current_poc = kb.registered_pocs[module]
        return
    kb.registered_pocs[module] = poc_class()
    kb.current_poc = kb.registered_pocs[module]

