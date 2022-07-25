#!/usr/bin/env python
import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from notification import getNotification
import RPi.GPIO as GPIO

from clock import getClockCanvas
from input import getInputOptions

#---------------- GLOBALS ----------------#
CURRENT_NOTIFICATION = None

#------ Configuration for the matrix -----#
options = RGBMatrixOptions()
options.rows = 32
options.cols =  64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'
options.pwm_lsb_nanoseconds = 130
#  options.chain_length = 1
#  options.parallel = 1
#  options.row_address_type = 0
options.multiplexing = 0
#options.pwm_bits = 11
options.brightness = 100
#  options.pwm_lsb_nanoseconds = 130
options.led_rgb_sequence = 'RGB'
#  options.pixel_mapper_config = ''
options.gpio_slowdown = 3
options.drop_privileges = False
matrix = RGBMatrix(options = options)

def loop():
    showDayOfWeek = getInputOptions()
    clock = getClockCanvas(showDayOfWeek)

    clock = matrix.SwapOnVSync(clock)
    time.sleep(.005)
    clock.Clear()
# -------------------------------------------------- Clock : End -------------------------------------------------  

last_check = None
try:
    print("Press CTRL-C to stop.")
    while True:
        loop()
        time.sleep(1)
        if last_check is None:
            last_check = time.monotonic()
        elif time.monotonic() > last_check + 60:
            last_check = time.monotonic()
            CURRENT_NOTIFICATION = getNotification()
        
except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit(0)
    