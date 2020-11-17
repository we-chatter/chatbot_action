# -*- coding: utf-8 -*-

"""
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   run_server.py
 
@Time    :   2020/8/23 1:55 下午
 
@Desc    :   start action server
 
"""
import os
import sys

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)

import logging
import types
import argparse
from typing import List, Text, Union

from sanic import Sanic, response
from sanic.response import HTTPResponse
from sanic.request import Request
from sanic_cors import CORS

from model import utils
from server import params
from model.Model_config import DEFAULT_SERVER_PORT
from model.Executor import ActionExecutor

logger = logging.getLogger(__name__)


def configure_cors(
        app: Sanic,
        cors_origins: Union[Text, List[Text], None] = ""
) -> None:
    """
    解决跨域问题
    :param app:
    :param cors_origins:
    :return:
    """

    CORS(
        app, resources={r"/*": {"origins": cors_origins or ""}}, automatic_options=True
    )


def create_argument_parser():
    """
    参数解析
    :return:
    """
    parser = argparse.ArgumentParser(description="starts the action server")
    params.add_endpoint_arguments(parser)
    utils.add_logging_option_arguments(parser)
    return parser


def create_app(
        action_package_name: Union[Text, types.ModuleType],
        cors_origins: Union[Text, List[Text], None] = "*",
        auto_reload: bool = True
) -> Sanic:
    """

    :param action_package_name:
    :param cors_origins:
    :param auto_reload:
    :return:
    """
    app = Sanic(__name__, configure_logging=True)

    configure_cors(app, cors_origins)

    # 机器人动作注册
    executor = ActionExecutor()
    executor.register_package(action_package_name)

    @app.get("/api/health")
    async def health(_) -> HTTPResponse:
        """
        检测服务是否正常
        :param _:
        :return:
        """
        body = {"status": "ok"}
        return response.json(body, status=200)

    @app.post("/api/action")
    async def chatbot_action(request: Request) -> HTTPResponse:
        """
        机器人动作执行接口
        接收DM传过来的数据
        :param request:

        :return:
        """
        action_call = request.json

        if action_call is None:
            body = {"error": "Invalid body request"}
            return response.json(body, status=400)

        result = await executor.run(action_call)

        return response.json(result, status=200)

    return app


def run(
        action_package_name: Union[Text, types.ModuleType],
        port: Union[Text, int] = DEFAULT_SERVER_PORT,
        cors_origins: Union[Text, List[Text], None] = "*",
        auto_reload: bool = True,  # 这个参数的作用
) -> None:
    """
    注意这里的
    :param action_package_name:
    :param port:
    :param cors_origins:
    :param auto_reload:
    :return:
    """
    logger.info("Starting Chatbot action endpoint server...")
    app = create_app(
        action_package_name=action_package_name,
        cors_origins=cors_origins,
        auto_reload=auto_reload
    )

    logger.info(f"Action endpoint is up and running on http://localhost:{port}")
    app.run("0.0.0.0", port, workers=utils.DEFAULT_SANIC_WORKERS, debug=True)


if __name__ == '__main__':
    run(action_package_name='action')
