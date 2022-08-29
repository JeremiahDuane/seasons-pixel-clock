from objects.rgb import RGB

class Scene:    
    def __init__(self, primaryColor, secondaryColor, bmps, tempo, action=None):      
        self.primaryColor = primaryColor            
        self.secondaryColor = secondaryColor
        # self.tertiaryColor = tertiaryColor           
        self.bmps = bmps                                  
        self.tempo = tempo
        self.action = action
    def setBMPs(self, bmps):
        self.bmps = bmps
    def getBMPs(self):    
        return self.bmps
    def setPrimaryColor(self, primaryColor):
        self.primaryColor = primaryColor
    def getPrimaryColor(self):    
        return self.primaryColor     
    def setSecondaryColor(self, secondaryColor):
        self.secondaryColor = secondaryColor
    def getSecondaryColor(self):    
        return self.secondaryColor    
    # def setTertiaryColor(self, tertiaryColor):
    #     self.tertiaryColor = tertiaryColor
    # def getTertiaryColor(self):    
    #     return self.tertiaryColor
    def setTempo(self, tempo):
        self.tempo = tempo    
    def getTempo(self):
        return self.tempo
    def setAction(self, action):
        self.action = action    
    def getAction(self):
        return self.action

def BirthdayAction(graphics, canvas, font, clrPrimary, clrSecondary, year):
    color = graphics.Color(255,230,230)
    graphics.DrawText(canvas, font, 47, 21, color, str(year-1997))
    graphics.DrawText(canvas, font, 47, 22, color, str(year-1997))

SCENES = [
    Scene(RGB(255,255,255), RGB(255,255,255), ["./bmps/blank.bmp", "./bmps/blank.bmp"], 4),                                                                                # -0-  Notification 
    Scene(RGB(255,190,0), RGB(255,100,0), ["./bmps/scarecrow_1.bmp", "./bmps/scarecrow_2.bmp"], 4),                                                                        # -1-  Scarecrow
    Scene(RGB(255,255,255), RGB(245,100,255), ["./bmps/pinkcake_1.bmp", "./bmps/pinkcake_2.bmp", "./bmps/pinkcake_3.bmp", "./bmps/pinkcake_4.bmp"], 1, BirthdayAction),    # -2-  Birthday
    Scene(RGB(255,255,255), RGB(255,180,255), ["./bmps/daffodil_1.bmp", "./bmps/daffodil_2.bmp"], 4),                                                                      # -3-  Daffodil
    Scene(RGB(255,190,0), RGB(255,130,0), ["./bmps/pumpkin_1.bmp", "./bmps/pumpkin_2.bmp"], 4),                                                                            # -4-  Pumpkin
    Scene(RGB(200,190,0), RGB(255,190,0), ["./bmps/sunflower_1.bmp", "./bmps/sunflower_2.bmp"], 4),                                                                        # -5-  Sunflowers
    Scene(RGB(255,255,255), RGB(0,255,255), ["./bmps/wreath_1.bmp", "./bmps/wreath_2.bmp"], 4),                                                                            # -6-  Wreath
    Scene(RGB(255,255,255), RGB(0,255,255), ["./bmps/snowman_1.bmp", "./bmps/snowman_2.bmp"], 4),                                                                          # -7-  Snowman
    Scene(RGB(255,255,255), RGB(255,255,0), 
        ["./bmps/egg_1.bmp", "./bmps/egg_1.bmp", "./bmps/egg_2.bmp", "./bmps/egg_3.bmp", 
        "./bmps/egg_4.bmp", "./bmps/egg_4.bmp", "./bmps/egg_4.bmp", "./bmps/egg_4.bmp", 
        "./bmps/egg_3.bmp", "./bmps/egg_2.bmp", "./bmps/egg_1.bmp", "./bmps/egg_1.bmp",
        ], 1),                                                                                                                                                             # -8-  Egg
    Scene(RGB(255, 126, 0), RGB(255,50,80), ["./bmps/turkey_1.bmp", "./bmps/turkey_2.bmp", "./bmps/turkey_3.bmp"], 1),                                                     # -9-  Turkey7
]