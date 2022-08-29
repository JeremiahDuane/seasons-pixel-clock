from rgbmatrix import graphics
from PIL import Image
from objects.scene import SCENES
from system.config import config_matrix
from datetime import datetime, timedelta

FONT_TITLE = graphics.Font()
FONT_SUBTITLE = graphics.Font()
FONT_HEADING = graphics.Font()

FONT_TITLE.LoadFont("/home/jgage/code/seasons-pixel-clock/fonts/pixelclock-main-24.bdf") 
FONT_SUBTITLE.LoadFont("/home/jgage/code/seasons-pixel-clock/fonts/pixelclock-subtitle-7.bdf") 
FONT_HEADING.LoadFont("/home/jgage/code/seasons-pixel-clock/fonts/pixelclock-heading-12.bdf") 

COUNT_START = None    
COUNT_END = None
COUNT_DAY = 0
COUNT_MINUTE = 0
COUNT_HOUR = 0

SHOW_DAY_OF_WEEK = False
SELECTED_OPTION = 0

IMAGE_INDEX = 0
TICK = 1
BLINK = False

def getImage(scene, second):
    global IMAGE_INDEX
    global TICK
    global BLINK

    if TICK >= 4:
        TICK = 1 
        BLINK = not BLINK
    else:
        TICK = TICK + 1 
 
    if TICK % scene.getTempo() == 0:
        IMAGE_INDEX = 0 if IMAGE_INDEX >= len(scene.getBMPs()) - 1 else IMAGE_INDEX + 1

    strImagePath = scene.getBMPs()[IMAGE_INDEX] 
    image = Image.open(strImagePath)
    image.thumbnail((config_matrix["width"], config_matrix["height"]), Image.ANTIALIAS)
    LAST_TICK = second
    return image

def getClockCanvas(cvsClock, year, month, day, hour, minute, second, weekday):
    #Clock
    strDate = getDateString(year, month, day, weekday)
    strHour, strColon, strMinute = getTimeString(hour, minute, second)
    strPeriod = getPeriodString(hour)
    scene = getScene(year, month, day, weekday)

    clrPrimary = graphics.Color(scene.getPrimaryColor().R,scene.getPrimaryColor().G,scene.getPrimaryColor().B) 
    clrSecondary = graphics.Color(scene.getSecondaryColor().R,scene.getSecondaryColor().G,scene.getSecondaryColor().B) 
    clrTertiary = graphics.Color(scene.getTertiaryColor().R,scene.getTertiaryColor().G,scene.getTertiaryColor().B) 
    clrQuaternary = graphics.Color(scene.getQuaternaryColor().R,scene.getQuaternaryColor().G,scene.getQuaternaryColor().B) 

    #Draw
    image = getImage(scene, second)
    cvsClock.SetImage(image.convert('RGB')) 

    action = scene.getAction()
    if action != None:
        action(graphics, cvsClock, FONT_HEADING, clrPrimary, clrSecondary, year)

    graphics.DrawText(cvsClock, FONT_TITLE, 2, 17, clrSecondary, strHour)
    graphics.DrawText(cvsClock, FONT_TITLE, 2, 18, clrPrimary, strHour)
    graphics.DrawText(cvsClock, FONT_TITLE, 20, 18, clrTertiary, strColon)
    graphics.DrawText(cvsClock, FONT_TITLE, 20, 18, clrTertiary, strColon)
    graphics.DrawText(cvsClock, FONT_TITLE, 25, 17, clrSecondary, strMinute)
    graphics.DrawText(cvsClock, FONT_TITLE, 25, 18, clrPrimary, strMinute)
    graphics.DrawText(cvsClock, FONT_TITLE, 2, 17, clrSecondary, "___")
    graphics.DrawText(cvsClock, FONT_TITLE, 2, 18, clrTertiary, "___")
    graphics.DrawText(cvsClock, FONT_SUBTITLE, 3, 29, clrQuaternary, strDate)
    graphics.DrawText(cvsClock, FONT_TITLE, 42, 17, clrQuaternary, strPeriod)

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
    global BLINK
    if hour == 0:
        hour = 12
    elif hour > 12:
        hour = hour - 12
    hourLabel =  "{hour:02d}".format(hour=hour,)
    minuteLabel =  "{minute:02d}".format(minute=minute,)
    colonLabel =  " " if BLINK else ":"

    return hourLabel, colonLabel,  minuteLabel

def getPeriodString(hours):
    periodLabel = "AM" if hours < 12 else "PM"
    return periodLabel

