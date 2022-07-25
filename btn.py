#!/usr/bin/env python
import time
import sys
import RPi.GPIO as GPIO


#---------------- GLOBALS ----------------#
BUTTON_A_PIN = 5
BUTTON_A_IS_PRESSED = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_A_PIN, GPIO.OUT, pull_up_down=GPIO.PUD_UP)
#------ Configuration for the matrix -----#

def loop():  
    print("button is")
    print(GPIO.input(BUTTON_A_PIN))
    if GPIO.input(BUTTON_A_PIN):
        print("pressed")
    else:
        print("not pressed")

# -------------------------------------------------- Clock : End -------------------------------------------------  

try:
    print("Press CTRL-C to stop.")
    while True:
        loop()
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit(0)
    