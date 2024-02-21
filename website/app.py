
from flask import Flask, render_template
from flask_apscheduler import APScheduler
from datetime import datetime
from usbcam import usbcam


IMAGE_PATH = '../static/images/'
UPDATE_JOB_ID = 'updater'

cam = usbcam(width_px=400, height_px=525, save_dir=IMAGE_PATH)

app = Flask(__name__)
scheduler = APScheduler()

@app.route("/")
def base():

    render_data = {
        'print_num': '---Printer 1---',
        'print_one_log': 'Recent Log: ' + cam.recent_time,
        'print_img': '../static/images/right_stock_img.jpg',
    }
    return render_template('index.html', **render_data)


@app.route("/<action>")
def action(action):

    if action.lower().strip() == 'off':
        # should turn off relay here
        print('should power off relay')
        scheduler.remove_all_jobs()
        str_time = datetime.now().strftime('%Y %m %d %I %M %S %p')
        render_data = {
            'print_num': '--OFFLINE--',
            'print_one_log': ' Last Log:' + str_time,
            'print_img': '../static/images/right_stock_img.jpg',
        }
        return render_template('index.html', **render_data)
    return render_template('index.html')


@scheduler.task('interval',id=UPDATE_JOB_ID, seconds=15)
def updater():
    cam.recent_time = datetime.now().strftime('%Y %m %d %I %M %S %p')
    cam.debug('Task ran...')


if __name__ == "__main__":
    scheduler.init_app(app)
    scheduler.start()
    app.run(host='0.0.0.0', port=5500, debug=True)

