# !/usr/bin/python3
# -*-coding:utf-8-*-
# Author: Liang Ma
# CreatedDate: 2021/1/5 10:26
# Description:

import os
import time

from lib.core.data import logger
from lib.core.interpreter import Parser
from lib.core.loader import load_string_to_module
from lib.core.settings import PATHS_POCS, POCS, CONF
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


def init(config: dict):
    patch_session()
    args = Parser().args
    print(args)
    # parser.parse_args()
    print("[*] target:{}".format(config["url"]))

    _pocs = []
    for root, dirs, files in os.walk(PATHS_POCS):
        files = filter(lambda x: x.endswith('.py') and not x.startswith('__') and x not in config.get('poc', []), files)
        _pocs.extend(map(lambda x: os.path.join(root, x), files))

    for poc in _pocs:
        with open(poc, 'r', encoding='utf-8') as f:
            model = load_string_to_module(f.read())
            POCS.append(model)
    CONF.update(config)


def end():
    print("[*] shutting down at {0}".format(time.strftime("%X")))


def worker():
    if not WORKER.empty():
        arg, poc = WORKER.get()
        try:
            ret = poc.verify(arg)
        except Exception as e:
            logger.error(e)
        if ret:
            logger.info(ret)


def start(config: dict):
    url_list = config.get("url", [])
    for arg in url_list:
        for poc in POCS:
            WORKER.put((arg, poc))

    run_threads(config.get('thread_num', 10), worker)


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

        "url": ["http://www.httpbin.org/get"],
        "poc": [],
        "thread_num": 10,
        "requests": {
            "timeout": 10,
            "headers": {
                "User-Agent": "i'm config"
            }
        }

    }

    init(config)

    start(config)

    end()


if __name__ == '__main__':
    version = "v0.00000001"

    main()
