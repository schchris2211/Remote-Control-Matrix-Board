import gc
import board
import time
import displayio
import terminalio
import time
import supervisor
import storage
import json
import os

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


def update_display_file(url, filename):
    try:
        storage.remount("/", readonly=False)  # Remount filesystem as writable to change display.py file
        response = requests.get(url)
        with open(filename, "w") as file:
            file.write(response.text)
    finally:
        storage.remount("/", readonly=True)  # Important: remount as read-only after the operation


# def update_lib_list(list_url):
#     try:
#         response = requests.get(list_url)
#         library_list = []
#         file_markers = [f'file {i}' for i in range(1, 11)]  # Markers for 'file 1' to 'file 10'

#         for marker in file_markers:
#             if marker in response.text:
#                 start = response.text.find(marker) + len(marker)
#                 end = response.text.find('\n', start)
#                 line = response.text[start:end].strip()
#                 parts = line.split('\t')
#                 if len(parts) >= 2:
#                     library_list.append((parts[0], parts[1]))  # Append URL and file/folder type

#         return library_list

#     except MemoryError:
#         print("Memory error occurred")
#     except Exception as e:
#         print("Error:", e)
#         return []

# def update_libraries(dir_url, lib_list):
#     try:
#         local_libs = os.listdir("/lib")
#         print('Lib List: \n', local_libs)

#         github_list = []
#         response = requests.get(url)
#         print(response.text)
#         files = json.loads(response.text)

#         for file in files:
#             lib_type = 'folder' if file['type'] == 'dir' else 'file'
#             lib_name = file['name']

#             if lib_type == 'file' and lib_name.endswith('.mpy'):
#                 lib_type = 'mpy'

#             github_list.append((lib_name, lib_type))

#         print('GitHub Lib List: \n', github_list)

#     except MemoryError:
#         print("Memory error occurred")
#     except Exception as e:
#         print("Error:", e)


def report_error_to_server(error_message):
    flask_server_url = 'http://192.168.178.43:5000'
    try:
        response = requests.post(flask_server_url + '/report_error', data=error_message)
        print('Response from server:', response.text)
    except Exception as e:
        print('Failed to send error message:', e)


gc.collect()

#Initiate board
matrixportal = MatrixPortal(status_neopixel=board.NEOPIXEL, debug=True, rotation = 180)

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
    lib_dir_url = 'https://github.com/schchris2211/Remote-Control-Matrix-Board/tree/c5a181d02b93a7c747b0e9216c5a1f5a7f19249e/lib_update' 
    lib_list_url = 'https://github.com/schchris2211/Remote-Control-Matrix-Board/blob/ce999c40f029f7b8cf340adef67bcaaad202bcac/update_lib_list.txt'

    # Check for updates
    print('Checking for Updates...')

    update_info = check_for_updates(info_url)

    print('Update Info: ', update_info)


    if update_info['update_code']:
        print('Updating display file...')
        update_display_file(display_file_url, "/display.py")

    # if update_info['update_libs']:
    #     print('Updating libraries...')
    #     update_liblist = update_lib_list(lib_list_url)
    #     print(update_liblist)
    #     update_libraries(lib_url, update_liblist)

    #Execute Run File
    exec(open("/display.py").read())


except Exception as e:
    error_message = str(e)
    report_error_to_server(error_message)
    raise  # Re-raise the exception to see it in the serial output




