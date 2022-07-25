import time
from rgbmatrix import graphics
from PIL import Image
from scene import Scene
from rgb import RGB
from config import matrix

FONT_TITLE = graphics.Font()
FONT_SUBTITLE = graphics.Font()

FONT_TITLE.LoadFont("/home/jgage/code/seasons-pixel-clock/fonts/pixelclock-main-24.bdf") 
FONT_SUBTITLE.LoadFont("/home/jgage/code/seasons-pixel-clock/fonts/pixelclock-subtitle-7.bdf") 

def getClockCanvas(cvsClock, showDayOfWeek=False):
    #Clock
    now = time.localtime() 
    year = now[0]
    month = now[1]
    day = now[2]
    hour = now[3]
    minute = now[4]
    second =  now[5]
    weekday = now[6]
    
    strDate = getDateString(year, month, day, weekday, showDayOfWeek)
    strTime = getTimeString(hour, minute, second)
    strPeriod = getPeriodString(hour)
    scene = getScene(year, month, day, weekday)

    #Scene
    clrPrimary = graphics.Color(scene.getPrimaryColor().R,scene.getPrimaryColor().G,scene.getPrimaryColor().B) 
    clrSecondary = graphics.Color(scene.getSecondaryColor().R,scene.getSecondaryColor().G,scene.getSecondaryColor().B) 
    strImagePath = scene.getBMP1() if second % 2 == 0 else scene.getBMP2()

    #Draw
    image = Image.open(strImagePath)
    image.thumbnail((matrix["width"], matrix["height"]), Image.ANTIALIAS)
    cvsClock.SetImage(image.convert('RGB'))  

    graphics.DrawText(cvsClock, FONT_TITLE, 2, 17, clrSecondary, strTime)
    graphics.DrawText(cvsClock, FONT_TITLE, 2, 18, clrPrimary, strTime)
    graphics.DrawText(cvsClock, FONT_TITLE, 2, 17, clrSecondary, "___")
    graphics.DrawText(cvsClock, FONT_TITLE, 2, 18, clrPrimary, "___")
    graphics.DrawText(cvsClock, FONT_SUBTITLE, 3, 29, clrPrimary, strDate)
    graphics.DrawText(cvsClock, FONT_TITLE, 42, 17, clrPrimary, strPeriod)

    return cvsClock

def getDateString(year, month, day, weekday, showDayOfWeek):
    dateLabel = None
    if showDayOfWeek: 
        dateLabel =  "{dayOfWeek} {zero}{day}-{zero1}{month}".format(
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
        scene = scenes[1]

    return scene
