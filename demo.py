import logging
from huey import SqliteHuey, crontab

huey = SqliteHuey(filename='/tmp/demo.db')

LOGGER = logging.getLogger("huey")

# TODO How to disable altogether the huey default formatter and handler?

# Add our own handler and formatter.
custom_handler = logging.StreamHandler()
custom_logformat = '[%(levelname)s:%(name)s:%(threadName)s] %(message)s'
custom_handler.setFormatter(logging.Formatter(custom_logformat))
LOGGER.addHandler(custom_handler)

@huey.task()
def add(a, b):
    return a + b

@huey.periodic_task(crontab(minute='*/1'))
def add_periodic():
    res = add(41, 1)
    LOGGER.info("Add 41 + 1 = %d", res(blocking=True))