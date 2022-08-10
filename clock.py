from rgbmatrix import graphics
from PIL import Image
from scene import SCENES
from config import config_matrix
from datetime import datetime, timedelta

FONT_TITLE = graphics.Font()
FONT_SUBTITLE = graphics.Font()

FONT_TITLE.LoadFont("/home/jgage/code/seasons-pixel-clock/fonts/pixelclock-main-24.bdf") 
FONT_SUBTITLE.LoadFont("/home/jgage/code/seasons-pixel-clock/fonts/pixelclock-subtitle-7.bdf") 

COUNT_DAYS = 0
COUNT_TIME = datetime(datetime.now().year,datetime.now().month,datetime.now().day, 0,0,0)    
SHOW_DAY_OF_WEEK = False
SELECTED_OPTION = 0
def getClockCanvas(cvsClock, year, month, day, hour, minute, second, weekday):
    #Clock
    strDate = getDateString(year, month, day, weekday)
    strTime = getTimeString(hour, minute, second)
    strPeriod = getPeriodString(hour)
    scene = getScene(year, month, day, weekday)

    #Scene
    clrPrimary = graphics.Color(scene.getPrimaryColor().R,scene.getPrimaryColor().G,scene.getPrimaryColor().B) 
    clrSecondary = graphics.Color(scene.getSecondaryColor().R,scene.getSecondaryColor().G,scene.getSecondaryColor().B) 
    strImagePath = scene.getBMP1() if second % 2 == 0 else scene.getBMP2()

    #Draw
    image = Image.open(strImagePath)
    image.thumbnail((config_matrix["width"], config_matrix["height"]), Image.ANTIALIAS)
    cvsClock.SetImage(image.convert('RGB'))  

    graphics.DrawText(cvsClock, FONT_TITLE, 2, 17, clrSecondary, strTime)
    graphics.DrawText(cvsClock, FONT_TITLE, 2, 18, clrPrimary, strTime)
    graphics.DrawText(cvsClock, FONT_TITLE, 2, 17, clrSecondary, "___")
    graphics.DrawText(cvsClock, FONT_TITLE, 2, 18, clrPrimary, "___")
    graphics.DrawText(cvsClock, FONT_SUBTITLE, 3, 29, clrPrimary, strDate)
    graphics.DrawText(cvsClock, FONT_TITLE, 42, 17, clrPrimary, strPeriod)

    return cvsClock

def getDateString(year, month, day, weekday):
    dateLabel = None
    if SHOW_DAY_OF_WEEK: 
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
    timeLabel =  "{hour:02d}{colon}{minute:02d}".format(
        hour=hour, minute=minute,
        colon=" " if second % 2 == 0 else ":"
    )
    return timeLabel

def getPeriodString(hours):
    periodLabel = "AM" if hours < 12 else "PM"
    return periodLabel

def getScene(year, month, day, weekday): 
    IsSpring = False
    IsSummer = True
    IsFall = False
    IsWinter = False

    if IsSummer:
        scene = SCENES[2]
    else: 
        scene = SCENES[1]

    return scene

def handleButtons_Clock(B, C, D):
    if B:
        SHOW_DAY_OF_WEEK = not SHOW_DAY_OF_WEEK   

#---------- Countdown ----------#
def getCountdownCanvas(cvsClock, year, month, day, hour, minute, second, weekday):
    global COUNT_DAYS
    global COUNT_TIME

    #Clock
    strTime = getCountdownTimeString(COUNT_TIME.hour, COUNT_TIME.minute, COUNT_TIME.second)
    strDay = getCountdownDayString(COUNT_DAYS)
    scene = getScene(year, month, day, weekday)

    #Scene
    clrPrimary = graphics.Color(scene.getPrimaryColor().R,scene.getPrimaryColor().G,scene.getPrimaryColor().B) 
    clrSecondary = graphics.Color(scene.getSecondaryColor().R,scene.getSecondaryColor().G,scene.getSecondaryColor().B) 

    #Draw
    graphics.DrawText(cvsClock, FONT_TITLE, 1, 14, clrSecondary, strDay)
    graphics.DrawText(cvsClock, FONT_TITLE, 1, 15, clrPrimary, strDay)
    graphics.DrawText(cvsClock, FONT_TITLE, 1, 31, clrSecondary, strTime)
    graphics.DrawText(cvsClock, FONT_TITLE, 1, 32, clrPrimary, strTime)

    return cvsClock

def getCountdownDayString(days):
    timeLabel =  "{days:02d} remaining".format(
        days=days
    )
    return timeLabel

def getCountdownTimeString(hour, minute, second):
    timeLabel =  "{hour:02d}:{minute:02d}:{second:02d}".format(
        hour=hour, minute=minute, second=second
    )
    return timeLabel

def handleButtons_Countdown(B, C, D):
    global SELECTED_OPTION
    def addDay():
        global COUNT_DAYS
        COUNT_DAYS = COUNT_DAYS + 1
        print("Adding days", COUNT_DAYS)
    def remDay():
        global COUNT_DAYS
        COUNT_DAYS = COUNT_DAYS - 1
    def addHour():
        global COUNT_TIME
        COUNT_TIME = COUNT_TIME + timedelta(hours=1)
    def remHour():        
        global COUNT_TIME
        COUNT_TIME = COUNT_TIME - timedelta(hours=1)
    def addMinute():
        global COUNT_TIME
        COUNT_TIME = COUNT_TIME + timedelta(minutes=1)
    def remMinute():
        global COUNT_TIME
        COUNT_TIME = COUNT_TIME - timedelta(minutes=1)           

    if B:
        SELECTED_OPTION = SELECTED_OPTION + 1 if SELECTED_OPTION < 3 else 0
    print(SELECTED_OPTION, B, C, D)
    if C:
        if SELECTED_OPTION == 1:
           addDay()
        elif SELECTED_OPTION == 2:
            addHour()
        elif SELECTED_OPTION == 3:
            addMinute()
    if D:
        if SELECTED_OPTION == 1:
           remDay()
        elif SELECTED_OPTION == 2:
            remHour()
        elif SELECTED_OPTION == 3:
            remMinute()
