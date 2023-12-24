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


#---------------------------------- FUNCTIONS ----------------------------------

def get_current_time():
    response = requests.get('http://worldtimeapi.org/api/timezone/Etc/UTC')
    json_data = response.json()
    current_utc_time_str = json_data['datetime']
    current_utc_time = datetime.fromisoformat(current_utc_time_str)
    return current_utc_time



def update_text_and_color(index, text, color):
    matrixportal.set_text(text, index=index)
    matrixportal.set_text_color(color, index=index)


#---------------------------------- Run Script ----------------------------------


#Text Position
First_row_X = 2
First_row_Y = 12
Second_row_X = 5
Second_row_Y = 27

# Create a new label for 'Merry'
first_row = matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(First_row_X, First_row_Y),
    scrolling=False,
    text_scale=1,
)

# Create a new label for 'Christmas'
second_row = matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(Second_row_X, Second_row_Y),
    scrolling=False,
    text_scale=1,
)


update_text_and_color(first_row, 'Merry', '#cf2727')  # Red
update_text_and_color(second_row, 'Christmas', '#008000')  # Green


time_label = matrixportal.add_text(
    # text_font=terminalio.FONT,
    text_font = '/fonts/spleen-5x8.bdf',
    text_position=(matrixportal.graphics.display.width -50, 0 + 5),
)


reset_label = matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(0, (matrixportal.graphics.display.height // 2) + 10),
    scrolling=False,
    text_scale=1,
)


SCROLL_DELAY = 0.03

colors = [
    { 'color_1': '#008000',  'color_2': '#cf2727'}
]


last_displayed_time = None


while True:
    current_time = get_current_time()
    formatted_time = "{:02}:{:02}".format(current_time.hour+1, current_time.minute)

    # Update the display only if the time has changed
    if formatted_time != last_displayed_time:
        matrixportal.set_text(formatted_time, index=time_label)
        matrixportal.set_text_color('#FFFFFF')
        last_displayed_time = formatted_time


    if current_time.hour + 1 == 8 and current_time.minute == 0 and current_time.second < 30:
        # Clear previous messages
        matrixportal.set_text("", index=time_label)
        matrixportal.set_text("", index=first_row)
        matrixportal.set_text("", index=second_row)

        for remaining in range(30, 0, -1):
            matrixportal.set_text("Reset in {}".format(remaining), index=reset_label)
            time.sleep(1)

        print('Reset device...')

        time.sleep(30)
        supervisor.reload()


    if current_time.second % 10 < 5:
        # Even second: Set one color
        matrixportal.set_text_color(colors[0]['color_1'], index=first_row)
        matrixportal.set_text_color(colors[0]['color_2'], index=second_row)
    else:
        # Odd second: Set another color
        matrixportal.set_text_color(colors[0]['color_2'], index=first_row)
        matrixportal.set_text_color(colors[0]['color_1'], index=second_row)



