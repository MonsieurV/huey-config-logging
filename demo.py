import logging
from huey import SqliteHuey, crontab

huey = SqliteHuey(filename='/tmp/demo.db')

LOGGER = logging.getLogger("huey")

# TODO How to disable altogether the huey default formatter and handler.

@huey.task()
def add(a, b):
    return a + b

@huey.periodic_task(crontab(minute='*/1'))
def add_periodic():
    res = add(41, 1)
    LOGGER.info("Add 41 + 1 = %d", res(blocking=True))