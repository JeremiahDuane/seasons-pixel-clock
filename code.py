#TODO adjust the char bit width to include punctuation. 

# SPDX-FileCopyrightText: 2020 John Park for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# Metro Matrix Clock
# Runs on Airlift Metro M4 with 64x32 RGB Matrix display & shield
import gc
import json
import time
import board
import displayio

from adafruit_display_text.bitmap_label import Label as BitmapLabel
from adafruit_display_text.label import Label as Label
from adafruit_bitmap_font import bitmap_font
from adafruit_matrixportal.network import Network
from adafruit_matrixportal.matrix import Matrix
from digitalio import DigitalInOut, Direction, Pull

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise
print("    Metro Minimal Clock")
print("Time will be set for {}".format(secrets["timezone"]))

# -------------------------------------------------- Setup : Start -------------------------------------------------
print(f"0: Memory : {gc.mem_free()}")

matrix = Matrix()
display = matrix.display
display.refresh(minimum_frames_per_second=0)

network = Network(status_neopixel=board.NEOPIXEL, debug=False)

btnUp = DigitalInOut(board.BUTTON_UP)
btnUp.direction = Direction.INPUT
btnUp.pull = Pull.UP

btnDown = DigitalInOut(board.BUTTON_DOWN)
btnDown.direction = Direction.INPUT
btnDown.pull = Pull.UP

# ----------------- Globals ------------------

TIME_FONT = bitmap_font.load_font("/fonts/pixelclock-main-24.bdf")
DATE_FONT = bitmap_font.load_font("/fonts/pixelclock-subtitle-7.bdf")
DEFAULT_BITMAP = displayio.OnDiskBitmap("/bmps/blank.bmp")

BLINK = False
SHOW_DAY_OF_WEEK = False
SHOW_NOTIFICATION = False
NOTIFICATION_IS_NEW = False
NOTIFICATION_IS_UNREAD = False

NOTIFICATION_MESSAGE = None
CURRENT_BITMAP1 = None
CURRENT_BITMAP2 = None

DEBUG_COUNT = 0
# ----------------- Clock Group ------------------

group = displayio.Group() 
display.show(group)

#Add loading Screen
scene_tile_grid = displayio.TileGrid(DEFAULT_BITMAP, pixel_shader=DEFAULT_BITMAP.pixel_shader)
group.append(scene_tile_grid)

time_label_shadow       = Label(TIME_FONT, x=1 , y=8)
time_label              = Label(TIME_FONT, x=1 , y=9)
underline_label         = Label(TIME_FONT, x=2 , y=9, text = "___")
underline_shadow_label  = Label(TIME_FONT, x=2 , y=8, text = "___")
period_label            = Label(TIME_FONT, x=42, y=8)
date_label              = Label(DATE_FONT, x=3 , y=26)
notification_label      = Label(TIME_FONT, x=55, y=8)

group.append(time_label_shadow)
group.append(time_label)
group.append(underline_label)
group.append(underline_shadow_label)
group.append(period_label)
group.append(date_label)   
group.append(notification_label)

print(f"1: Memory : {gc.mem_free()}")
# ----------------- Notification Group ------------------

notification_group = displayio.Group()
notification_scene_tile_grid = displayio.TileGrid(DEFAULT_BITMAP, pixel_shader=DEFAULT_BITMAP.pixel_shader)

notification_label_text = BitmapLabel(DATE_FONT, x=0, y=2)

notification_group.append(notification_scene_tile_grid)
notification_group.append(notification_label_text)

# -------------------------------------------------- Setup : End -------------------------------------------------

# -------------------------------------------------- Notification : Start -------------------------------------------------

class Notification:    
    def __init__(self, id, content, date):      
        self.id = id            
        self.content = content            
        self.date = date             
    def setId(self, id):
        self.id = id
    def getId(self):    
        return self.id
    def setContent(self, content):
        self.content = content
    def getContent(self):    
        return self.content
    def setDate(self, date):
        self.date = date
    def getDate(self):    
        return self.date

