#!/usr/bin/env python
import time
import sys
import RPi.GPIO as GPIO

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from components.notification import fetchNotification, getNotificationCanvas, getAlertCanvas, markNotificationRead
from components.clock import getClockCanvas, getCountdownCanvas, handleButtons_Clock, handleButtons_Countdown
from system.input import getInputOptions
from system.logger import debugger, boot


#---------------- GLOBALS ----------------#
ON = True
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
MATRIX = RGBMatrix(options = options)

CANVAS1 = MATRIX.CreateFrameCanvas()
CANVAS2 = MATRIX.CreateFrameCanvas()
SWITCH = False

def readyExit():
    global ON
    global MATRIX

    ON = False
    MATRIX.SwapOnVSync(MATRIX.CreateFrameCanvas())
    GPIO.cleanup()
    sys.exit(0)  

def loop():
    global MATRIX
    global CANVAS1
    global CANVAS2
    global SWITCH

    global CURRENT_PAGE
    global ALERT_NOTIFICATION

    SWITCH = not SWITCH
    canvas = CANVAS1 if SWITCH else CANVAS2

    now = time.localtime() 
    second =  now[5]

    btn_a_pressed, btn_b_pressed, btn_c_pressed, btn_d_pressed, btn_power_pressed = getInputOptions()

    if btn_power_pressed:
        readyExit()
      
    if btn_a_pressed:
        CURRENT_PAGE+=1

    if CURRENT_PAGE == 2:
        handleButtons_Countdown(btn_b_pressed, btn_c_pressed, btn_d_pressed)    
        canvas = getCountdownCanvas(canvas)
    elif CURRENT_PAGE == 1:
        ALERT_NOTIFICATION = False
        markNotificationRead() 
        canvas = getNotificationCanvas(canvas)
    else:
        CURRENT_PAGE = 0
        handleButtons_Clock(btn_b_pressed, btn_c_pressed, btn_d_pressed)
        canvas = getClockCanvas(canvas)

    if ALERT_NOTIFICATION and second % 2 == 0:
        canvas = getAlertCanvas(canvas)

    MATRIX.SwapOnVSync(canvas)
# -------------------------------------------------- Clock : End -------------------------------------------------  

boot()
last_check = None
try:
    print("Press CTRL-C to stop.")
    while ON:
        debugger()
        loop()
        time.sleep(.25)
        if last_check is None:
            last_check = time.monotonic()
        elif time.monotonic() > last_check + 60:
            last_check = time.monotonic()
            ALERT_NOTIFICATION = fetchNotification()
except KeyboardInterrupt:
    readyExit()