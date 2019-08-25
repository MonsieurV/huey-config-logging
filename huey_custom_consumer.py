#!/usr/bin/env python
import os
import sys
import logging

from huey.consumer import Consumer
from huey.consumer_options import ConsumerConfig
from huey.consumer_options import OptionParserHandler
from huey.utils import load_class

huey_logger = logging.getLogger("huey")

def disable_huey_custom_handler():
    print("handlers in huey_customer_consumer.py (before removing huey default handler):", huey_logger.handlers)
    huey_logger.handlers.pop()
    print("handlers in huey_customer_consumer.py (after removing huey default handler):", huey_logger.handlers)

def err(s):
    sys.stderr.write('\033[91m%s\033[0m\n' % s)


def load_huey(path):
    try:
        return load_class(path)
    except:
        cur_dir = os.getcwd()
        if cur_dir not in sys.path:
            sys.path.insert(0, cur_dir)
            return load_huey(path)
        err('Error importing %s' % path)
        raise


def consumer_main():
    parser_handler = OptionParserHandler()
    parser = parser_handler.get_option_parser()
    options, args = parser.parse_args()

    if len(args) == 0:
        err('Error:   missing import path to `Huey` instance')
        err('Example: huey_consumer.py app.queue.huey_instance')
        sys.exit(1)

    options = {k: v for k, v in options.__dict__.items()
               if v is not None}
    config = ConsumerConfig(**options)
    config.validate()

    huey_instance = load_huey(args[0])
    # TODO This call may be disabled by a command-line option
    # to avoid adding a custom log handler altogether?
    # But then we have no logger at all, while we just want to disable
    # the default handler.
    config.setup_logger(huey_logger)

    consumer = huey_instance.create_consumer(**config.values)
    # Disable Huey default handler.
    # TODO Could be done by user in demo.py if we make a `SIGNAL_INITIALIZED` signal
    # available (triggered after Huey consumer successful init).
    disable_huey_custom_handler()
    consumer.run()


if __name__ == '__main__':
    consumer_main()
