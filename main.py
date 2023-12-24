import gc
import board
import time
import displayio
import terminalio
import time
import supervisor
import storage

import adafruit_requests as requests

from adafruit_datetime import datetime
from adafruit_bitmap_font import bitmap_font
from adafruit_matrixportal.matrixportal import MatrixPortal
from displayio import Bitmap
from os import getenv


def check_for_updates(info_url):
    response = requests.get(info_url)
    update_info = {
        'update_code': False,
        'update_libs': False
    }

    # Process the response as a whole
    if 'update_code = True' in response.text:
        update_info['update_code'] = True
    if 'update_libs = True' in response.text:
        update_info['update_libs'] = True

    return update_info

def download_and_save_runfile(url, filename):
    try:
        storage.remount("/", readonly=False)  # Remount filesystem as writable to change display.py file
        response = requests.get(url)
        with open(filename, "w") as file:
            file.write(response.text)
    finally:
        storage.remount("/", readonly=True)  # Important: remount as read-only after the operation



def report_error_to_server(error_message):
    flask_server_url = 'http://192.168.178.43:5000'
    try:
        response = requests.post(flask_server_url + '/report_error', data=error_message)
        print('Response from server:', response.text)
    except Exception as e:
        print('Failed to send error message:', e)


gc.collect()

#Initiate board
matrixportal = MatrixPortal(status_neopixel=board.NEOPIXEL, debug=True)

try:

    # --- WiFi Setup ---
    try:
        from secrets import secrets
    except ImportError:
        print("WiFi secrets are kept in secrets.py, please add them there!")
        raise

    print("Connecting to WiFi...")
    matrixportal.network.connect()
    print("Connected to WiFi!")


    #Update links
    info_url = 'https://raw.githubusercontent.com/schchris2211/Remote-Control-Matrix-Board/main/update_info.txt'
    display_file_url = 'https://raw.githubusercontent.com/schchris2211/Remote-Control-Matrix-Board/main/display.py'
    # lib_url = 'https://www.dropbox.com/scl/fo/f21iveuv69ls1ash5k51x/h?rlkey=2z8rgs8kpom92nf811z4kxn41&dl=0' 


    # Check for updates
    print('Checking for Updates...')

    update_info = check_for_updates(info_url)

    print('Update Info: ', update_info)


    if update_info['update_code']:
        print('Downloading new display file...')
        download_and_save_runfile(display_file_url, "/display.py")


    #Execute Run File
    exec(open("/display.py").read())


except Exception as e:
    error_message = str(e)
    report_error_to_server(error_message)
    raise  # Re-raise the exception to see it in the serial output




