from pickle import NONE
from rgbmatrix import graphics
from PIL import Image
from scene import SCENES
from config import config_matrix
from datetime import datetime, timedelta

FONT_TITLE = graphics.Font()
FONT_SUBTITLE = graphics.Font()

FONT_TITLE.LoadFont("/home/jgage/code/seasons-pixel-clock/fonts/pixelclock-main-24.bdf") 
FONT_SUBTITLE.LoadFont("/home/jgage/code/seasons-pixel-clock/fonts/pixelclock-subtitle-7.bdf") 

COUNT_START = None    
COUNT_END = None
COUNT_DAY = 0
COUNT_MINUTE = 0
COUNT_HOUR = 0

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
    global SHOW_DAY_OF_WEEK
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
    global SHOW_DAY_OF_WEEK
    if B:
        SHOW_DAY_OF_WEEK = not SHOW_DAY_OF_WEEK   

#---------- Countdown ----------#
def getCountdownCanvas(cvsClock, year, month, day, hour, minute, second, weekday):
    #Clock
    strDay, strTime = getCountdownString()
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

def getCountdownString():
    global COUNT_END
    global COUNT_START
    global COUNT_DAY
    global COUNT_HOUR
    global COUNT_MINUTE

    if COUNT_START != None:
        if COUNT_START > COUNT_END:
            return "0 days", "00:00:00"

        duration = (COUNT_END- COUNT_START)
        days, seconds = duration.days, duration.seconds
        dayLabel =  "{days:02d} days".format(
            days=days
        )
        timeLabel =  datetime.datetime.strptime(str(duration),'%H:%M:%S')
        
        return dayLabel, timeLabel
    else:
        print("none")
        dayLabel =  "{days:02d} days".format(
            days=COUNT_DAY
        )
        timeLabel =  "{hour:02d}:{minute:02d}:{second:02d}".format(
            hour=COUNT_HOUR, minute=COUNT_MINUTE, second=0
        )
        return dayLabel, timeLabel

def handleButtons_Countdown(B, C, D):
    global SELECTED_OPTION
    global COUNT_END
    global COUNT_START
    global COUNT_DAY
    global COUNT_HOUR
    global COUNT_MINUTE
    if B:
        SELECTED_OPTION = SELECTED_OPTION + 1 if SELECTED_OPTION < 3 else 0
    print(SELECTED_OPTION, B, C, D)

    if SELECTED_OPTION == 0:
        if C:
            COUNT_DAY = COUNT_DAY+1
        if D:
            COUNT_DAY = COUNT_DAY-1
        COUNT_START = None
        COUNT_END = None    
    elif SELECTED_OPTION == 1:
        if C:
            COUNT_HOUR = COUNT_HOUR+1
        if D:
            COUNT_HOUR = COUNT_HOUR-1
        COUNT_START = None
        COUNT_END = None    
    elif SELECTED_OPTION == 2:
        if C:
            COUNT_MINUTE = COUNT_MINUTE+1
        if D:
            COUNT_MINUTE = COUNT_MINUTE-1
        COUNT_START = None
        COUNT_END = None    
    elif SELECTED_OPTION == 3:
        COUNT_START = datetime.now()
        print("twtrwertwe", COUNT_DAY, COUNT_HOUR)
        COUNT_END = datetime(datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour, datetime.now().minute) + timedelta(days=COUNT_DAY, hours=COUNT_HOUR, minutes=COUNT_MINUTE)
        print("Here is the output", COUNT_START, COUNT_END)

