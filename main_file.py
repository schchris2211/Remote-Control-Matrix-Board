import gc
import board
import time
import displayio
import terminalio
import time
import supervisor

import adafruit_requests as requests

from adafruit_datetime import datetime
from adafruit_bitmap_font import bitmap_font
from adafruit_matrixportal.matrixportal import MatrixPortal
from displayio import Bitmap
from os import getenv


def check_for_updates(info_url):
    response = requests.get(info_url, stream=True)
    update_info = {
        'update_code': False,
        'update_libs': False
    }
    for chunk in response.iter_content(chunk_size=128):
        # Process each chunk as it's downloaded
        chunk_text = chunk.decode("utf-8")
        if 'update_code = True' in chunk_text:
            update_info['update_code'] = True
        if 'update_libs = True' in chunk_text:
            update_info['update_libs'] = True

    return update_info

def download_new_run_file(url):
    response = requests.get(url)
    with open('/run_file.py', 'w') as file:
        file.write(response.text)



gc.collect()

#Initiate board
matrixportal = MatrixPortal(status_neopixel=board.NEOPIXEL, debug=True)


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
info_url = 'https://www.dropbox.com/scl/fi/3uruzvmz0rv0m3armj6o2/bool_update.txt?rlkey=bqp5v3el4kilil8mtn66pvh4s&dl=0'
code_url = 'https://www.dropbox.com/scl/fi/1tiqy823tajurbnfuf48y/code.py?rlkey=e3c1w9yvzkmr84dx26yus4eqe&dl=0'
lib_url = 'https://www.dropbox.com/scl/fo/f21iveuv69ls1ash5k51x/h?rlkey=2z8rgs8kpom92nf811z4kxn41&dl=0' 


# Check for updates
print('Checking for Updates...')

update_info = check_for_updates(info_url)

print('Update Info: ', update_info)


if update_info['update_code']:
    print('Downloading new run file...')
    download_new_run_file(code_url)


#Execute Run File
exec(open("/run_file.py").read())


