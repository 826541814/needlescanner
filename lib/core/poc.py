# !/usr/bin/python3
# -*-coding:utf-8-*-
# Author: Liang Ma
# CreatedDate: 2021/1/11 10:02
# Description:

import re
from collections import OrderedDict
from urllib.error import HTTPError
from urllib.parse import urlparse

from requests import ConnectTimeout, TooManyRedirects

from lib.common.common import parse_target_url
from lib.core.data import logger
from lib.core.enums import POC_CATEGORY, OUTPUT_STATUS, ERROR_TYPE_ID, CUSTOM_LOGGING
from lib.core.exception import NeedleValidationException, NeedleInvalidModeException
from lib.core.settings import CONF
from lib.utils import str_to_dict

conf = CONF


class POCBase(object):
    def __init__(self):
        self.type = None
        self.target = None
        self.headers = None
        self.target_id = None
        self.url = None
        self.mode = None
        self.params = None
        self.verbose = None
        self.expt = (0, 'None')
        self.current_protocol = getattr(self, 'protocol', POC_CATEGORY.PROTOCOL.HTTP)
        self.pocDesc = getattr(self, 'pocDesc', 'Poc的作者啥也没说！')

        # global options init
        self.global_options = OrderedDict()
        if self.current_protocol == POC_CATEGORY.PROTOCOL.HTTP:
            self.global_options['target'] = ''
            self.global_options['referer'] = ''
            self.global_options['agent'] = ''
            self.global_options['proxy'] = ''
            self.global_options['timeout'] = ''
        else:
            self.global_options['rhost'] = ''
            self.global_options['rport'] = ''
            self.global_options['ssl'] = ''

        # payload options for exploit
        self.payload_options = OrderedDict()
        if hasattr(self, '_shell'):
            self.payload_options['lhost'] = ''
            self.payload_options['lport'] = ''

        self.options = OrderedDict()
        # module options init

        if hasattr(self, '_options'):
            self.options.update(self._options)

    def get_options(self):
        tmp = OrderedDict()
        for k, v in self.options.items():
            tmp[k] = v
        for k, v in self.payload_options.items():
            tmp[k] = v
        for k, v in self.global_options.items():
            tmp[k] = v
        # return self.options.update(self.global_options).update(self.payload_options)
        return tmp

    def getg_option(self, name):
        if name not in self.global_options:
            raise NeedleValidationException
        return self.global_options[name]

    def getp_option(self, name):
        if name not in self.payload_options:
            raise NeedleValidationException
        return self.payload_options[name]

    # def get_option(self, name):
    #     if name not in self.options:
    #         raise NeedleValidationException
    #     # 处理options中的payload，将Payload的IP和端口转换
    #     value = self.options[name]
    #     flag = re.search(r'\{0\}.+\{1\}', str(value))
    #     if flag:
    #         value.format(conf.connect_back_host, conf.connect_back_port)
    #     return value

    def get_info(self):
        """
        得到 PoC 的信息，返回dict
        :return:
        """
        fields = ["name", "VulID", "version", "author", "vulDate", "createDate", "updateDate", "references",
                  "appPowerLink", "appName", "appVersion", "vulType", "desc", "pocDesc", "current_protocol"]
        data = {
        }
        for field in fields:
            value = getattr(self, field, None)
            if value:
                data[field] = value
        return data

    def set_options(self, kwargs):
        if hasattr(self, 'options'):
            self.options.update(kwargs)
        else:
            self.options = kwargs

    def set_option(self, key, value):

        if key not in self.options:
            raise NeedleValidationException("No Key " + key)
        self.options[key] = value

    def setg_option(self, key, value):
        if key not in self.global_options:
            raise NeedleValidationException("No Key " + key)
        self.global_options[key] = value

    def setp_option(self, key, value):
        if key not in self.options:
            raise NeedleValidationException("No Key " + key)
        self.payload_options[key] = value

    def check_requirement(self, *args):
        for option in args:
            for key, v in option.items():
                if v.require and v.value == "":
                    raise NeedleValidationException(f'"{key}" must be set, please using command "set {key}"')
        return True

    def build_url(self):
        if self.target:
            pr = urlparse(parse_target_url(self.target))
            rport = pr.port if pr.port else 0
            rhost = pr.hostname
            ssl = False
            if pr.scheme == 'https://':
                ssl = True
            self.setg_option('rport', rport)
            self.setg_option('rhost', rhost)
            self.setg_option('ssl', ssl)
        return parse_target_url(self.target)

    def _execute(self):
        if self.mode == 'verify':
            output = self._verify()
        elif self.mode == 'attack':
            output = self._attack()
        else:
            raise NeedleInvalidModeException
        return output

    def execute(self, target_id=0, target="", headers=None, params=None, mode='verify', verbose=True, **kwargs):
        self.target_id = target_id
        self.target = target
        self.url = parse_target_url(target) if self.current_protocol == POC_CATEGORY.PROTOCOL.HTTP else self.build_url()
        self.headers = headers
        self.params = params if isinstance(params, dict) else str_to_dict(params)
        self.mode = mode
        self.verbose = verbose
        self.expt = (0, 'None')
        # import requests
        # print(requests.get(target,params=params).text)
        # TODO
        output = None
        try:
            output = self._execute()
        except NotImplementedError:
            self.expt = (ERROR_TYPE_ID.NOTIMPLEMENTEDERROR, e)
            logger.log(CUSTOM_LOGGING.ERROR, 'POC {} not defined "{1}" mode'.format(self.name, self.mode))
            output = Output(self)
        except ConnectTimeout as e:
            self.expt = (ERROR_TYPE_ID.CONNECTTIMEOUT, e)
            counts = conf.get('retry',0)
            while counts > 0:
                logger.debug('POC:{0} timeout, start is over.'.format(self.name))
                try:
                    output = self._execute()
                    break
                except ConnectTimeout:
                    logger.debug('POC:{0} time-out retry failed!'.format(self.name))
                counts -= 1
                conf['retry'] = counts
            else:
                msg = "connect target '{0}' failed!".format(target)
                logger.error(msg)
                output = Output(self)
        except HTTPError as e:
            self.expt = (ERROR_TYPE_ID.HTTPERROR, e)
            logger.warn('POC: {0} HTTPError occures, start it over.'.format(self.name))
            output = Output(self)
        except ConnectionError as e:
            self.expt = (ERROR_TYPE_ID.CONNECTIONERROR, e)
            msg = "connect target '{0}' failed!".format(self.target)
            logger.error(msg)
            output = Output(self)
        except TooManyRedirects as e:
            self.expt = (ERROR_TYPE_ID.TOOMANYREDIRECTS, e)
            logger.debug(str(e))
            output = Output(self)
        except BaseException as e:
            self.expt = (ERROR_TYPE_ID.OTHER, e)
            logger.error('PoC {0} has raised a exception: {1}'.format(self.name, e))
            output = Output(self)
        return output

    def _attack(self):
        """
        @function   以Poc的attack模式对urls进行检测（可能具有危险性），
                    需要用户在自定义的Poc中进行重写，
                    返回一个Output实例
        :return:
        """
        raise NotImplementedError

    def _verify(self):
        """
        @function   以Poc的verify模式对urls进行检测（可能具有危险性），
                    需要用户在自定义的Poc中进行重写，
                    返回一个Output实例
        :return:
        """
        raise NotImplementedError

    def _run(self):
        """
        @function   以Poc的GUI模式对url进行检测（可能具有危险性），
                    需要在用户自定义的Poc中进行重写，
                    返回一个Output实例
        :return:
        """
        raise NotImplementedError


