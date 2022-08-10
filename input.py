from datetime import timedelta
import time
import RPi.GPIO as GPIO

SHOW_DAY_OF_WEEK = False
COUNT = timedelta(days=0, hours=0, minutes=0)

BUTTON_A_PIN = 9 #MOSI
BUTTON_B_PIN = 10 #MISO
BUTTON_C_PIN = 11 #SCLK
BUTTON_E_PIN = 7 #CE0   
BUTTON_D_PIN = 8 #CE1

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_A_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_B_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_C_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_D_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_E_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def getInputOptions():
    cycleUp = False
    
    def handleButton(isPressed, thenDo):
        if isPressed:
            thenDo()
    def btnAHandler():
        global SHOW_DAY_OF_WEEK
        SHOW_DAY_OF_WEEK = not SHOW_DAY_OF_WEEK
        print("Button A Pressed")
    def btnBHandler():
        nonlocal cycleUp
        cycleUp = True
        print("Button B Pressed")
    def btnCHandler():
        global COUNT
        COUNT.hours = COUNT.hours + 1
        print("Button C Pressed")
    def btnDHandler():
        print("Button D Pressed")
    def btnEHandler():
        print("Button E Pressed")
        
    handleButton(not GPIO.input(BUTTON_A_PIN), btnAHandler)
    handleButton(not GPIO.input(BUTTON_B_PIN), btnBHandler)
    handleButton(not GPIO.input(BUTTON_C_PIN), btnCHandler)
    handleButton(not GPIO.input(BUTTON_D_PIN), btnDHandler)
    handleButton(not GPIO.input(BUTTON_E_PIN), btnEHandler)

    return SHOW_DAY_OF_WEEK, cycleUp, COUNT