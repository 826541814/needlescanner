# !/usr/bin/python3
# -*-coding:utf-8-*-
# Author: Liang Ma
# CreatedDate: 2021/1/12 15:07
# Description:
from queue import Queue

from lib.core.data import kb, conf, logger, merged_options
from lib.core.datatype import AttribDict
from lib.core.settings import DEFAULT_LISTENER_PORT, DEFAULT_USER_AGENT
from lib.thirdparty.oset.orderedset import OrderedSet


def _set_conf_attributes():
    """
    This function set some needed attributes into the configuration singleton
    :return:
    """
    debug_msg = "initializing th configuration"
    logger.debug(debug_msg)

    conf.url = None
    conf.url_file = None
    conf.mode = 'verify'
    conf.poc = None
    conf.cookie = None
    conf.host = None
    conf.referer = None
    conf.agent = None
    conf.headers = None
    conf.random_agent = None
    conf.proxy = None
    conf.proxy_cred = None
    conf.proxies = {}
    conf.timeout = 30
    conf.retry = 0
    conf.delay = 0
    conf.http_headers = {}
    conf.agents = [DEFAULT_USER_AGENT]  # 数据源从插件加载的时候无默认值需要处理
    conf.login_user = None
    conf.login_pass = None
    # conf.shodan_token = None
    # conf.fofa_user = None
    # conf.fofa_token = None
    # conf.censys_uid = None
    # conf.censys_secret = None
    # conf.dork = None
    # conf.dork_zoomeye = None
    # conf.dork_shodan = None
    # conf.dork_fofa = None
    # conf.dork_censys = None
    # conf.max_page = 1
    conf.search_type = 'host'
    conf.comparison = False
    conf.vul_keyword = None
    conf.ssvid = None
    conf.plugins = []
    conf.threads = 1
    conf.batch = False
    conf.check_requires = False
    conf.quiet = False
    conf.update_all = False
    conf.verbose = 1

    conf.ipv6 = False
    conf.multiple_targets = False
    conf.pocs_path = None
    conf.output_path = None
    conf.plugin_name = None
    conf.plugin_code = None
    conf.connect_back_host = None
    conf.connect_back_port = DEFAULT_LISTENER_PORT
    conf.console_mode = False
    conf.show_version = False
    conf.api = False  # api for zipoc
    conf.ppt = False


# def _set_poc_options(input_options):
#     for line in input_options.keys():
#         if line not in CMD_PARSE_WHITELIST:
#             DIY_OPTIONS.append(line)


def _set_kb_attributes():
    """
    This function set some needed attributes into the knowledge base
    :return:
    """
    debug_msg = "initializing the knowledge base"
    logger.debug(debug_msg)

    kb.abs_file_paths = set()
    kb.os = None
    kb.os_version = None
    kb.arch = None
    kb.dbms = None
    kb.auth_header = None
    kb.counters = {}
    kb.multi_thread_mode = False
    kb.thread_continue = True
    kb.thread_exception = False
    kb.word_lists = None
    kb.single_log_flags = set()

    kb.cache = AttribDict()
    kb.cache.addrinfo = {}
    kb.cache.content = {}
    kb.cache.regex = {}

    kb.data = AttribDict()
    kb.data.local_ips = []
    kb.data.connect_back_ip = None
    kb.data.connect_back_port = DEFAULT_LISTENER_PORT
    kb.data.clients = []
    kb.targets = OrderedSet()
    kb.plugins = AttribDict()
    kb.plugins.targets = AttribDict()
    kb.plugins.pocs = AttribDict()
    kb.plugins.results = AttribDict()
    kb.results = []
    kb.current_poc = None
    kb.registered_pocs = AttribDict()
    kb.task_queue = Queue()
    # kb.cmd_line = DIY_OPTIONS or []

    kb.comparison = None


def _merge_options(input_options, override_options):
    if hasattr(input_options, "items"):
        input_options_items = input_options.items()
    else:
        input_options_items = input_options.__dict__.items()

    for key, value in input_options_items:
        if key not in conf or value not in (None, False) or override_options:
            conf[key] = value

    if input_options.get("configFile"):
        # config_file_parser(input_options["configFile"])
        logger.error("can't load config from file")

    merged_options.update(conf)


def init_options(input_options=AttribDict(), override_options=False):
    _set_conf_attributes()
    # _set_poc_options(input_options)
    _set_kb_attributes()
    _merge_options(input_options, override_options)
    if conf.show_version:
        exit()