def check_notifications():
    global NOTIFICATION_IS_UNREAD
    global NOTIFICATION_IS_NEW
    global NOTIFICATION_MESSAGE
    # Emulate the api call for testing...
    r = '{"messages": [{"content": "Inspirational message. Lorem ipsum lorem ipsum doreafud fam dafeifiea mfaiefm eiafm ","eventId": "663c7f94-945f-47bc-99b5-fd6d2b0bddb3","date": "2023-03-01T19:10:10.000"},{"content": "Inspirational message. 5, but with a loooooooot of sauce safjdk fajdf akdf adhk fj kadfh afdkjhf jdkaf hdjklfa hdjfkla hdfjkladh faldkjf hasdlkf jashd","eventId": "9b315fb8-741f-438c-ae21-b21fd24dee67","date": "2023-02-02T14:10:10.000"}]}'
    data = json.loads(r)
    # #END of test #1 

    network.connect()
    requests = network.requests
    if requests != None:
        # url = secrets["api_read-unread"]
        # r = requests.post(url, data={}, headers={})
        # data = r.json()
        # r.close()

        messages = data['messages']
        if len(messages) > 0:
            for message in messages:
                notification = Notification(message["eventId"], message["content"], message["date"])

                # Only store the newest message.
                if NOTIFICATION_MESSAGE == None or notification.getDate() > NOTIFICATION_MESSAGE.getDate():
                    NOTIFICATION_MESSAGE = notification
                    NOTIFICATION_IS_NEW = True

                NOTIFICATION_IS_UNREAD = True

                del notification
        
        del messages
        del r
        del data
        gc.collect()

    
# -------------------------------------------------- Notification : End -------------------------------------------------

# -------------------------------------------------- Clock : Start -------------------------------------------------

class Scene:    
    def __init__(self, primaryColor, secondaryColor, bmp, bmp2=None):      
        self.primaryColor = primaryColor            
        self.secondaryColor = secondaryColor            
        self.bmp = bmp                                  
        self.bmp2 = bmp2        
    def setBMP(self, bmp):
        self.bmp = bmp
    def getBMP(self):    
        return self.bmp
    def setBMP2(self, bmp2):
        self.bmp = bmp2
    def getBMP2(self):    
        return self.bmp2
    def setPrimaryColor(self, primaryColor):
        self.primaryColor = primaryColor
    def getPrimaryColor(self):    
        return self.primaryColor     
    def setSecondaryColor(self, secondaryColor):
        self.secondaryColor = secondaryColor
    def getSecondaryColor(self):    
        return self.secondaryColor 

SCENES = [
    Scene(0xFFFFFF, 0xFFFFFF, "/bmps/blank.bmp", "/bmps/blank.bmp"),                 # -0-  Notification 
    Scene(0xFFFFFF, 0x40FFFF, "/bmps/snowman_1.bmp", "/bmps/snowman_2.bmp"),         # -1-  January Snowman
    Scene(0xFF9000, 0x856035, "/bmps/sunflower_1.bmp", "/bmps/sunflower_2.bmp"),     # -8-  August Sunflowers
    Scene(0xFFFFFF, 0x40FFFF, "/bmps/wreath_1.bmp", "/bmps/wreath_2.bmp")            # -12- December Wreath
]

