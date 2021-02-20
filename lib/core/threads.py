# !/usr/bin/python3
# -*-coding:utf-8-*-
# Author: Liang Ma
# CreatedDate: 2021/1/5 15:28
# Description:

import time
import threading
import traceback

from lib.core.data import conf
from lib.core.data import kb
from lib.core.data import logger
# from lib.core.settings import MAX_NUMBER_OF_THREADS


def exception_handled_function(thread_function, args=()):
    try:
        thread_function(*args)
    except KeyboardInterrupt:
        raise
    except Exception as e:
        # print('thread {0}:{1}'.format(threading.currentThread().getName(), str(e)))
        logger.error('thread {0}:{1}'.format(threading.currentThread().getName(), str(e)))


def run_threads(num_threads, thread_function, args: tuple = ()):
    threads = []
    for num_threads in range(num_threads):
        thread = threading.Thread(target=exception_handled_function, name=num_threads, args=(thread_function, args))
        thread.setDaemon(True)
        try:
            thread.start()
        except Exceptionas as ex:
            err_msg = "error occurred while starting new thread ('{0}')".format(str(ex))
            # print(err_msg)
            logger.error(err_msg)
            break
        threads.append(thread)

    alive = True
    while alive:
        alive = False
        for thread in threads:
            if thread.is_alive():
                alive = True
                time.sleep(0.1)
