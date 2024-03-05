""" inotifyt.py """
# import inotify.adapters
import os
import logging
import builtins
from inotify_simple import INotify, flags, masks

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Watcher:
    """ Watcher is a simple inotify watcher """

    def __init__(self):
        logger.info("watcher start")

        path = "./logs/inotify.log"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write('Hello, world!')
        self.watch(path)

    def on_event(self, path, event):
        """ log event """
        logger.info("%s got event %s", path, flags.from_mask(event))

    def watch(self, path):
        """ watch a path for event """
        logger.info("watching %s", path)

        try:
            i = INotify()
            i.add_watch(path, masks.ALL_EVENTS)
        except builtins.Exception as error:
            logger.info("watch failed %s", error)
            raise error

        while 1:
            logger.info("waiting for events in %s", path)
            for events in i.read():
                self.on_event(path, events[1])
                if events[1] & flags.DELETE_SELF:
                    return
