""" futures.py """
import logging
import builtins
import atexit
import traceback
import time
from concurrent.futures import ThreadPoolExecutor
from threading import BoundedSemaphore
from inotifyt import Watcher

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

MAX_WORKERS = 4
MAX_QUEUE = MAX_WORKERS
executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)
futures = []
semaphore = BoundedSemaphore(MAX_QUEUE)

def shutdown():
    """ shutdown handler """
    try:
        traceback.print_stack()
        executor.shutdown(wait=True)
    except builtins.Exception as error:
        logger.error("Error occurred during executor shutdown: %s", error)
atexit.register(shutdown)

def executor_stats():
    """ executor_stats """
    logger.info("Executor stats: threads [%s], work_queue [%s], futures [%s]",
        executor._threads, executor._work_queue, futures)

def executor_stats_loop():
    """ executor_stats_loop """
    while True:
        executor_stats()
        time.sleep(3)

global executor_stats_loop_started
executor_stats_loop_started = False
def executor_stats_loop_start():
    """ executor_stats_loop_start """
    global executor_stats_loop_started
    if not executor_stats_loop_started:
        executor.submit(executor_stats_loop)
    executor_stats_loop_started = True

class Executor:
    """ Executor """

    @classmethod
    def submit(cls, function_cmd, *args, **kwargs):
        """ same as concurrent.futures.Executor#submit, but with queue """
        executor_stats_loop_start()
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

        futures.append(future)
        return future

    @classmethod
    def shutdown(cls, wait=True):
        """ See concurrent.futures.Executor#shutdown """
        executor.shutdown(wait)


if __name__ == "__main__":
    Executor.submit(Watcher)
