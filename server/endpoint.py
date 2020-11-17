# -*- coding: utf-8 -*-

"""
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   endpoint.py
 
@Time    :   2020/8/21 6:18 下午
 
@Desc    :   机器人动作（Action）服务 Action Server
 
"""

import argparse
import logging
import types
from typing import List, Text, Union

from sanic import Sanic, response
from sanic.response import HTTPResponse
from sanic.request import Request
from sanic_cors import CORS

from model import utils
from model.Executor import ActionExecutor
from model.Model_config import DEFAULT_SERVER_PORT
from model.Action import ActionExecutionRejection, ActionNotFoundException

import action

logger = logging.getLogger(__name__)


def configure_cors(
        app: Sanic, cors_origins: Union[Text, List[Text], None] = ""
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
    """Parse all the command line arguments for the run script."""

    parser = argparse.ArgumentParser(description="starts the action endpoint")
    add_endpoint_arguments(parser)
    utils.add_logging_option_arguments(parser)
    return parser


def create_app(
        action_package_name: Union[Text, types.ModuleType],
        cors_origins: Union[Text, List[Text], None] = "*",
        auto_reload: bool = False,
) -> Sanic:
    """Create a Sanic application and return it.

    Args:
        action_package_name: 需要加载的包
        cors_origins: CORS origins to allow.
        auto_reload: When `True`, auto-reloading of actions is enabled.

        # 这里让他热加载，自动注册

    Returns:
        A new Sanic application ready to be run.
    """
    app = Sanic(__name__, configure_logging=False)

    configure_cors(app, cors_origins)
    executor = ActionExecutor()
    executor.register_package(action_package_name)

    @app.get("/health")
    async def health(_) -> HTTPResponse:
        """Ping endpoint to check if the server is running and well."""
        body = {"status": "ok"}
        return response.json(body, status=200)

    @app.post("/webhook")
    async def webhook(request: Request) -> HTTPResponse:
        """
        接收DM传过来的数据
        :param request:
        :return:
        """

        action_call = request.json
        if action_call is None:
            body = {"error": "Invalid body request"}
            return response.json(body, status=400)

        # utils.check_version_compatibility(action_call.get("version"))      # 版本检查

        if auto_reload:
            executor.reload()

        try:
            result = await executor.run(action_call)
        except ActionExecutionRejection as e:
            logger.error(e)
            body = {"error": e.message, "action_name": e.action_name}
            return response.json(body, status=400)
        except ActionNotFoundException as e:
            logger.error(e)
            body = {"error": e.message, "action_name": e.action_name}
            return response.json(body, status=404)

        return response.json(result, status=200)

    @app.get("/actions")
    async def actions(_) -> HTTPResponse:
        """List all registered actions."""
        if auto_reload:
            executor.reload()

        body = [{"name": k} for k in executor.actions.keys()]
        return response.json(body, status=200)

    return app


def run(
        action_package_name: Union[Text, types.ModuleType],
        port: Union[Text, int] = DEFAULT_SERVER_PORT,
        cors_origins: Union[Text, List[Text], None] = "*",
        auto_reload: bool = True,  # 这个参数的作用
) -> None:
    logger.info("Starting Chatbot action endpoint server...")
    app = create_app(
        action_package_name, cors_origins=cors_origins, auto_reload=auto_reload
    )

    logger.info(f"Action endpoint is up and running on http://localhost:{port}")
    app.run("0.0.0.0", port, workers=utils.number_of_sanic_workers())


if __name__=='__main__':
    # python -m rasa_sdk.endpoint --actions actions
    run(action_package_name=action.actions)