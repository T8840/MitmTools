# -*- coding: utf-8 -*-
"""
    :author: T8840
    :tag: Thinking is a good thing!
    :description: 
"""

import mitmproxy.http
import json

import os,sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
from utils import get_yaml_data

data = get_yaml_data('./mock_response.yaml')
path_resp_list = [j for i in data.values() for j in i ]
path_list =  [i['path'] for i in path_resp_list[::2]]
resp_list = [i['response'] for i in path_resp_list[1::2]]

class MockResponse:

    def response(self, flow: mitmproxy.http.HTTPFlow):
        if flow.request.path in path_list :
            mock_response = json.dumps(resp_list[path_list.index(flow.request.path)],ensure_ascii=False)
            flow.response.content = bytes(mock_response.encode('utf8'))
        else:
            return


addons = [
    MockResponse()
]

