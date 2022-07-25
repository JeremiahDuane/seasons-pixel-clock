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