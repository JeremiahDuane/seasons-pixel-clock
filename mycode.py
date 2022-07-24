#!/usr/bin/env python
import time
import sys
import RPi.GPIO as GPIO
from datetime import datetime, timedelta
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image
from scene import Scene
from rgb import RGB

#---------------- GLOBALS ----------------#
MATRIX = None
FONT_TITLE = graphics.Font()
FONT_TITLE.LoadFont("/home/jgage/code/seasons-pixel-clock/fonts/pixelclock-main-24.bdf") 
FONT_SUBTITLE = graphics.Font()
FONT_SUBTITLE.LoadFont("/home/jgage/code/seasons-pixel-clock/fonts/pixelclock-subtitle-7.bdf") 

BUTTON_A_PIN = 5
BUTTON_A_IS_PRESSED = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_A_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#------ Configuration for the matrix -----#
options = RGBMatrixOptions()
options.rows = 32
options.cols =  64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat-pwm'  # If you have an Adafruit HAT: 'adafruit-hat'
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
    BUTTON_A_IS_PRESSED = GPIO.input(BUTTON_A_PIN)
    print("button is")
    if BUTTON_A_IS_PRESSED:
        print("pressed")
    else:
        print("not pressed")

    now = time.localtime() 
    strDate = getDateString(now[0],now[1],now[2],now[6])
    strTime = getTimeString(now[3],now[4],now[5])
    strPeriod = getPeriodString(now[3])
    scene = getScene(now[0],now[1],now[2],now[6])

    offscreen_canvas = matrix.CreateFrameCanvas()

    image = Image.open(scene.getBMP1() if now[5] % 2 == 0 else scene.getBMP2())
    image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
    offscreen_canvas.SetImage(image.convert('RGB'))  

    clrCurrentPrimary = graphics.Color(scene.getPrimaryColor().R,scene.getPrimaryColor().G,scene.getPrimaryColor().B) 
    clrCurrentSecondary = graphics.Color(scene.getSecondaryColor().R,scene.getSecondaryColor().G,scene.getSecondaryColor().B) 

    graphics.DrawText(offscreen_canvas, FONT_TITLE, 2, 17, clrCurrentSecondary, strTime)
    graphics.DrawText(offscreen_canvas, FONT_TITLE, 2, 18, clrCurrentPrimary, strTime)
    graphics.DrawText(offscreen_canvas, FONT_TITLE, 2, 17, clrCurrentSecondary , "___")
    graphics.DrawText(offscreen_canvas, FONT_TITLE, 2, 18, clrCurrentPrimary, "___")
    graphics.DrawText(offscreen_canvas, FONT_SUBTITLE, 3, 29, clrCurrentPrimary, strDate)
    graphics.DrawText(offscreen_canvas, FONT_TITLE, 42, 17, clrCurrentPrimary, strPeriod)

    offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
    time.sleep(.005)
    offscreen_canvas.Clear()

def getDateString(year, month, day, weekday, showDayOfWeek=False):
    dateLabel = None
    if showDayOfWeek: 
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
    
def getTimeString(hours, minutes, seconds):
    hours = hours - 12 if hours > 12 else hours 
    timeLabel =  "{zero}{hours}{colon}{minutes:02d}".format(
        zero="0" if hours < 10 else "", 
        hours=hours, minutes=minutes,
        colon=" " if seconds % 2 == 0 else ":"
    )
    return timeLabel

def getPeriodString(hours):
    periodLabel = "AM" if hours <= 11 else "PM"
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

# -------------------------------------------------- Clock : End -------------------------------------------------  

try:
    print("Press CTRL-C to stop.")
    while True:
        loop()
        time.sleep(1)

except KeyboardInterrupt:
    sys.exit(0)
