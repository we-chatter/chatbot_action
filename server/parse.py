# -*- coding: utf-8 -*-

"""
@Author  :   Xu
 
@Software:   PyCharm
 
@File    :   parse.py
 
@Time    :   2020/8/22 7:58 下午
 
@Desc    :
 
"""
import logging

from model import utils
from server.run_server import create_argument_parser, run

def main_from_args(args):
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("matplotlib").setLevel(logging.WARN)

    utils.configure_colored_logging(args.loglevel)
    utils.update_sanic_log_level()

    run(
        args.actions,
        args.port,
        args.cors,
        args.ssl_certificate
    )


def main():
    # Running as standalone python application
    arg_parser = create_argument_parser()
    cmdline_args = arg_parser.parse_args()

    main_from_args(cmdline_args)


if __name__ == "__main__":
    main()
