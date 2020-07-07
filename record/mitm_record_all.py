# -*- coding: utf-8 -*-
"""
    :author: T8840
    :tag: Thinking is a good thing!
    :description:  除了添加在filter.yaml文件中需要忽略的后缀，其他所有的请求与响应都会被记录
"""

import re
from mitmproxy import (
    http,
    ctx,
)

import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
from utils import get_yaml_data

yaml_data = get_yaml_data('./filter.yaml')
def get_filter_rule(data):
    ignore = data.get('ignore')
    ignore_rule = ''.join([j for i in ignore for j in i.values()]).replace('/', '').replace('*.', '|').lstrip('|')
    return ignore_rule


class HTTPRecordAll:

    def __init__(self):
        self.record_dump_file = './record_all_file' + '.txt'
        self.save_file = open(self.record_dump_file,'w')


    def done(self):
        if self.save_file:
            self.save_file.close()

    def save_http_request(self,httpflow):
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

    def save_http_response(self,httpflow):
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

        ignore_rule = get_filter_rule(yaml_data)
        if ignore_rule:
            ignore_pattern = f'.*\.({ignore_rule})$'
            filter = re.match(ignore_pattern, httpflow.request.url)
            if filter != None:
                pass
            else:
                self.save_http_request(httpflow)
                self.save_http_response(httpflow)



    def response(self, flow: http.HTTPFlow):
        if self.save_file:
            self.save_http(flow)
    

addons = [ HTTPRecordAll() ]
