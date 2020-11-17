# -*- coding: utf-8 -*-

"""
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   expressList.py
 
@Time    :   2020/7/27 8:00 下午
 
@Desc    :   快递公司编码，快递公司对应关系
 
"""

import requests
import json
import logging

from config.service_config import ServiceConfig

sc = ServiceConfig()

logger = logging.getLogger(__name__)


def get_express_value(type):
    """
    获取快递公司编码对应的中文快递公司名称
    :param type:
    :return:
    """
    path = '/cExpressLists'
    url = sc.exhost + path + '?' + 'type=' + type
    header = {"Authorization":'APPCODE ' + sc.appcode}
    try:
        res = requests.get(url,headers=header)
    except :
        logger.info('Url:{} is wrong'.format(url))
        exit()
    httpStatusCode = res.status_code

    if(httpStatusCode == 200):
        logger.info('Requested successful，httpStatusCode is {}'.format(httpStatusCode))
        result = json.loads(res.text)['result']

        return result
    else:
        httpReason = res.headers['X-Ca-Error-Message']
        logger.info('Failure, reason is {}'.format(httpReason))


if __name__=='__main__':
    type = 'DANNIAO'
    get_express_value(type)