import yaml
import os
import json
import random
import re
from time import sleep

def get_yaml_data(file):
    if not os.path.isfile(file):
        raise FileNotFoundError
    fname, fext = os.path.splitext(file)
    with open(file) as data:
        if fext == ".yaml":
            data = yaml.safe_load(data)
        else:
            data = json.load(data)
        return data

def delay(flow, conf):
    """Delay http flow

    delay flow according to conf file

    Arg:
        flow : http flow
    """
    config = get_yaml_data(conf)
    url = flow.request.url

    if config is not None:
        for patternURL, timer in config.items():
            delay = round(random.uniform(min(timer[0], timer[1]), max(timer[0], timer[1])), 2)
            if re.match(patternURL, url) is not None:
                # ctx.log.warn(str(delay) + 's delay: ' + url)
                sleep(delay)

def base64De(s):
    """base64解码"""
    import base64
    missing_padding = 4 - len(s) % 4
    if missing_padding:
        s += '=' * missing_padding
    s=bytes(s,encoding='utf8')
    return base64.b64decode(s)

def urlDe(s):
    """URL解码"""
    from urllib import parse
    if isinstance(s,bytes):
        s= str(s,encoding='utf-8')
        return parse.unquote(s)

import json

class GetKeyValue(object):
    def __init__(self, o, mode='j'):
        self.json_object = None
        if mode == 'j':
            self.json_object = o
        elif mode == 's':
            self.json_object = json.loads(o)
        else:
            raise Exception('Unexpected mode argument.Choose "j" or "s".')

        self.result_list = []

    def search_key(self, key):
        self.result_list = []
        self.__search(self.json_object, key)
        return self.result_list

    def __search(self, json_object, key):

        for k in json_object:
            if k == key:
                self.result_list.append(json_object[k])
            if isinstance(json_object[k], dict):
                self.__search(json_object[k], key)
            if isinstance(json_object[k], list):
                for item in json_object[k]:
                    if isinstance(item, dict):
                        self.__search(item, key)
        return
