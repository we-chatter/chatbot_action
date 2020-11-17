# -*- coding: utf-8 -*-

"""
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   ali_express.py
 
@Time    :   2020/7/27 5:28 下午
 
@Desc    :
 
"""

import requests
import logging
import json
from config.service_config import ServiceConfig


logger = logging.getLogger(__name__)

sc = ServiceConfig()


def get_express_detail(exNum, type=None):
    """

    :param exNum:
    :param type:
    :return:
    """
    path = '/kdwlcx' # 接口路径
    url = sc.exhost + path + '?' + 'no=' + exNum
    header = {"Authorization":'APPCODE ' + sc.appcode}
    try:
        response = requests.get(url,headers=header)
    except :
        logger.info('{} is wrong'.format(url))
        exit()
    httpStatusCode = response.status_code

    if(httpStatusCode == 200):
        logger.info('Success requested Ali Express, StatusCode is {}'.format(httpStatusCode))
        result = json.loads(response.text)   # 返回结果
        print(response.text)
    else:
        httpReason = response.headers['X-Ca-Error-Message']
        logger.info('Failure, reason is {}'.format(httpReason))

if __name__=='__main__':
    msg = '1192753372520'
    get_express_detail(msg)