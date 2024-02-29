""" inotifyt.py """
# import inotify.adapters
import logging
from inotify_simple import INotify, masks

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
            logger.info("got events %s in %s", events, path)

if __name__ == "__main__":
    PATH = "./logs/inotify.log"
    watch(PATH)
