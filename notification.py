import requests
from secrets import secrets

NOTIFICATION_IS_NEW = True

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

def getNotification():
    global NOTIFICATION_IS_NEW

    if requests != None:
        url = secrets["api_read-unread"]
        r = requests.post(url, data={}, headers={})
        data = r.json()
        r.close()

        messages = data['messages']
        if len(messages) > 0:
            for message in messages:
                currentNotification = None
                notification = Notification(message["eventId"], message["content"], message["date"])

                # Only store the newest message.
                if currentNotification == None or notification.getDate() > currentNotification.getDate():
                    currentNotification = notification
                    NOTIFICATION_IS_NEW = True
    
    print(currentNotification.getContent())
    return currentNotification