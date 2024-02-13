# Author: Sean Hyacinthe
# Date: 2/21/24
# Description: Automates image capture and file management with uvccapture.
# Configures capture settings, saves images with timestamps, and moves them to a specified directory.
# Utilizes subprocess for command execution and datetime for timestamping.


import subprocess

from datetime import datetime


# UVCCAPTURE  Constants
CAPTURE = 'uvccapture'
HEIGHT_FLAG = '-x'
WIDTH_FLAG = '-y'
WAIT_FLAG = '-w'
OUTPUT_FLAG = '-o'
FILE_EXT = '.jpg'


class usbcam:

    def __init__(self, width_px=240, height_px=240, save_dir='', days=0, hours=0, minutes=0, seconds=0):
        self.width = width_px
        self.height = height_px
        self.save_dir = save_dir
        self.days = days
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.recent = ''
        self.images = 0
        self.recent_time = 'Y m d I M S p'

    def create_cmd(self,*cmd_args):
        return ' '.join(list(cmd_args))

    def make_file_name(self):
        self.recent_time = datetime.now().strftime('%Y_%m_%d-%I_%M_%p')
        name = self.recent_time+FILE_EXT
        self.recent = name
        return name

    def mv_picture(self):
        cmd = self.create_cmd('mv', self.recent, self.save_dir)
        status = subprocess.run(cmd, shell=True)
        if status.returncode != 0:
            raise Exception(
                '[ERROR] could not move most recent photo to images folder...')

    def take_picture(self):
        self.images = self.images + 1
        file_name = self.make_file_name()
        cmd = self.create_cmd(CAPTURE,  OUTPUT_FLAG+file_name)
        print('\n'+cmd+'\n')
        status = subprocess.run('uvccapture -m -o'+file_name, shell=True)
        if status.returncode != 0:
            raise Exception('[ERROR] uvccapture didn\'t run sucessfully...')

    def update_picture(self):
        self.take_picture()
        self.mv_picture()

    def log(self):
        print(f'[PHOTO] {self.recent} generated')
