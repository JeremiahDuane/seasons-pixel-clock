#!/usr/bin/env python
import time
import sys
import RPi.GPIO as GPIO

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from components.notification import fetchNotification, getNotificationCanvas, getAlertCanvas
from components.clock import getClockCanvas, getCountdownCanvas, handleButtons_Clock, handleButtons_Countdown
from system.input import getInputOptions

#---------------- GLOBALS ----------------#
CURRENT_PAGE = 0
ALERT_NOTIFICATION = False

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

CANVAS1 = matrix.CreateFrameCanvas()
CANVAS2 = matrix.CreateFrameCanvas()
SWITCH = False

def loop():
    global CANVAS1
    global CANVAS2
    global SWITCH

    global CURRENT_PAGE
    global ALERT_NOTIFICATION
    global SHOW_DAY_OF_WEEK
    global COUNT_DAYS
    global COUNT_TIME

    SWITCH = not SWITCH
    canvas = CANVAS1 if SWITCH else CANVAS2

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
        handleButtons_Countdown(btn_b_pressed, btn_c_pressed, btn_d_pressed)    
        canvas = getCountdownCanvas(canvas, year, month, day, hour, minute, second, weekday)
    elif CURRENT_PAGE == 1:
        ALERT_NOTIFICATION = False
        canvas = getNotificationCanvas(canvas)
    else:
        CURRENT_PAGE = 0
        handleButtons_Clock(btn_b_pressed, btn_c_pressed, btn_d_pressed)
        canvas = getClockCanvas(canvas, year, month, day, hour, minute, second, weekday)

    if ALERT_NOTIFICATION and second % 2 == 0:
        canvas = getAlertCanvas(canvas)

    matrix.SwapOnVSync(canvas)
    time.sleep(.005)
# -------------------------------------------------- Clock : End -------------------------------------------------  

last_check = None
try:
    print("Press CTRL-C to stop.")
    while True:
        loop()
        time.sleep(.25)

        if last_check is None:
            last_check = time.monotonic()
        elif time.monotonic() > last_check + 60:
            last_check = time.monotonic()
            ALERT_NOTIFICATION = fetchNotification()
        
except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit(0)
    