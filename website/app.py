#!/usr/bin/env python3
from flask import Flask, render_template
from flask_apscheduler import APScheduler
from datetime import datetime
import lcd as lcd16

# must in be local directory
from usbcam import usbcam
from data_wrapper import data_wrapper

OFF_URL_TAG = '/off'
UPDATE_JOB_ID = 'updater'

OFFLINE_MSG = '---OFFLINE---'
ONLINE_MSG = '---ONLINE---'

#Pin Out
# Set up GPIO for memmap
GPIO1_offset = 0x4804c000
GPIO2_offset = 0x481AC000
GPIO1_size = 0x4804cfff-GPIO1_offset
GPIO_OE = 0x134
GPIO_SETDATAOUT = 0x194
GPIO_CLEARDATAOUT = 0x190
#Pins connected to LCD
P8_26 = 1 << 29
P8_18 = 1 << 1 #GPIO_2
P8_11 = 1 << 13
P8_12 = 1 << 12
P8_15 = 1 << 15
P8_16 = 1 << 14
P9_23 = 1 << 17

RS = P8_26
E = P8_18 #GPIO_2
D4 = P8_11
D5 = P8_12
D6 = P8_15
D7 = P8_16

# user parameters <you can change theses for your needs>

WIDTH = 400                             # in pixels
HEIGHT = 525                            # in pixels
IMAGE_PATH = '/home/debian/LayerWatch/website/static/images/'
STATIC_PATH = '../static/images/'


# days, hours, minutes, seconds
DAYS = 0
HOURS = 0
MINUTES = 0
SECONDS = 15

cam = usbcam(width_px=WIDTH, height_px=HEIGHT,
             save_dir=IMAGE_PATH, days=DAYS, hours=HOURS, minutes=MINUTES, seconds=SECONDS)
lcd = lcd16.lcd(RS=RS, E=E, D4=D4, D5=D5,D6=D6, D7=D7, 
                enable_offset= GPIO2_offset, chip_offset = GPIO1_offset, gpio_size = GPIO1_size, relay_pin= P9_23)

lcd.setup_pins()
lcd.setup_pin_enable()
lcd.setup_commands()

lcd.write_string("http://172.22.166.50:5051")
lcd.toggle_relay()

power_off = False

app = Flask(__name__)
scheduler = APScheduler()


@app.route("/")
def base():
    str_time = datetime.now().strftime('%Y %m %d %I %M %S %p')
    data = data_wrapper(cadence=cam.seconds, status=ONLINE_MSG,
                        time=str_time, img=STATIC_PATH+cam.recent, btn_txt='Stop Print')
    print('base')
    print(data.gen_dict())
    return render_template('index.html', **data.gen_dict())


@app.route('/<action>')
def shutdown(action):
    print('shutdown')
    if action.lower().strip() == 'off':
        print('should power off relay')
        global power_off
        power_off = True
        lcd.toggle_relay()
        str_time = datetime.now().strftime('%Y %m %d %I %M %S %p')
        data = data_wrapper(cadence= -1, status= OFFLINE_MSG, time=str_time, img=STATIC_PATH+cam.recent , btn_txt='Cancelled')
        print(data.gen_dict())
        return render_template('index.html', **(data.gen_dict()))
    return render_template('index.html')


@scheduler.task('interval', id=UPDATE_JOB_ID, days=cam.days, hours=cam.hours, minutes=cam.minutes, seconds=cam.seconds)
def updater():
    if power_off:
        scheduler.remove_all_jobs()
        lcd.mem_close()
    cam.update_picture()
    cam.log()


if __name__ == "__main__":
    scheduler.init_app(app)
    scheduler.start()
    app.run(host='0.0.0.0', port=5500, use_reloader=False,  debug=True)
