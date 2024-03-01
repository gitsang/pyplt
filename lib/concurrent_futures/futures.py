""" futures.py """
import time
import logging
# import builtins
from concurrent.futures import ThreadPoolExecutor
from threading import BoundedSemaphore

logger = logging.getLogger(__name__)

MAX_WORKERS = 4
MAX_QUEUE = MAX_WORKERS

executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)
semaphore = BoundedSemaphore(MAX_QUEUE)

def wait_on_b():
    """ Wait on b """
    time.sleep(5)
    print(b.result())  # b will never complete because it is waiting on a.
    return 5

def wait_on_a():
    """ Wait on a """
    time.sleep(5)
    print(a.result())  # a will never complete because it is waiting on b.
    return 6

if __name__ == "__main__":
    a = executor.submit(wait_on_b)
    b = executor.submit(wait_on_a)
