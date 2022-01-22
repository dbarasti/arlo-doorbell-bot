from glob import glob
import telegram_utils
import datetime
from time import sleep
import os
import pyaarlo
from logger import logging

last_snapshot = None
running = False
arlo = None
camera = None


def setup():
    global arlo
    arlo = pyaarlo.PyArlo(username=os.environ.get('ARLO_USERNAME'),
                          password=os.environ.get('ARLO_PASSWORD'),
                          tfa_source='imap', tfa_type='email',
                          tfa_host=os.environ.get('TFA_HOST'),
                          tfa_username=os.environ.get('TFA_USERNAME'),
                          tfa_password=os.environ.get('TFA_PASSWORD'))
    telegram_utils.send_message("Arlo Doorbell system booted")


def is_running():
    return running


def send_snapshot():
    global camera
    snapshot = camera.get_snapshot()
    logging.info("Sending snapshot")
    telegram_utils.send_message(snapshot_source())
    telegram_utils.send_photo(snapshot)


def get_snapshot_file():

    global camera
    snapshot = camera.get_snapshot()
    return snapshot


def snapshot_source():
    global arlo
    return arlo.last_image_source()


def motion_detected(device, attr, value):
    global last_snapshot
    logging.info("Motion detected")
    telegram_utils.send_message("Motion detected")
    if last_snapshot is None or timeout_passed():
        send_snapshot()
        last_snapshot = datetime.datetime.now()


def timeout_passed():
    global last_snapshot
    return (datetime.datetime.now() - last_snapshot).total_seconds() > 60


def launch():
    global running, arlo, camera, last_snapshot
    try:
        setup()
        camera = arlo.cameras[1]
        camera.add_attr_callback('motionDetected', motion_detected)
        running = True
    except:
        arlo.stop()
        running = False
        last_snapshot = None
        logging.error("system shut down abruptly")
        telegram_utils.send_message("Arlo Doorbell system shut down")


def shutdown():
    global camera, last_snapshot, running, arlo
    if running:
        arlo.stop()
        telegram_utils.send_message("Arlo Doorbell system shut down")
        last_snapshot = None
        running = False
