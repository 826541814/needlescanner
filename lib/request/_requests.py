# !/usr/bin/python3
# -*-coding:utf-8-*-
# Author: Liang Ma
# CreatedDate: 2021/1/6 11:35
# Description:

from lib.core.settings import CONF
from requests.models import Request
from requests.sessions import Session
from requests.sessions import merge_setting, merge_cookies
from requests.cookies import RequestsCookieJar
from requests.utils import get_encodings_from_content


def session_requests(self, method, url, params=None, data=None, headers=None, cookies=None, files=None, auth=None,
                     timeout=None, allow_redirects=True, proxies=None, hooks=None, stream=None, verify=False, cert=None,
                     json=None):
    conf = CONF.get('requests', {})
    timeout = timeout if timeout else conf.get('timeout', 30)
    merged_cookies = merge_cookies(merge_cookies(RequestsCookieJar(), self.cookies),
                                   cookies or conf.get('cookie', None))
    eq = Request(

        method=method.upper(),

        url=url,

        headers=merge_setting(headers, conf["headers"] if 'headers' in conf else {}),

        files=files,

        data=data or {},

        json=json,

        params=params or {},

        auth=auth,

        cookies=merged_cookies,

        hooks=hooks,

    )

    prep = self.prepare_request(req)

    proxies = proxies or (conf["proxies"] if 'proxies' in conf else {})

    settings = self.merge_environment_settings(

        prep.url, proxies, stream, verify, cert

    )

    # Send the request.

    send_kwargs = {

        'timeout': timeout,

        'allow_redirects': allow_redirects,

    }

    send_kwargs.update(settings)

    resp = self.send(prep, **send_kwargs)

    if resp.encoding == 'ISO-8859-1':

        encodings = get_encodings_from_content(resp.text)

        if encodings:

            encoding = encodings[0]

        else:

            encoding = resp.apparent_encoding

        resp.encoding = encoding

    return resp


def patch_session():
    Session.request = session_request