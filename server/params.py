# -*- coding: utf-8 -*-

"""
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   params.py
 
@Time    :   2020/8/22 8:40 下午
 
@Desc    :
 
"""

import argparse

from model.Model_config import DEFAULT_SERVER_PORT


def action_arg(action):
    if "/" in action:
        raise argparse.ArgumentTypeError(
            "Invalid actions format. Actions file should be a python module "
            "and passed with module notation (e.g. directory.actions)."
        )
    else:
        return action


def add_endpoint_arguments(parser):
    parser.add_argument(
        "-p",
        "--port",
        default=DEFAULT_SERVER_PORT,
        type=int,
        help="port to run the server at",
    )
    parser.add_argument(
        "--cors",
        nargs="*",
        type=str,
        help="enable CORS for the passed origin. Use * to whitelist all origins",
    )
    parser.add_argument(
        "--actions",
        type=action_arg,
        default=None,
        help="name of action package to be loaded",
    )
    parser.add_argument(
        "--auto-reload",
        help="Enable auto-reloading of modules containing Action subclasses.",
        action="store_true",
    )