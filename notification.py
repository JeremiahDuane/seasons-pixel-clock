import imp
import requests
from rgbmatrix import graphics
from PIL import Image
from scene import SCENES
from config import matrix
from secrets import secrets

NOTIFICATION_IS_NEW = True
CURRENT_NOTIFICATION = None

FONT_SUBTITLE = graphics.Font()
FONT_SUBTITLE.LoadFont("/home/jgage/code/seasons-pixel-clock/fonts/pixelclock-subtitle-7.bdf") 

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

def fetchNotification():
    global NOTIFICATION_IS_NEW

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

def getNotificationCanvas(cvsNotification):
    arrContent = getContentString()

    #Scene
    scene = SCENES[0]
    clrPrimary = graphics.Color(scene.getPrimaryColor().R,scene.getPrimaryColor().G,scene.getPrimaryColor().B) 
    clrSecondary = graphics.Color(scene.getSecondaryColor().R,scene.getSecondaryColor().G,scene.getSecondaryColor().B) 
    strImagePath = scene.getBMP1()

    #Draw
    image = Image.open(strImagePath)
    image.thumbnail((matrix["width"], matrix["height"]), Image.ANTIALIAS)
    cvsNotification.SetImage(image.convert('RGB'))  

    i = 0
    for line in arrContent:
        i+=1
        graphics.DrawText(cvsNotification, FONT_SUBTITLE, 1, i*6, clrPrimary, line)

    return cvsNotification

def getContentString():
    contentArr = []

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
    if CURRENT_NOTIFICATION != None:        
        bitCount = 0
        result = ""
        for char in CURRENT_NOTIFICATION.getContent():
            if (bitCount + getBitWidth(char)) <= 64:
                bitCount += getBitWidth(char)
                result += char
            else:
                contentArr.append(result)
                bitCount = 0
                result = char
        contentArr.append(result.strip())
    else:
        contentArr = ["No messages, or", "messages are", "loading..."]

    return contentArr