class Output(object):
    def __init__(self, poc=None):
        self.error_msg = tuple()
        self.result = {}
        self.status = OUTPUT_STATUS.FAILED
        if poc:
            self.target_id = poc.target_id
            self.target = poc.target
            self.url = poc.url
            self.mode = poc.mode
            self.vul_id = poc.vulID
            self.name = poc.name
            self.app_name = poc.appName
            self.app_version = poc.appVersion
            self.error_msg = poc.expt
            self.expt = poc.expt

    def is_success(self):
        return bool(True and self.status)

    def show_result(self):
        msg = "target {}: {} is exist [{}].".format(
            self.target_id, self.url, self.name) if self.status else "target {}: {} is not exist [{}]".format(
            self.target_id, self.url, self.name)
        return msg

    def success(self, result):
        assert isinstance(result, dict)
        self.status = OUTPUT_STATUS.SUCCESS

    def fail(self, error=""):
        assert isinstance(error, str)
        self.status = OUTPUT_STATUS.FAILED
        self.error_msg = (0, error)

    def error(self, error=''):
        self.expt = (ERROR_TYPE_ID.OTHER, error)
        self.error_msg = (0, error)

    # def show_result(self):
    #     if self.status == OUTPUT_STATUS.SUCCESS:
    #         for k, v in self.result.items():
    #             if isinstance(v, dict):
    #                 for kk, vv in v.items():
    #                     #     if (kk == "URL" or kk == "IP") and conf.ppt:
    #                     #         vv = desensitization(vv)
    #                     logger.log(CUSTOM_LOGGING.SUCCESS, "%s : %s" % (kk, vv))
    #             else:
    # if (k == "URL" or k == "IP") and conf.ppt:
    #     v = desensitization(v)
    # logger.log(CUSTOM_LOGGING.SUCCESS, "%s : %s" % (k, v))


def to_dict(self):
    return self.__dict__
