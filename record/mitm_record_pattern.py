# -*- coding: utf-8 -*-
"""
    :author: T8840
    :tag: Thinking is a good thing!
    :description: 只允许与在allow.yaml文件中url path一致的请求才会记录对应的请求与响应
"""


import re
from mitmproxy import (
    http,
    ctx,
)
from urllib.parse import urlparse
import os, sys

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
from utils import get_yaml_data

yaml_data = get_yaml_data('./allow.yaml')


def get_allow_rule(data):
    allow_path_rule = data.get('allow').get('path')
    return allow_path_rule


class HTTPRecordAll:

    def __init__(self):
        self.record_dump_file = './record_allow_file' + '.txt'
        self.save_file = open(self.record_dump_file, 'w')

    def done(self):
        if self.save_file:
            self.save_file.close()

    def save_http_request(self, httpflow):
        self.save_file.write('========\n')
        self.save_file.write('REQUEST\n')
        self.save_file.write('========\n')
        req = httpflow.request
        self.save_file.write('%s %s %s\n' %
                             (req.method, req.url, req.http_version))
        for key, val in req.headers.items():
            self.save_file.write('%s: %s\n' % (key, val))
        if req.content:
            self.save_file.write('\n\n%s\n' %
                                 ((req.content).decode('utf-8')))

    def save_http_response(self, httpflow):
        self.save_file.write('=========\n')
        self.save_file.write('RESPONSE\n')
        self.save_file.write('=========\n')
        res = httpflow.response
        self.save_file.write('%s %s %s\n' %
                             (res.http_version, res.status_code, res.reason))
        for key, val in res.headers.items():
            self.save_file.write('%s: %s\n' % (key, val))
        if res.content:
            self.save_file.write('\n\n%s\n' %
                                 ((res.content).decode('utf-8')))

    def save_http(self, httpflow):
        """Dump HTTP Request and Response
          同时，针对filter.yaml中后缀规则进行过滤
        """

        allow_path_rule = get_allow_rule(yaml_data)
        if allow_path_rule:
            url_info = urlparse(httpflow.request.url)
            if url_info.path not in allow_path_rule:
                pass
            else:
                self.save_http_request(httpflow)
                self.save_http_response(httpflow)

    def response(self, flow: http.HTTPFlow):
        if self.save_file:
            self.save_http(flow)


addons = [HTTPRecordAll()]
