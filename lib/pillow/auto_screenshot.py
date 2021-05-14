import time
import os
from PIL import ImageGrab

BASE_DIR = os.getcwd()
compress_rate = 0.5
interval = 10


def screenshot():
    local_tm = time.localtime(time.time())

    # create dir by date
    date_str = time.strftime("%Y%m%d", local_tm)
    dir_name = "screenshot_" + date_str
    dir_path = os.path.join(BASE_DIR, dir_name)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    # screenshot
    time_str = time.strftime("%Y%m%d_%H%M%S", local_tm)
    file_name = time_str + ".jpg"
    file_path = os.path.join(dir_path, file_name)
    im = ImageGrab.grab()

    # thumbnail
    if 0 < compress_rate < 1:
        w, h = im.size
        im.thumbnail((w*compress_rate, h*compress_rate))

    # save
    im.save(file_path)
    print("save: ", file_path, " size:", im.size)


if __name__ == '__main__':
    print("start auto_screenshot: ", BASE_DIR)
    while True:
        screenshot()
        time.sleep(interval)
