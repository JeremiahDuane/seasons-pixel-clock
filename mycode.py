#!/usr/bin/env python
import time
import sys

from datetime import datetime, timedelta
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image

if len(sys.argv) < 2:
    sys.exit("Require an image argument")
else:
    image_file = sys.argv[1]

image = Image.open(image_file)

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols =  64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat-pwm'  # If you have an Adafruit HAT: 'adafruit-hat'

matrix = RGBMatrix(options = options)

# Make image fit our screen.
image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)

matrix.SetImage(image.convert('RGB'))
offscreen_canvas = matrix.CreateFrameCanvas()

font = graphics.Font()
font.LoadFont("/fonts/pixelclock-main-24.bdf") 
now = datetime.now()
current_time = now.strftime("%H")    
color_time = graphics.Color(200, 160, 15)
graphics.DrawText(offscreen_canvas, font, 1, 7, color_time ,current_time)


offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
time.sleep(.005)
offscreen_canvas.Clear()

try:
    print("Press CTRL-C to stop.")
    while True:
        time.sleep(100)

except KeyboardInterrupt:
    sys.exit(0)
