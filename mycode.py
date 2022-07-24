#!/usr/bin/env python
import time
import sys

from datetime import datetime, timedelta
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image

#---------------- START: GLOBALS ----------------#
MATRIX = None
FONT_TITLE = graphics.Font()
FONT_TITLE.LoadFont("/home/jgage/code/seasons-pixel-clock/fonts/pixelclock-main-24.bdf") 
FONT_SUBTITLE = graphics.Font()
FONT_SUBTITLE.LoadFont("/home/jgage/code/seasons-pixel-clock/fonts/pixelclock-subtitle-7.bdf") 
#------ START: Configuration for the matrix -----#
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
    now = time.localtime() 
    strDate = parseDateString(now[0],now[1],now[2],now[6])
    strTime, strPeriod = parseTimeString(now[3],now[4],now[5])

    offscreen_canvas = matrix.CreateFrameCanvas()
    clrCurrentPrimary = graphics.Color(200, 160, 15)
    clrCurrentSecondary = graphics.Color(240, 120, 15)
    strImagePath = "/home/jgage/code/seasons-pixel-clock/bmps/sunflower_1.bmp"
    image = Image.open(strImagePath)
    image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
    offscreen_canvas.SetImage(image.convert('RGB'))  

    graphics.DrawText(offscreen_canvas, FONT_TITLE, 2, 17, clrCurrentSecondary , strTime)
    graphics.DrawText(offscreen_canvas, FONT_TITLE, 2, 18, clrCurrentPrimary , strTime)
    graphics.DrawText(offscreen_canvas, FONT_TITLE, 2, 17, clrCurrentSecondary , "___")
    graphics.DrawText(offscreen_canvas, FONT_TITLE, 2, 18, clrCurrentPrimary , "___")
    graphics.DrawText(offscreen_canvas, FONT_SUBTITLE, 3, 29, clrCurrentPrimary , strDate)
    graphics.DrawText(offscreen_canvas, FONT_TITLE, 42, 17, clrCurrentPrimary , strPeriod)

    offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
    time.sleep(.005)
    offscreen_canvas.Clear()

def parseDateString(year, month, day, weekday, showDayOfWeek=False):
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
    
def parseTimeString(hours, minutes, seconds):
    periodLabel = "AM" if hours <= 11 else "PM"
    hours = hours - 12 if hours > 12 else hours 
    timeLabel =  "{zero}{hours}{colon}{minutes:02d}".format(
        zero="0" if hours < 10 else "", 
        hours=hours, minutes=minutes,
        colon=" " if seconds % 2 == 0 else ":"
    )
    return timeLabel, periodLabel

# -------------------------------------------------- Clock : End -------------------------------------------------  

try:
    print("Press CTRL-C to stop.")
    while True:
        loop()
        time.sleep(1)

except KeyboardInterrupt:
    sys.exit(0)
