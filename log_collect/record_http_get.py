# -*- coding: utf-8 -*-
"""
    :author: T8840
    :tag: Thinking is a good thing!
          纸上得来终觉浅，绝知此事要躬行！
    :description: 本脚本只针对埋点上报格式为 GET https://xxxx.net/logCollect/events?content=encode_content&em=eb
                    其中,content=encode_content中encode_content为先后进行了url编码与base64编码的加密串

                    使用方式：
                            1）在同级目录下allow.yaml中写入需要记录的path：如：/logCollect/events 或events ,只允许1条
                                                              或host：如：xxxx.net ，只允许存在1条
                                                              也可以这2种类型都可以进行配置，最后记录的是同时满足这2种类型的url
                                                    上面 ?content=...eb 的部分请不要设置在path中，请注意
                            2）在Terminal中执行命令：mitmdump -s record_http_get.py

                    输出数据：
                            1）根据save_type会将捕获到的埋点数据，格式： https://xxxx.net/logCollect/events?content=encode_content&em=eb
                                                分别保存到本地record_allow_urls.txt文件中
                                                        或mysql数据库中
                                                        或rabbitmq队列中

"""

__all__ = ["save_type"]

import re
from mitmproxy import (
    http,
    ctx,
)
from urllib.parse import urlparse
from collections import namedtuple
import os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)

from utils import get_yaml_data
from log_collect.compare import Rabbit


yaml_data = get_yaml_data('./allow.yaml')
AllowRule = namedtuple('AllowRule',['allow_path_rule','allow_host_rule'])
allow_rule = AllowRule(yaml_data.get('allow').get('path'),yaml_data.get('allow').get('host'))

save_type = ['save_file', 'save_mysql','save_rabbit'][0]

class RecordHttpGet:

    def save_flow_to(self,content):
        if save_type == "save_file":
            record_dump_file = './record_allow_urls' + '.txt'
            self.save_file = open(record_dump_file, 'a')
            self.save_file.write('%s \n' % (content))

        elif save_type == "save_mysql":
            mysql_env = {}
            self.mysql = ""
            pass
        elif save_type == "save_rabbit":
            rabbitmq_env = {'host': '10.201.5.156', 'port': 5673, 'password': 'guest', 'username': 'guest'}
            self.rabbit = Rabbit(**rabbitmq_env)
            self.rabbit.declare_queue(queue_name="flows", is_durable=1000)
            self.rabbit_key = ''
            self.rabbit.produce(r_key="flows", msg=content)
        else:
            raise Exception

    def done(self):
        if self.save_file:
            self.save_file.close()
        if self.rabbit:
            self.rabbit.close()
        if self.mysql:
            # self.mysql.close()
            pass

    def save_http_request(self, httpflow):
        req = httpflow.request
        self.save_flow_to(req.url)


    def save_http(self, httpflow):

        url_info = urlparse(httpflow.request.url)

        exist_index = [i for i in range(allow_rule.__len__()) if allow_rule.__getitem__(i)]
        if len(exist_index) == 2:
            if  allow_rule.allow_path_rule[0] not in url_info.path:
                pass
            else:
                if url_info.hostname not in allow_rule.allow_host_rule:
                    self.save_http_request(httpflow)
                else:
                    pass
        else:
            if 0 in exist_index:
                if allow_rule.allow_path_rule[0] not in url_info.path:
                    pass
                else:
                    self.save_http_request(httpflow)
            else:
                if url_info.hostname not in allow_rule.allow_host_rule:
                    pass
                else:
                    self.save_http_request(httpflow)


    def request(self,flow:http.HTTPFlow):
        self.save_http(flow)



addons = [RecordHttpGet()]
