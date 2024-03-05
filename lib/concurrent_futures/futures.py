""" futures.py """
import time
import logging
import builtins
import atexit
from concurrent.futures import ThreadPoolExecutor
from threading import BoundedSemaphore
from inotifyt import Watcher

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

MAX_WORKERS = 4
MAX_QUEUE = MAX_WORKERS
executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)
semaphore = BoundedSemaphore(MAX_QUEUE)

def shutdown():
    """ shutdown """
    logger.error("shuting down")
    executor.shutdown(wait=True)
    logger.error("shutdown end")
atexit.register(shutdown)

class Executor:
    """ Executor """

    @classmethod
    def submit(cls, function_cmd, *args, **kwargs):
        """ same as concurrent.futures.Executor#submit, but with queue """
        logger.info("submit cls: %s, fn: %s", cls, function_cmd)

        # check if semaphore can be acquired, if not queue is full
        queue_not_full = semaphore.acquire(blocking=False)
        if not queue_not_full:
            logger.error("Executor queue full")
            return None

        try:
            future = executor.submit(function_cmd, *args, **kwargs)
        except builtins.Exception as error:
            logger.error("Executor task %s could not be submitted: %s", function_cmd, error)
            semaphore.release()
            raise error

        def when_finished(_):
            logger.info("Execute task %s end", function_cmd)
            semaphore.release()
        future.add_done_callback(when_finished)

        return future

    @classmethod
    def shutdown(cls, wait=True):
        """ See concurrent.futures.Executor#shutdown """
        executor.shutdown(wait)


if __name__ == "__main__":
    Executor.submit(Watcher)
