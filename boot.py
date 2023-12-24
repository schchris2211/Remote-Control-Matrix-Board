import board
import digitalio
import time

# Set up the LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Function to blink the LED
def blink_led(times, duration):
    for _ in range(times):
        led.value = True
        time.sleep(duration)
        led.value = False
        time.sleep(duration)

# Function to log a message
def log_message(message):
    with open('/log.txt', 'a') as log_file:
        log_file.write(message + '\n')

log_message('Boot script started.')


for _ in range(3):
    blink_count = 5
    blink_led(blink_count, 0.2)
    #log_message(f"Blinked {blink_count} times with 0.2s duration")
    time.sleep(1)

    blink_count = 2
    blink_led(blink_count, 1)
    #log_message(f"Blinked {blink_count} times with 1s duration")
    time.sleep(1)


