# -*- coding: utf-8 -*-
"""
    :author: T8840
    :tag: Thinking is a good thing!
          纸上得来终觉浅，绝知此事要躬行！
    :description: 本脚本只针对埋点上报格式为 POST https://xxxx.net/log-collect/front-behaviour

                    其中, request body 包含埋点上报字段，格式：raw
                    content=%7B%22commons%22%3A%7B%22departmentID%22%3A%22financing%22%2C%22businessID%22%3A%22behaviour_common%22%2C%22udid%22%3A%22deviceId-864555037917836%22%2C%22channel%22%3A%22feature%22%2C%22system_name%22%3A%22android+OS%22%2C%22system_version%22%3A%227.1.2%22%2C%22appName%22%3A%22android-mymoney%22%2C%22appVersion%22%3A%2212.58.0.0%22%2C%22cookieid%22%3A%22%22%7D%2C%22events%22%3A%5B%7B%22session_id%22%3A%22a119ed594c084f28acc0654d067cb2231596006368191%22%2C%22url%22%3A%22https%3A%2F%2Flctsres4.ssjlicai.com%2Fpublic-vue%2Fbank%2Findex.html%23%2Fpurchase%2Fzgcbank%3Ftype%3D3%22%2C%22title%22%3A%22%E4%B8%AD%E5%85%B3%E6%9D%91%E9%93%B6%E8%A1%8C-%E5%AD%98%E5%85%A5%E9%A1%B5%22%2C%22etype%22%3A%22view%22%2C%22sku%22%3A%22licai_zbank%22%2C%22page_name%22%3A%22%E5%AD%98%E5%85%A5%E9%A1%B5%22%2C%22order_id%22%3A%22%22%2C%22amount%22%3A%22%22%2C%22inner_media%22%3A%22%22%2C%22outer_media%22%3A%22%22%2C%22referrer%22%3A%22%22%2C%22useragent%22%3A%22Mozilla%2F5.0+(Linux%3B+Android+7.1.2%3B+vivo+X9+Build%2FN2G47H%3B+wv)+AppleWebKit%2F537.36+(KHTML%2C+like+Gecko)+Version%2F4.0+Chrome%2F55.0.2883.91+Mobile+Safari%2F537.36+DPI%2F480+Resolution%2F1080*1920+feideeAndroid-V7+MyMoney%2F12.58.0.0+feideeAndroidMarket%22%2C%22product_id%22%3A%22%22%2C%22client_id%22%3A%2204%22%2C%22sub_client_id%22%3A%22ssj%22%2C%22adid%22%3A%22%22%2C%22cid%22%3A%22%22%2C%22appstoreid%22%3A%22%22%2C%22idfa%22%3A%22%22%7D%5D%7D&em=n

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

from utils import get_yaml_data, urlDe
from log_collect.compare import Rabbit


yaml_data = get_yaml_data('./allow.yaml')
AllowRule = namedtuple('AllowRule',['allow_path_rule','allow_host_rule'])
allow_rule = AllowRule(yaml_data.get('allow').get('path'),yaml_data.get('allow').get('host'))

save_type = ['save_file', 'save_mysql','save_rabbit'][0]

class RecordHttpPost:

    def save_flow_to(self,content):
        if save_type == "save_file":
            record_dump_file = './record_post_contents' + '.txt'
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
        self.save_flow_to(urlDe((req.content)))


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



addons = [RecordHttpPost()]
