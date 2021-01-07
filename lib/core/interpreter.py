# !/usr/bin/python3
# -*-coding:utf-8-*-
# Author: Liang Ma
# CreatedDate: 2021/1/6 16:50
# Description:
import argparse
import ast
from lib.common.merge_dict import rec_merge
from lib.core.settings import CONF

conf = CONF


class Parser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog='needle Scanner', usage='python3 main.py [options]..')
        self.target_group = self.parser.add_argument_group(title='Target',
                                                           description='At least one of these options has to be provided to define the target(s)')
        self.mode_group = self.parser.add_argument_group(title='Mode', description='Scanner running model options')

        self.request_group = self.parser.add_argument_group(title='Request', description='Network request options')

        self.optimization_group = self.parser.add_argument_group(title='Optimization',
                                                                 description='Optimization options')

        self.poc_group = self.parser.add_argument_group(title='Poc', description='Optimization options')

        self.target_parser()
        self.mode_parser()
        self.request_parser()
        self.optimization_parser()
        self.poc_parser()

        self.parser.add_argument('--version', help="Show program's version number and exit")
        self.args = self.parser.parse_args()
        self.format_args()

    def target_parser(self):
        target_group = self.target_group
        target_group.add_argument('-u', '--url', help='Target URL (e.g. "https://www.site.com/vuln.php?id=1")')
        target_group.add_argument('-f', '--file', help='Scan multiple targets given in a textual file')
        target_group.add_argument('-r', '--poc', help='Load Poc file From local or remote website')
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
        request_group.add_argument('--timeout', help='Seconds to wait before timeout connection (default:30)')
        request_group.add_argument('--retry', help='Time out retrials times')
        request_group.add_argument('--delay', help='Delay between two request of one thread')
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
        if self.args.poc_args:
            self.args.poc_args = ast.literal_eval(args.poc_args)

        args = vars(args)
        request = {}
        request.update((k, args[k]) for k in
                            ['cookie', 'host', 'referer', 'proxy', 'proxy_cred', 'timeout', 'retry', 'delay',
                             'headers'])
        for key in request.keys():
            del args[key]
        args['requests'] = request

        self.args = args
