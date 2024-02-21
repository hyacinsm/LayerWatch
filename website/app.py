
from flask import Flask, render_template
from flask_apscheduler import APScheduler
from datetime import datetime

# must in be local directory
from usbcam import usbcam
from data_wrapper import data_wrapper

OFF_URL_TAG = '/off'
UPDATE_JOB_ID = 'updater'

OFFLINE_MSG = '---OFFLINE---'
ONLINE_MSG = '---ONLINE---'



# user parameters <you can change theses for your needs>

WIDTH = 400                             # in pixels
HEIGHT = 525                            # in pixels
IMAGE_PATH = '../static/images/'


# days, hours, minutes, seconds
DAYS = 0
HOURS = 0
MINUTES = 0
SECONDS = 15

cam = usbcam(width_px=WIDTH, height_px=HEIGHT,
             save_dir=IMAGE_PATH, days=DAYS, hours=HOURS, minutes=MINUTES, seconds=SECONDS)

power_off = False

app = Flask(__name__)
scheduler = APScheduler()


@app.route("/")
def base():
    str_time = datetime.now().strftime('%Y %m %d %I %M %S %p')
    data = data_wrapper(cadence=cam.seconds, status=ONLINE_MSG,
                        time=str_time, img='../static/images/right_stock_img.jpg', btn_txt='Stop Print')
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
        str_time = datetime.now().strftime('%Y %m %d %I %M %S %p')
        data = data_wrapper(cadence= -1, status= OFFLINE_MSG, time=str_time, img= '../static/images/right_stock_img.jpg', btn_txt='Cancelled')
        print(data.gen_dict())
        return render_template('index.html', **(data.gen_dict()))
    return render_template('index.html')


@scheduler.task('interval', id=UPDATE_JOB_ID, days=cam.days, hours=cam.hours, minutes=cam.minutes, seconds=cam.seconds)
def updater():
    if power_off:
        scheduler.remove_all_jobs()
    cam.recent_time = datetime.now().strftime('%Y %m %d %I %M %S %p')
    cam.log()


if __name__ == "__main__":
    scheduler.init_app(app)
    scheduler.start()
    app.run(host='0.0.0.0', port=5500, use_reloader=False,  debug=True)
