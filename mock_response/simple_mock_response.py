# -*- coding: utf-8 -*-
"""
    :author: T8840
    :tag: Thinking is a good thing!
    :description: 
"""

import mitmproxy.http

env= "UAT"

accountInfo_response_test4 = """"""
# 需补全
# accountInfo_response_UAT = """{"succeed":true,"code":"000000","msg":"操作成功","cache":"MISS","data":[{"productCode":"zbank","bankName":"","baseAcctNo":"6236430901112268621","status":1,"balance":0.56,"name":"肖育明","idNo":"360731*********4332","phoneNo":"186****1416","isAddAccountInfo":true,"bankCards":[{"bankCode":"BOC","bankName":"中国银行","cardType":"01","cardNo":"621758*********5115","phoneNo":"186****1416","tradeAccount":"016911045692621758511514164332","isDefault":true,"dayLimit":50000.0,"onceLimit":50000.0,"monthLimit":0},{"bankCode":"CCB","bankName":"中国建设银行","cardType":"01","cardNo":"621700*********7418","phoneNo":"186****1416","tradeAccount":"016911045692621700741814164332","isDefault":false,"dayLimit":4000000.0,"onceLimit":200000.0,"monthLimit":0}],"rechargeStatus":1,"rechargeNoticeMsg":null,"rechargeLimitSource":null,"withdrawStatus":1,"withdrawNoticeMsg":null,"withdrawLimitSource":null,"idCardStatus":0,"expiredStatus":1}]}"""
# 
accountInfo_response_UAT ="""{"succeed":true,"code":"000000","msg":"操作成功","cache":"MISS","data":[{"productCode":"zbank","bankName":"","baseAcctNo":"6236430901024965140","status":1,"balance":100.76,"name":"王希涛","idNo":"372923*********005X","phoneNo":"132****7633","isAddAccountInfo":true,"bankCards":[{"bankCode":"CCB","bankName":"中国建设银行","cardType":"01","cardNo":"621700*********1105","phoneNo":"132****7633","tradeAccount":"01691969838662170011057633005X","isDefault":true,"dayLimit":4000000.0,"onceLimit":200000.0,"monthLimit":0}],"rechargeStatus":1,"rechargeNoticeMsg":null,"rechargeLimitSource":null,"withdrawStatus":1,"withdrawNoticeMsg":null,"withdrawLimitSource":null,"idCardStatus":1,"expiredStatus":2}]}"""
accountInfo_response_Pro = """"""

accountInfo_response = {
    "Test4": accountInfo_response_test4,
    "UAT": accountInfo_response_UAT,
    "Pro":accountInfo_response_Pro
}


accountInfo1_response_UAT = """{"succeed":true,"code":"000000","msg":"操作成功","cache":"MISS","data":{"baseAcctNo":"623643*********8621","status":1,"balance":0.56,"name":"XX","idNo":"36*********2","phoneNo":"186****1416","isAddAccountInfo":true,"bankCards":[{"bankCode":"BOC","bankName":"行","cardType":"01","cardNo":"621758*********5115","phoneNo":"186****1416","tradeAccount":"016911045692621758511514164332","isDefault":true,"dayLimit":1000000.0,"onceLimit":1000000.0,"monthLimit":0},{"bankCode":"CCB","bankName":"中国建设银行","cardType":"01","cardNo":"621700*********7418","phoneNo":"186****1416","tradeAccount":"016911045692621700741814164332","isDefault":false,"dayLimit":1000000.0,"onceLimit":1000000.0,"monthLimit":0}],"expiredStatus":1,"idCardStatus":0}}"""
accountInfo1_response = {
    "UAT": accountInfo1_response_UAT
}


# 过期加需补全
getOcrRecord_response_test4 = """{"succeed":true,"code":"000000","msg":"操作成功","cache":"MISS","data":{"name":"XX","idNo":"447","expiryDate":"2020.06.21","issDate":"2006.06.21","serialNo":"ZBACC100","day":1,"idCardStatus":1}}"""
# 
# getOcrRecord_response_UAT = """{"succeed":true,"code":"000000","msg":"操作成功","cache":"MISS","data":{"name":"XX","idNo":"36072","expiryDate":"2027.05.31","issDate":"2017.05.31","serialNo":"ZBA502710000","day":2533,"idCardStatus":0}}"""
# wang
getOcrRecord_response_UAT ="""{"succeed":true,"code":"000000","msg":"操作成功","cache":"MISS","data":{"name":"XX","idNo":"YY","expiryDate":"2039.08.19","issDate":"2019.08.19","serialNo":"Z840000","day":1,"idCardStatus":1}}"""
getOcrRecord_response_Pro ="""{"succeed":true,"code":"000000","msg":"操作成功","cache":"MISS","data":{"name":"XX","idNo":"YY","expiryDate":"2039.08.19","issDate":"2019.08.19","serialNo":"Z406840000","day":1,"idCardStatus":0}}"""

getOcrRecord_response = {
    "Test4": getOcrRecord_response_test4,
    "UAT": getOcrRecord_response_UAT,
    "Pro":getOcrRecord_response_Pro
}



class MockResponse:

    def response(self, flow: mitmproxy.http.HTTPFlow):
        if "/zbankws/ws/account/v3/accountInfo" in flow.request.path :
            mock_response = accountInfo_response[env]
            flow.response.content = bytes(mock_response.encode('utf8'))

        if "/zbankws/ws/account/v1/accountInfo" in flow.request.path:
            mock_response = accountInfo1_response["UAT"]
            flow.response.content = bytes(mock_response.encode('utf8'))

        elif "/zbankws/ws/realName/v1/getOcrRecord" in flow.request.path:
            mock_response = getOcrRecord_response[env]
            flow.response.content = bytes(mock_response.encode('utf8'))
        else:
            return


addons = [
    MockResponse()
]