def update_clock(year=None, month=None, day=None, hours=None, minutes=None, seconds=None, weekday=None, period=None, scene=None):  
    # ------------------- Clockface : START -------------------
    global NOTIFICATION_IS_UNREAD
    global NOTIFICATION_IS_NEW
    global NOTIFICATION_MESSAGE

    now = time.localtime()
    
    if year is None:
        year = now[0]
    if month is None:
        month = now[1]
    if day is None:
        day = now[2]
    if hours is None:
        hours = now[3]
    if minutes is None:
        minutes = now[4]
    if seconds is None:
        seconds = now[5]
    if weekday is None:
        weekday = now[6]

    if hours > 11:  # Handle times later than 12:59
        periodLabel = "PM"
    else:
        periodLabel = "AM"  
    if hours > 12:  # Handle times later than 12:59
        hours -= 12
    elif not hours:  # Handle times between 0:00 and 0:59
        hours = 12

    timeLabel =  "{zero}{hours}{colon}{minutes:02d}".format(
        zero="0" if hours < 10 else "", 
        hours=hours, minutes=minutes,
        colon=" " if BLINK else ":"
    )
    if SHOW_DAY_OF_WEEK: 
        daysOfWeek = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
        dateLabel =  "{dayOfWeek}. {zero}{day}-{zero1}{month}".format(
            zero="0" if day < 10 else "", 
            zero1="0" if month < 10 else "",
            month=month,
            dayOfWeek=daysOfWeek[weekday],
            day=day
        )
    else:
        dateLabel =  "{zero}{day}.{zero1}{month}.{year}".format(
            zero="0" if day < 10 else "", zero1="0" if month < 10 else "", year=year, month=month, day=day
        )
    
    # ----------------- Update Fields : START ------------------
    #Periodically check and see if there is a new season/theme for the scene. 
    #DO NOT RELEASE: Hardcoded as true to test update. 
    if True or (hours == 0 and minutes == 0 and seconds == 0): 
        if minutes % 2 == 0:
            print(f"--------------------------------------------------------------------------Even")
            scene = SCENES[2]
        else: 
            print(f"--------------------------------------------------------------------------Odd")
            scene = SCENES[3]

        print(f"2: Memory : {gc.mem_free()}")
        bmp = displayio.OnDiskBitmap(scene.getBMP())
        print(f"3: Memory : {gc.mem_free()}")
        bmp2 = displayio.OnDiskBitmap(scene.getBMP2())
        print(f"4: Memory : {gc.mem_free()}")

        CURRENT_BITMAP = bmp if BLINK else bmp2
        # CURRENT_BITMAP = displayio.OnDiskBitmap(scene.getBMP()) if BLINK else displayio.OnDiskBitmap(scene.getBMP2())

        del bmp
        del bmp2
        gc.collect()

        underline_label.color = scene.getPrimaryColor()
        time_label.color = scene.getPrimaryColor()
        date_label.color = scene.getPrimaryColor()
        period_label.color = scene.getPrimaryColor()
        time_label_shadow.color = scene.getSecondaryColor()
        underline_shadow_label.color = scene.getSecondaryColor()

    print(f"5: Memory : {gc.mem_free()}")
    group.pop(0)
    group.insert(0, displayio.TileGrid(CURRENT_BITMAP, pixel_shader=CURRENT_BITMAP.pixel_shader))
    
    del CURRENT_BITMAP
    gc.collect()
    print(f"6: Memory : {gc.mem_free()}")

    time_label_shadow.text = timeLabel
    time_label.text = timeLabel
    date_label.text = dateLabel
    period_label.text = periodLabel

    if NOTIFICATION_IS_NEW and BLINK:
        notification_label.text = "O" #Q for heart Icon
    else:
        notification_label.text = " "

    # ----------------- Notification Setup : START ------------------
    #Get the bit width of each character
    def getBitWidth(char):
        if char in ["M", "W", "^"]:
            return 6
        elif char in ["N"]:
            return 5
        elif char in [",", ".", "!", "[", "]", "(", ")", "'"]:
            return 3
        else:
            return 4

    #If there is a notification message that is unread. 
    if NOTIFICATION_MESSAGE != None and NOTIFICATION_IS_UNREAD:
        NOTIFICATION_IS_UNREAD = False
        
        bitCount = 0
        result = ""
        contentArr = []
        for char in NOTIFICATION_MESSAGE.getContent():
            if (bitCount + getBitWidth(char)) <= 64:
                bitCount += getBitWidth(char)
                result += char
            else:
                contentArr.append(result)
                bitCount = 0
                result = char
        contentArr.append(result.strip())

        result = ""
        for str in contentArr:
            result += str + "\n"

        notification_label_text.text = result

        del result
        del contentArr
        gc.collect()

    # ----------------- Switch between groups ------------------
    if SHOW_NOTIFICATION:
        display.show(notification_group)
    else:
        display.show(group)    

# -------------------------------------------------- Clock : End -------------------------------------------------

# -------------------------------------------------- Loop : Start -------------------------------------------------

last_check = None
last_notification_check = None

while True:
    print(f"#{DEBUG_COUNT} | {time.monotonic()}")
    DEBUG_COUNT+=1
    BLINK = not BLINK

    if not btnUp.value:
        SHOW_DAY_OF_WEEK = not SHOW_DAY_OF_WEEK
    if not btnDown.value:
        NOTIFICATION_IS_NEW = False
        SHOW_NOTIFICATION = not SHOW_NOTIFICATION
    

    if last_check is None or time.monotonic() > last_check + 3600:
        try:
            print("Updating time...")
            update_clock()                
            network.get_local_time()  # Synchronize Board's clock to Internet
            last_check = time.monotonic()
        except RuntimeError as e:
            print("Some error occured, retrying! -", e)
    if (last_notification_check is None or time.monotonic() > last_notification_check + 60): #and time.monotonic() > last_check + 120:
        try:
            print("Checking notifications...")
            check_notifications()
            last_notification_check = time.monotonic()
        except RuntimeError as e:
            print("Error making a request to AWS", e)
    
    update_clock()
    # update_clock()
    time.sleep(1)