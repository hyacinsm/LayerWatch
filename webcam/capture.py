# Author: Sean Hyacinthe
# Date: 2/21
# Description: This program automates the process of capturing images using uvccapture.
# It schedules and executes image captures every 5 seconds, continuing until a total
# of 10 images have been taken.

import subprocess
import schedule
import time

from datetime import datetime

CAPTURE = 'uvccapture'
WAIT_FLAG = '-w'
OUTPUT_FLAG = '-o'
FILE_EXT = '.jpg'

recent_file = '????'
images = 0


def make_file_name():
    recent_file = datetime.now().strftime('%Y_%m_%d-%I_%M_%p')+FILE_EXT
    return recent_file


def create_cmd(*cmd_args):
    return ' '.join(list(cmd_args))


def take_picture():
    global images
    images = images + 1
    file_name = make_file_name()
    # -o<file_name> should not have space
    cmd = create_cmd(CAPTURE,  OUTPUT_FLAG+file_name)
    status = subprocess.run('uvccapture -m -o'+file_name+'.jpg', shell=True)
    if status.returncode != 0:
        raise Exception('[ERROR] uvccapture didn\'t run successfully...')


print('running script...')

schedule.every(5).seconds.do(take_picture)
schedule.run_pending()

while images < 10:
    schedule.run_pending()
    time.sleep(1)

print('script finished...')


