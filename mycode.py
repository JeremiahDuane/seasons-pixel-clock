#!/usr/bin/env python
import time
import sys
import RPi.GPIO as GPIO
import requests

from datetime import datetime, timedelta
from code import SHOW_DAY_OF_WEEK
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image
from scene import Scene
from notification import Notification
from rgb import RGB
from secrets import secrets

#---------------- GLOBALS ----------------#
MATRIX = None
FONT_TITLE = graphics.Font()
FONT_TITLE.LoadFont("/home/jgage/code/seasons-pixel-clock/fonts/pixelclock-main-24.bdf") 
FONT_SUBTITLE = graphics.Font()
FONT_SUBTITLE.LoadFont("/home/jgage/code/seasons-pixel-clock/fonts/pixelclock-subtitle-7.bdf") 

BUTTON_A_PIN = 24

NOTIFICATION_IS_UNREAD = True
CURRENT_NOTIFICATION = None

SHOW_DAY_OF_WEEK = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_A_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
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
    btnAIsPressed = not GPIO.input(BUTTON_A_PIN)
    handleButton(btnAIsPressed, btnAHandler)

    #Clock
    now = time.localtime() 
    year = now[0]
    month = now[1]
    day = now[2]
    hour = now[3]
    minute = now[4]
    second =  now[5]
    weekday = now[6]
    
    strDate = getDateString(year, month, day, weekday)
    strTime = getTimeString(hour, minute, second)
    strPeriod = getPeriodString(hour)
    scene = getScene(year, month, day, weekday)

    #Scene
    clrCurrentPrimary = graphics.Color(scene.getPrimaryColor().R,scene.getPrimaryColor().G,scene.getPrimaryColor().B) 
    clrCurrentSecondary = graphics.Color(scene.getSecondaryColor().R,scene.getSecondaryColor().G,scene.getSecondaryColor().B) 
    currentImagePath = scene.getBMP1() if now[5] % 2 == 0 else scene.getBMP2()

    #Draw
    drawToMatrix(clrCurrentPrimary, clrCurrentSecondary, currentImagePath, strTime, strDate, strPeriod)

def getDateString(year, month, day, weekday):
    global SHOW_DAY_OF_WEEK
    dateLabel = None
    if SHOW_DAY_OF_WEEK: 
        dateLabel =  "{dayOfWeek}. {zero}{day}-{zero1}{month}".format(
            zero="0" if day < 10 else "", 
            zero1="0" if month < 10 else "",
            month=month,
            dayOfWeek=["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"][weekday],
            day=day
        )
    else:
        dateLabel =  "{zero}{day}.{zero1}{month}.{year}".format(
            zero="0" if day < 10 else "", zero1="0" if month < 10 else "", year=year, month=month, day=day
        )
        return dateLabel
    
def getTimeString(hour, minute, second):
    if hour == 0:
        hour = 12
    elif hour > 12:
        hour = hour - 12
    timeLabel =  "{zero}{hour}{colon}{minute:02d}".format(
        zero="0" if hour < 10 else "", 
        hour=hour, minute=minute,
        colon=" " if second % 2 == 0 else ":"
    )
    return timeLabel

def getPeriodString(hours):
    periodLabel = "AM" if hours < 12 else "PM"
    return periodLabel

def getScene(year, month, day, weekday):
    scenes = [
        Scene(RGB(255,255,255), RGB(255,255,255), "./bmps/blank.bmp", "./bmps/blank.bmp"),                 # -0-  Notification 
        Scene(RGB(255,255,255), RGB(0,255,255), "./bmps/snowman_1.bmp", "./bmps/snowman_2.bmp"),         # -1-  January Snowman
        Scene(RGB(200,190,0), RGB(255,190,0), "./bmps/sunflower_1.bmp", "./bmps/sunflower_2.bmp"),     # -8-  August Sunflowers
        Scene(RGB(255,255,255), RGB(0,255,255), "./bmps/wreath_1.bmp", "./bmps/wreath_2.bmp")            # -12- December Wreath
    ]
    
    IsSpring = False
    IsSummer = True
    IsFall = False
    IsWinter = False

    if IsSummer:
        scene = scenes[2]
    else: 
        scene = scenes[3]

    return scene

def drawToMatrix(clrPrimary, clrSecondary, strImagePath, strTime, strDate, strPeriod):
    offscreen_canvas = matrix.CreateFrameCanvas()

    image = Image.open(strImagePath)
    image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
    offscreen_canvas.SetImage(image.convert('RGB'))  

    graphics.DrawText(offscreen_canvas, FONT_TITLE, 2, 17, clrSecondary, strTime)
    graphics.DrawText(offscreen_canvas, FONT_TITLE, 2, 18, clrPrimary, strTime)
    graphics.DrawText(offscreen_canvas, FONT_TITLE, 2, 17, clrSecondary, "___")
    graphics.DrawText(offscreen_canvas, FONT_TITLE, 2, 18, clrPrimary, "___")
    graphics.DrawText(offscreen_canvas, FONT_SUBTITLE, 3, 29, clrPrimary, strDate)
    graphics.DrawText(offscreen_canvas, FONT_TITLE, 42, 17, clrPrimary, strPeriod)

    offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
    time.sleep(.005)
    offscreen_canvas.Clear()

def check_notifications():
    global NOTIFICATION_IS_NEW
    global CURRENT_NOTIFICATION

    if requests != None:
        url = secrets["api_read-unread"]
        r = requests.post(url, data={}, headers={})
        data = r.json()
        r.close()

        messages = data['messages']
        if len(messages) > 0:
            for message in messages:
                notification = Notification(message["eventId"], message["content"], message["date"])

                # Only store the newest message.
                if CURRENT_NOTIFICATION == None or notification.getDate() > CURRENT_NOTIFICATION.getDate():
                    CURRENT_NOTIFICATION = notification
                    NOTIFICATION_IS_NEW = True
    
    print(CURRENT_NOTIFICATION.getContent())

def handleButton(isPressed, thenDo):
    if isPressed:
        thenDo()

def btnAHandler():
    global SHOW_DAY_OF_WEEK
    SHOW_DAY_OF_WEEK = not SHOW_DAY_OF_WEEK
    print("Button was pressed")
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
            check_notifications()
        
except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit(0)
    