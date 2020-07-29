# -*- coding: utf-8 -*-
"""
    :author: T8840
    :tag: Thinking is a good thing!
          纸上得来终觉浅，绝知此事要躬行！
    :description:
                传入文件：
                    用户需要将检查的埋点要求保存到本地文件：record_check.csv，格式见范例
                输出文件：
                    1）捕获的埋点解密后的数据：upload_record.txt
                    2）捕获的埋点中需要校对的类型数据：upload_record_type.txt

"""
__all__ = ["Rabbit"]
import os,sys
import re
import json
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)

from utils import urlDe,base64De
from utils import GetKeyValue
# from log_collect.record_http_get import save_type
save_type = ['save_file', 'save_mysql','save_rabbit'][0]


import pika


class Rabbit(object):

    def __init__(self, username, password, host, port=5672):
        self.host = str(host)
        self.port = int(port)
        self.crt = pika.PlainCredentials(username, password)
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host=self.host,
                                                                      port=self.port, credentials=self.crt))
        self.channel = self.conn.channel()

    def declare_queue(self, queue_name, is_durable):
        queue = self.channel.queue_declare(queue=queue_name,
                                           durable=is_durable)

    def produce(self, r_key, msg, ex=''):
        self.channel.basic_publish(exchange=ex,
                                   routing_key=r_key,
                                   body=msg,
                                   properties=pika.BasicProperties(
                                       delivery_mode=2  # make message persistent
                                   ))

    def set_qos(self):
        self.channel.basic_qos(prefetch_count=1)

    def callback(cls, ch, method, properties, body):
        print(" [x] Received %r " % body)
        url = str(body,encoding='utf-8')
        c = Compare()
        c.compare(c.getUserValues(),c.parseData(url))

    def consume(self, queue_name, callback=None, no_ack=False):
        if callback == None:
            self.channel.basic_consume(on_message_callback= self.callback,
                                       queue=queue_name, auto_ack=True)
        else:
            self.channel.basic_consume(callback,
                                       queue=queue_name, no_ack=no_ack)
        self.channel.start_consuming()

    def msg_count(self, queue_name, is_durable=True):
        queue = self.channel.queue_declare(queue=queue_name, durable=is_durable)
        count = queue.method.message_count
        return count

    def close(self):
        self.conn.close()




class Compare():

    def __init__(self):
        self.record_type= ["GET","POST"][1]
        self.keys = ["etype", "title"]
        # 用户上传的用于检查埋点的文档
        self.u_file = "./record_check.csv"

        # 将捕获的埋点中需要校对的类型数据到upload_record.txt
        self.f_file = "./upload_record.txt"
        # 将捕获的埋点中需要校对的类型数据到upload_record_type.txt
        self.s_file = "./upload_record_type.txt"

    def getUserValues(self):
        """从埋点文件中提取出用户想校验的数据"""
        need_check_data = []

        with open(self.u_file, encoding='utf-8') as f:
            for line in f.readlines():
                if "etype" in line:
                    continue
                value = [[i] for i in line.replace("\n", '').split(",")]
                need_check_data.append(dict(zip(self.keys, value)))
        return need_check_data

    def parseGetData(self,url):
        """解析Get方法URL中加密数据"""
        pattern = 'content=(.*)&em=eb'
        s = re.compile(pattern).findall(str(url))
        if s:
            deContent = urlDe(base64De(s[0]))
            with open(self.f_file, 'a+',encoding='utf-8') as f:
                f.write("{}\n".format(str(deContent)))

            gkv = GetKeyValue(deContent, mode='s')
            result = {'etype': gkv.search_key('etype'), 'title': gkv.search_key('title')}
            print(result)
            with open(self.s_file, 'a+',encoding='utf-8') as f:
                f.write("{}\n".format(str(result)))
            return result

    def parsePostData(self,content):
        """解析POST body中content中内容"""
        pattern = 'content=(.*)&em=n'
        s = re.compile(pattern).findall(str(content))
        if s:
            deContent = s[0]
            with open(self.f_file, 'a+', encoding='utf-8') as f:
                f.write("{}\n".format(str(deContent)))

            gkv = GetKeyValue(deContent, mode='s')
            result = {'etype': gkv.search_key('etype'), 'title': gkv.search_key('title')}
            print(result)
            with open(self.s_file, 'a+', encoding='utf-8') as f:
                f.write("{}\n".format(str(result)))
            return result

    def compare(self,user_values, upload_data):
        """针对上传数据单条进行比对,注意要比对的是什么类型的记录数据"""
        if self.record_type == "GET":
            if self.parseGetData(upload_data) in user_values:
                print("符合要求的埋点:{}，原始数据为：{}".format(self.parseGetData(upload_data),upload_data))
        elif self.record_type == "POST":
            if self.parsePostData(upload_data) in user_values:
                print("符合要求的埋点:{}，原始数据为：{}".format(self.parsePostData(upload_data), upload_data))
        else:
            raise Exception

    def compareDataFromType(self):
        if save_type == "save_file":
            if self.record_type == "GET":
                file = './record_allow_urls.txt'
            elif self.record_type == "POST":
                file = './record_post_contents.txt'
            else:
                raise Exception
            with open(file,'r',encoding='utf-8') as f:
                for url in f.readlines():
                    self.compare(self.getUserValues(), url)
        elif save_type == "save_mysql":
            mysql_env = {}
            self.mysql = ""
            pass
        elif save_type == "save_rabbit":
            rabbitmq_env = {'host': '10.201.5.156', 'port': 5673, 'password': 'guest', 'username': 'guest'}
            rabbit = Rabbit(**rabbitmq_env)
            rabbit.consume(queue_name="flows")
        else:
            raise Exception


if __name__ == "__main__":
    compare = Compare()
    compare.compareDataFromType()
