### Use Mitmproxy Mock Response

解决问题：使用本地客户端Mock替换接口返回数据，来验证前端逻辑与展示  
实现原理：针对Mitmproxy生命周期中的response流程进行了过滤处理，会将每一条数据流中的url path与目标path进行匹对，匹配成功就会返回目标response数据，没有匹配到就直接返回原response数据

#### 提供了三种方式
##### 1.简单的替换
说明：需要在该脚本中将选择替换的path与mock response数据放入到不同条件分支  
脚本：simple_mock_response.py  
使用：  
     1.Teminal切换到脚本目录  
     2.在Terminal中输入命令：mitmdump -s simple_mock_response.py
     
##### 2.path与mock数据写入到yaml文件中  
脚本：yaml_mock_response.py 与 mock_response.yaml
使用：1.在mock_response.yaml文件中按下面示例分别将目标path与response写入，使用数字区分不同path
     `1:  
        - path: "/zbankws/ws/realName/v1/getOcrRecord"  
        - response: {"succeed":true,"code":"000000","msg":"操作成功","cache":"MISS","data":{"name":"T8840"}}  
      2:  
        - path: "/log-collect/front-behaviour"  
        - response: {"succeed":true,"code":"000000","msg":"操作成功","cache":"MISS","data":[]}`  
     2.Teminal切换到脚本目录  
     3.在Terminal中输入命令：mitmdump -s yaml_mock_response.py
##### 3.与第三方Mock平台结合使用  
说明：  
脚本：opEasyMock.py与mock_response_with_easymock.py  
使用：
    1.在Easy Mock新建项目，并添加目标path与对应的response到该项目中  
    2.在mock_response_with_easymock.py脚本中填写下面2个信息：  
        1）将在Easy Mock创建项目时浏览器中的URL保存为project_url变量  
        2）并填入对应Easy Mock的账户密码  
    3.Teminal切换到脚本目录  
    4.在Terminal中输入命令：mitmdump -s mock_response_with_easymock.py