#!/usr/bin/env python
import time
import sys
import RPi.GPIO as GPIO

from datetime import datetime, timedelta
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from notification import fetchNotification, getNotificationCanvas, getAlertCanvas
from clock import getClockCanvas, getCountdownCanvas
from input import getInputOptions

#---------------- GLOBALS ----------------#
CURRENT_PAGE = 0
ALERT_NOTIFICATION = False
SHOW_DAY_OF_WEEK = False
COUNT_DAYS = 0
COUNT_TIME = datetime(datetime.now().year,datetime.now().month,datetime.now().day, 0,0,0)    
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
    global CURRENT_PAGE
    global ALERT_NOTIFICATION
    global SHOW_DAY_OF_WEEK
    global COUNT_DAYS
    global COUNT_TIME

    display = None
    canvas = None

    now = time.localtime() 
    year = now[0]
    month = now[1]
    day = now[2]
    hour = now[3]
    minute = now[4]
    second =  now[5]
    weekday = now[6]

    btn_a_pressed, btn_b_pressed, btn_c_pressed, btn_d_pressed, btn_e_pressed = getInputOptions()

    if btn_a_pressed:
        CURRENT_PAGE+=1

    if CURRENT_PAGE == 2:
        if btn_c_pressed:
            COUNT_DAYS = COUNT_DAYS + 1
        if btn_d_pressed:
            COUNT_TIME = COUNT_TIME + timedelta(hours=1)
        if btn_e_pressed:
            COUNT_TIME = COUNT_TIME + timedelta(minutes=1)
    else:
        if btn_b_pressed:
            SHOW_DAY_OF_WEEK = not SHOW_DAY_OF_WEEK        

    clock = getClockCanvas(matrix.CreateFrameCanvas(), year, month, day, hour, minute, second, weekday, SHOW_DAY_OF_WEEK)
    notification = getNotificationCanvas(matrix.CreateFrameCanvas())
    countdown = getCountdownCanvas(matrix.CreateFrameCanvas(), year, month, day, hour, minute, second, weekday, COUNT_DAYS, COUNT_TIME)

    if CURRENT_PAGE == 2:
        canvas = countdown    
    elif CURRENT_PAGE == 1:
        canvas = notification
    else:
        CURRENT_PAGE = 0
        canvas = clock

    if ALERT_NOTIFICATION and second % 2 == 0:
        canvas = getAlertCanvas(canvas)

    display = matrix.SwapOnVSync(canvas)
    time.sleep(.005)
    display.Clear()
# -------------------------------------------------- Clock : End -------------------------------------------------  

last_check = None
debug = 0
try:
    print("Press CTRL-C to stop.")
    while True:
        loop()
        time.sleep(1)
        debug+=1
        print(debug)

        if last_check is None:
            last_check = time.monotonic()
        elif time.monotonic() > last_check + 60:
            last_check = time.monotonic()
            ALERT_NOTIFICATION = fetchNotification()
        
except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit(0)
    