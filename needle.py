# !/usr/bin/python3
# -*-coding:utf-8-*-
# Author: Liang Ma
# CreatedDate: 2021/1/5 10:26
# Description:
import copy
import os
import time

from lib.common.common import set_paths
from lib.common.merge_dict import rec_merge
from lib.core.data import logger, kb, paths
from lib.core.interpreter import Parser
from lib.core.loader import load_string_to_module, PocLoader
from lib.core.poc import POCBase
from lib.core.register import load_file_to_module
from lib.core.option import init_options
from lib.core.settings import PATHS_POCS, POCS, CONF, PATHS_ROOT
import queue

from lib.core.threads import run_threads
from lib.request.patch import patch_session

WORKER = queue.Queue()


def banner():
    msg = r'''
  _   _               _ _      
 | \ | | ___  ___  __| | | ___ 
 |  \| |/ _ \/ _ \/ _` | |/ _ \
 | |\  |  __/  __/ (_| | |  __/
 |_| \_|\___|\___|\__,_|_|\___| {}
                               
    '''.format(version)

    print(msg)


def load_pocs(config):
    """
    遍历加载所有POC文件，并将使用的POC加入POCS中
    :return:
    """
    for root, dirs, files in os.walk(PATHS_POCS):
        files = filter(lambda x: x.endswith('.py') and not x.startswith('__') and x not in config.get('poc', []), files)
        for file in files:
            # _pocs.append(os.path.join(root,file))
            load_file_to_module(os.path.join(root, file))
    for k, v in kb.registered_pocs.items():
        if config.get('use_poc') in [v.vulID, v.name]:
            POCS.append(v)
            # output = v.execute(config.get('url'))
            # if output.is_success():
            #     print(output.result)
            # else:
            #     print(output.error_msg)


def init(config: dict):
    set_paths(PATHS_ROOT)
    patch_session()
    init_options()
    Parser(config)
    # parser.parse_args()
    load_pocs(config)
    logger.info("[*] target:{}".format(config["url"]))
    # _pocs = []

    # print(kb.registered_pocs.items())

    # for root, dirs, files in os.walk(PATHS_POCS):
    #     files = filter(lambda x: x.endswith('.py') and not x.startswith('__') and x not in config.get('poc', []), files)
    #     if keywords := config.get('use_pocs', None):
    #         for file in files:
    #             for keyword in keywords:
    #                 if keyword in file:
    #                     _pocs.append(os.path.join(root, file))
    #                 else:
    #                     pass
    #     else:
    #         _pocs.extend(map(lambda x: os.path.join(root, x), files))
    # for poc in _pocs:
    #     with open(poc, 'r', encoding='utf-8') as f:
    #         model = load_string_to_module(f.read())
    #         POCS.append(model)
    # CONF.update(config)


def end():
    print("[*] shutting down at {0}".format(time.strftime("%X")))


def worker():
    while not WORKER.empty():
        target_id, url, poc, header, param = WORKER.get()
        try:
            poc_mode = copy.deepcopy(poc)

            ret = poc_mode.execute(target_id=target_id, target=url, headers=header, params=param)
        except Exception as e:
            logger.error(e)
        if ret:
            # logger.info(ret.is_success())
            logger.info(ret.show_result())


def start(config: dict):
    url_list = config.get("url", [])
    request = config['requests']
    for target_id, url in enumerate(url_list):
        for poc in POCS:
            WORKER.put((target_id, url, poc, request.get('headers', {}), request.get('params', {})))
    run_threads(config.get('threads', CONF.get('threads', 4)), worker)


# def start(config: dict):
#     url_list = config.get('url', [])
#     for i in url_list:
#         for poc in POCS:
#             try:
#                 ret = poc.verify(i)
#             except Exception as e:
#                 ret = None
#                 print(e)
#             if ret:
#                 print(ret)


def main():
    banner()

    config = {

        "url": [""],
        "poc": [],
        "thread_num": 10,

    }
    rec_merge(config, CONF)

    init(config)

    start(config)

    end()


if __name__ == '__main__':
    version = "v0.00000001"

    main()