def handleButtons_Clock(B, C, D):
    global SHOW_DAY_OF_WEEK
    if B:
        SHOW_DAY_OF_WEEK = not SHOW_DAY_OF_WEEK   

#---------- Countdown ----------#
def getCountdownCanvas(cvsClock, year, month, day, hour, minute, second, weekday):
    global BLINK
    #Clock
    strDay, strHour, strMinute = getCountdownString()
    scene = getScene(year, month, day, weekday)

    clrPrimary = graphics.Color(scene.getPrimaryColor().R,scene.getPrimaryColor().G,scene.getPrimaryColor().B) 
    clrSecondary = graphics.Color(scene.getSecondaryColor().R,scene.getSecondaryColor().G,scene.getSecondaryColor().B) 
    white = graphics.Color(255,255,255)
    
    #Draw
    image = getImage(scene, second)
    cvsClock.SetImage(image.convert('RGB')) 

    action = scene.getAction()
    if action != None:
        action(graphics, cvsClock, FONT_HEADING, clrPrimary, clrSecondary, year)

    graphics.DrawText(cvsClock, FONT_SUBTITLE, 2, 8, clrPrimary if SELECTED_OPTION != 0 else white, strDay)
    graphics.DrawText(cvsClock, FONT_TITLE, 2, 7, clrSecondary, "___")
    graphics.DrawText(cvsClock, FONT_TITLE, 2, 8, clrPrimary, "___")
    graphics.DrawText(cvsClock, FONT_TITLE, 2, 28, clrSecondary if SELECTED_OPTION != 1 else white, strHour)
    graphics.DrawText(cvsClock, FONT_TITLE, 2, 29, clrPrimary if SELECTED_OPTION != 1 else white, strHour)
    graphics.DrawText(cvsClock, FONT_TITLE, 20, 28, clrSecondary, ":" if BLINK else "")
    graphics.DrawText(cvsClock, FONT_TITLE, 20, 29, clrPrimary, ":" if BLINK else "")
    graphics.DrawText(cvsClock, FONT_TITLE, 25, 28, clrSecondary if SELECTED_OPTION != 2 else white, strMinute)
    graphics.DrawText(cvsClock, FONT_TITLE, 25, 29, clrPrimary if SELECTED_OPTION != 2 else white, strMinute)
    
    return cvsClock

def getCountdownString():
    global COUNT_END
    global COUNT_START
    global COUNT_DAY
    global COUNT_HOUR
    global COUNT_MINUTE

    if COUNT_START != None:
        if COUNT_START > COUNT_END:
            return "00 days", "00", "00"

        duration = (COUNT_END- COUNT_START)
        days, s = duration.days, duration.seconds
        hours, remainder = divmod(s, 3600)
        minutes, seconds = divmod(remainder, 60)

        dayLabel =  "{days:02d} days".format(
            days=days
        )
        hourLabel = '{:02d}'.format(int(hours))
        minuteLabel = '{:02d}'.format(int(minutes))

        return dayLabel, hourLabel, minuteLabel
    else:
        dayLabel =  "{days:02d} days".format(
            days=COUNT_DAY
        )
        hourLabel =  "{hour:02d}".format(
            hour=COUNT_HOUR
        )
        minuteLabel =  "{minute:02d}".format(
            minute=COUNT_MINUTE
        )
        return dayLabel, hourLabel, minuteLabel

def handleButtons_Countdown(B, C, D):
    global SELECTED_OPTION
    global COUNT_END
    global COUNT_START
    global COUNT_DAY
    global COUNT_HOUR
    global COUNT_MINUTE

    if B:
        SELECTED_OPTION = SELECTED_OPTION + 1 if SELECTED_OPTION < 3 else 0

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
        if B or C or D:
            COUNT_END = datetime(datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour, datetime.now().minute) + timedelta(days=COUNT_DAY, hours=COUNT_HOUR, minutes=COUNT_MINUTE)


#---------- Shared ----------#
def getScene(year, month, day, weekday): 
    christmas = False
    thanksgiving = False
    easter = True
    birthday = False
    anniversary = False
    halloween = False
    spring = False
    summer = False
    fall = False
    winter = False


    if False:
        pass
    elif christmas:
        return SCENES[6]
    elif thanksgiving:
        return SCENES[9]
    elif easter:
        return SCENES[8]
    elif halloween:
        return SCENES[2]    
    elif anniversary:
        return SCENES[2]  
    elif birthday:
        return SCENES[2]    
    elif spring:
        return SCENES[3]
    elif summer:
        return SCENES[2]
    elif fall:
        return SCENES[5]
    elif winter:
        return SCENES[7]
    else:
        return SCENES[0]