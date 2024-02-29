""" inotifyt.py """
# import inotify.adapters
import os
import logging
from inotify_simple import INotify, flags, masks

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def watch(path):
    """watch a path for event"""
    logger.info("Watching %s", path)

    i = INotify()
    i.add_watch(path, masks.ALL_EVENTS)

    while 1:
        logger.info("waiting for events in %s", path)
        for events in i.read():
            logger.info("got events %s in %s", flags.from_mask(events[1]), path)

if __name__ == "__main__":
    PATH = "./logs/inotify.log"
    os.makedirs(os.path.dirname(PATH), exist_ok=True)
    with open(PATH, 'w', encoding='utf-8') as f:
        f.write('Hello, world!')
    watch(PATH)
