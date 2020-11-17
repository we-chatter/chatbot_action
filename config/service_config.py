# -*- coding: utf-8 -*-

"""
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   service_config.py
 
@Time    :   2020/7/27 7:13 下午
 
@Desc    :   外部服务调用配置
 
"""


class ServiceConfig:

    def __init__(self):

        # 快递查询
        self.exhost = 'https://kdwlcxf.market.alicloudapi.com'
        self.appcode = 'de7111ca3c0c4112bc726409e375c014'   # 阿里云快递查询接口

        self.api_secret = "Sq6NfAburbGs9MGQb"  # 心知天气API