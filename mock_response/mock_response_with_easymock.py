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
from mock_response.opEasyMock import EasyMock


# EasyMock配置
project_url = "http://10.201.7.226:7300/project/5eb66711e7b3875d86155ced"
login_info = {
        'name': 'caodashan',
        'password': '123456'
    }
easy_mock_project = EasyMock(project_url,login_info)
path_list = easy_mock_project.getMockURL()

class MockResponse:
    def response(self, flow: mitmproxy.http.HTTPFlow):
        if flow.request.path in path_list :
            content= easy_mock_project.getMockUrlResponse(flow.request.path)
            mock_response = json.dumps(json.loads(content), indent=4, sort_keys=False,ensure_ascii=False)
            flow.response.content = bytes(mock_response.encode('utf8'))
        else:
            return


addons = [
    MockResponse()
]

