# !/usr/bin/python3
# -*-coding:utf-8-*-
# Author: Liang Ma
# CreatedDate: 2021/1/6 16:50
# Description:
import argparse
import ast
import logging

from lib.core.data import logger
from lib.core.enums import CUSTOM_LOGGING
from lib.core.settings import VERSION, CONF
from lib.common.merge_dict import rec_merge
from lib.utils import str_to_dict


class Parser:
    def __init__(self, config):
        self.parser = argparse.ArgumentParser(prog='needle Scanner', usage='python3 main.py [options]..')
        self.target_group = self.parser.add_argument_group(title='Target',
                                                           description='At least one of these options has to be provided to define the target(s)')
        self.mode_group = self.parser.add_argument_group(title='Mode', description='Scanner running model options')

        self.request_group = self.parser.add_argument_group(title='Request', description='Network request options')

        self.optimization_group = self.parser.add_argument_group(title='Optimization',
                                                                 description='Optimization options')

        self.poc_group = self.parser.add_argument_group(title='Poc', description='Optimization options')

        self.optional_parser()
        self.target_parser()
        self.mode_parser()
        self.request_parser()
        self.optimization_parser()
        self.poc_parser()

        self.args = self.parser.parse_args()
        self.format_args()

        self.show_version()
        self.set_verbosity()
        rec_merge(config, self.args)

    def show_version(self):
        if self.args.get('version', False):
            print('needle Scanner version: {}'.format(VERSION))
            exit()
        else:
            return

    def set_verbosity(self):
        verbose = int(self.args.get('verbose') or 1)

        if verbose == 0:
            logger.setLevel(logging.ERROR)
        elif verbose == 1:
            logger.setLevel(logging.INFO)
        elif verbose == 2:
            logger.setLevel(logging.DEBUG)
        elif verbose == 3:
            logger.setLevel(logging.DEBUG)
            logger.setLevel(CUSTOM_LOGGING.SYSINFO)
        elif verbose == 4:
            logger.setLevel(logging.DEBUG)
            logger.setLevel(CUSTOM_LOGGING.WARNING)
        elif verbose >= 5:
            logger.setLevel(logging.DEBUG)
            logger.setLevel(CUSTOM_LOGGING.ERROR)
        logger.debug('verbose level={}'.format(verbose))

    def optional_parser(self):
        self.parser.add_argument('--version', help="Show program's version number and exit", action='store_true')
        self.parser.add_argument('-v', '--verbose', help='Verbosity level: 0-6 (default 1)', type=int,
                                 choices={0, 1, 2, 3, 4, 5, 6})

    def target_parser(self):
        target_group = self.target_group
        target_group.add_argument('-u', '--url', help='''Single or List of Target URL (e.g. "['url1','url2']")''')
        target_group.add_argument('-f', '--file', help='Scan multiple targets given in a textual file')
        target_group.add_argument('-r', '--poc', help='Load Poc file From local or remote website')
        target_group.add_argument('--use_pocs',
                                  help='''Use poc name's keyword or vulID to specify poc (e.g. "['ssh_burst','0001']"''',
                                  type=str)
        target_group.add_argument('-c', dest='configfile', help='Load options from a configuration INI file')

    def mode_parser(self):
        mode_group = self.mode_group
        mode_choice_group = mode_group.add_mutually_exclusive_group()
        mode_choice_group.add_argument('--verify', help='Run poc with verify mode', action='store_true')
        mode_choice_group.add_argument('--attack', help='Run poc with attack mode', action='store_true')

    def request_parser(self):
        request_group = self.request_group
        request_group.add_argument('--cookie', help='HTTP Cookie header value')
        request_group.add_argument('--host', help='HTTP Host header value')
        request_group.add_argument('--referer', help='HTTP Referer header value')
        request_group.add_argument('--proxy', help='Use a proxy to connect to the target URL')
        request_group.add_argument('--proxy_cred', help='Proxy authentication credentials (name:password)')
        request_group.add_argument('--timeout', help='Seconds to wait before timeout connection (default:30)',
                                   default=30, type=int)
        request_group.add_argument('--retry', help='Time out retrials times')
        request_group.add_argument('--delay', help='Delay between two request of one thread')
        request_group.add_argument('--params', help='''set params for request (e.g. "{'key1':'value1'}")''')
        request_group.add_argument('--headers', help='''Extra headers (e.g. "{'key1':'value1','key2':'value2'}")''')

    def optimization_parser(self):
        optimization_group = self.optimization_group
        optimization_group.add_argument('--threads', help='Max number of concurrent network requests (default 4)',
                                        default=4, type=int)
        optimization_group.add_argument('--batch', help='Automatically choose default choice without asking')
        optimization_group.add_argument('--quiet', help='Activate quiet mode, working without logger')
        optimization_group.add_argument('--requires', help='Check install_require')

    def poc_parser(self):
        poc_group = self.poc_group
        poc_group.add_argument('--poc_args',
                               help='''definition options dict for PoC (e.g. --poc_args "{'username':'xxx','password':'xxx'}")''')

    def format_args(self):
        """
        将命令行中参数格式化，并转为字典
        :return:
        """
        args = self.args
        if self.args.headers:
            self.args.headers = ast.literal_eval(args.headers)
        if self.args.params:
            self.args.params = ast.literal_eval(args.params)

        if self.args.url:
            try:
                self.args.url = ast.literal_eval(self.args.url)
            except Exception:
                self.args.url = [self.args.url]
        # if self.args.use_pocs:
        #     try:
        #         self.args.use_pocs = str_to_dict(self.args.use_pocs)
        #     except ValueError:
        #         self.args.use_pocs = [args.use_pocs]
        # try:
        #     self.args.use_pocs = ast.literal_eval(args.use_pocs)
        # except ValueError:
        #     self.args.use_pocs = [args.use_pocs]
        # except Exception as e:
        #     logger.error(e)
        #     exit()

        if self.args.poc_args:
            self.args.poc_args = str_to_dict(args.poc_args)
        args = vars(args)
        request = {}
        request.update((k, args[k]) for k in
                       ['cookie', 'host', 'referer', 'proxy', 'proxy_cred', 'timeout', 'retry', 'delay',
                        'headers', 'params'])
        for key in request.keys():
            del args[key]
        args['requests'] = request

        self.args = args
