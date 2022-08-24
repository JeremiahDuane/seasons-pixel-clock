from objects.rgb import RGB

class Scene:    
    def __init__(self, primaryColor, secondaryColor, bmp, bmp2=None, action=None):      
        self.primaryColor = primaryColor            
        self.secondaryColor = secondaryColor            
        self.bmp = bmp                                  
        self.bmp2 = bmp2     
        self.action = action   
    def setBMP1(self, bmp):
        self.bmp = bmp
    def getBMP1(self):    
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
    def setAction(self, action):
        self.action = action    
    def getAction(self):
        return self.action

def BirthdayAction(graphics, canvas, font, clrPrimary, clrSecondary, year):
    color = graphics.Color(200,200,255)
    graphics.DrawText(canvas, font, 47, 20, color, str(year-1997))
    graphics.DrawText(canvas, font, 47, 21, color, str(year-1997))

SCENES = [
    Scene(RGB(255,255,255), RGB(255,255,255), "./bmps/blank.bmp", "./bmps/blank.bmp"),                 # -0-  Notification 
    Scene(RGB(255,255,255), RGB(0,255,255), "./bmps/snowman_1.bmp", "./bmps/snowman_2.bmp"),         # -1-  January Snowman
    #Scene(RGB(200,190,0), RGB(255,190,0), "./bmps/sunflower_1.bmp", "./bmps/sunflower_2.bmp"),     # -8-  August Sunflowers
    Scene(RGB(255,255,255), RGB(255,150,255), "./bmps/pinkcake_1.bmp", "./bmps/pinkcake_2.bmp", BirthdayAction),     # -8-  August Sunflowers
    Scene(RGB(255,255,255), RGB(0,255,255), "./bmps/wreath_1.bmp", "./bmps/wreath_2.bmp")            # -12- December Wreath
]