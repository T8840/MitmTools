# -*- coding:utf-8 -*-

"""
通用Easy Mock操作方法
    传入：
        1.url -- easy mock路径
        2.匹配类型 -- 即要替换的目标值
        3.替换值  -- 替换目标的值

    输出：
        1.查看原url的接口内容
        2.替换执行是否成功

    具体做法：

"""

import requests
import json
import re
from collections import namedtuple

class EasyMock(object):
    def __init__(self,project_url,login_info):
        self.project_url = project_url
        self.path = self.getProjectInfo().path
        self.project_id = self.getProjectInfo().project_id
        # 登录相关
        # 登录的用户名密码
        self.login_info = login_info
        self.data_token = self.login()
        self.h = {"Authorization": "Bearer " + self.data_token}
        self.c = {"easy-mock_token": self.data_token}

    def login(self):
        login_url = r'http://' + self.path + '/api/u/login'
        r = requests.post(login_url, data=self.login_info, verify=False)
        data_token = json.loads(r.text)['data']['token']
        return data_token

    def getProjectInfo(self):
        project_info = namedtuple("mockURL", ['path', 'project_id'])
        if self.project_url.count(r'http://'):
            path = self.project_url.split('/')[2]
            project_id = self.project_url.split('/')[-1]

        else:
            path = self.project_url.split('/')[0]
            project_id = self.project_url.split('/')[2]

        return project_info(
            path=path,
            project_id=project_id
        )

    def getMockContent(self):
        project_detail_url = r'http://' + self.path + '/api/mock?project_id=' + self.project_id + '&page_size=2000&page_index=1&keywords='
        s = requests.get(project_detail_url, headers=self.h, cookies=self.c)
        json_text = json.loads(s.text)['data']['mocks']
        return json_text

    def getMockURL(self):
        url_list = [i["url"]  for i in self.getMockContent()]
        return url_list

    def getMockUrlResponse(self,api_url):
        for i in self.getMockContent():
            if i.get('url') == api_url:
                return i.get('mode')

    def getMockUrlContent(self,api_url):
        for i in self.getMockContent():
            if i.get('url') == api_url:
                return i

    def queryPatternInMock(self,pattern,api_url):
        """返回查询到的匹配值"""
        search_result = re.search(pattern, self.getMockUrlResponse(api_url), re.S)
        return search_result

    def updateContent(self,pattern,api_url,target):

        update_url = r'http://' + self.path + '/api/mock/update'
        mock_url_content = self.getMockUrlContent(api_url)
        search_result = self.queryPatternInMock(pattern,api_url)
        if search_result:
            replace_content = self.getMockUrlResponse(api_url).replace(search_result.group(1), target)
        else:
            # ("没有找到要替换内容,准备插入新内容:%s")%target)
            function_pattern = r"function\(.*?\).*?{"
            # Mock数据中存在条件筛选数据才会允许插入
            if self.queryPatternInMock(function_pattern,api_url):
                search_result = re.search(function_pattern, self.getMockUrlResponse(api_url), re.S)
                target = search_result.group(0) + target
                replace_content = self.getMockUrlResponse(api_url).replace(search_result.group(0), target)
            else:
                raise Exception("没有找到要替换内容,请手动插入到EasyMock中~")
        update_data = {"url": api_url, "description": mock_url_content.get('description'),
                       "id": mock_url_content.get('_id'), "method": mock_url_content.get('method'),
                       "mode": replace_content}
        # print(update_data)
        # print(replace_content)
        resp = requests.post(url=update_url, data=update_data, headers=self.h, cookies=self.c)
        print("已更新Easy Mock数据成功！%s"%resp)




if __name__ == "__main__":

    project_url = 'http://10.201.7.226:7300/project/5d0882ce0d79ef1a4f9480e4'
    api = '/loanDept2'
    target = """if (_req.body.suid === 'u_7wewr1') {
    return {"suid": "u_7wewr1",
         "product_code": "FUDAI",
         "zhitou_user": false,
         "details": [{"code": "auth_name", "status": "2", "channel": "", "value": "Easy Mock", "date_time": 1577940461000},
                     {"code": "auth_enhance", "status": "2", "channel": "", "value": "", "date_time": 1577940461000},
                     {"code": "auth_credit", "status": "2", "channel": "01", "value": "5000000","date_time": 1577940461000},
                     {"code": "money", "status": 0, "channel": "", "value": "", "date_time": ""},
                     {"code": "auth_credit_fail", "status": 0, "channel": "", "value": "", "date_time": ""}]}}"""
    # target = """if (_req.body.suid === 'u_7wewr1') { return {"没有找到该用户信息"} }"""
    pattern = r"({}.*?)(if|else)".format("if \(_req.body.suid === \'u_7wewr1\'\)")

    # 登录的用户名密码
    login_info = {
        'name': 'caodashan',
        'password': '123456'
    }
    A = EasyMock(project_url,login_info)
    print(A.getMockUrlResponse(api))
    print(A.getMockURL())
    # print(A.getMockUrlContent(api))
    # print(A.queryPatternInMock(pattern,api).group(1))
    # A.updateContent(pattern,api,target)

