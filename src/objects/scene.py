from objects.rgb import RGB

class Scene:    
    def __init__(self, primaryColor, secondaryColor, tertiaryColor, quaternaryColor, bmps, tempo, action=None):      
        self.primaryColor = primaryColor            
        self.secondaryColor = secondaryColor
        self.tertiaryColor = tertiaryColor           
        self.quaternaryColor = quaternaryColor           
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
    def setTertiaryColor(self, tertiaryColor):
        self.tertiaryColor = tertiaryColor
    def getTertiaryColor(self):    
        return self.tertiaryColor        
    def setQuaternaryColor(self, quaternaryColor):
        self.quaternaryColor = quaternaryColor
    def getQuaternaryColor(self):    
        return self.quaternaryColor    
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
    # -0-  Notification 
    Scene(
        RGB(255,255,255), RGB(255,255,255), RGB(255,255,255), RGB(255,255,255),
        ["./bmps/blank.bmp", "./bmps/blank.bmp"], 
        4
    ),
    # -1-  Wreath
    Scene(
        RGB(125,79,36), RGB(0,180,0), RGB(255, 0, 0), RGB(0,180,0), 
        ["./bmps/wreath_1.bmp", "./bmps/wreath_2.bmp"], 
        4
    ),
    # -2- Turkey
    Scene(
        RGB(125,79,36), RGB(255,150,0), RGB(255,50,80) ,RGB(255,190,0), 
        ["./bmps/turkey_1.bmp", "./bmps/turkey_2.bmp", "./bmps/turkey_3.bmp"], 
        2
    ),
    # -3-  Egg
    Scene(
        RGB(255,255,255), RGB(245,160,255), RGB(255,255,120), RGB(160,245,255),
        [
                "./bmps/egg_1.bmp", "./bmps/egg_1.bmp", "./bmps/egg_2.bmp", "./bmps/egg_3.bmp", 
                "./bmps/egg_4.bmp", "./bmps/egg_4.bmp", "./bmps/egg_4.bmp", "./bmps/egg_4.bmp", 
                "./bmps/egg_3.bmp", "./bmps/egg_2.bmp", "./bmps/egg_1.bmp", "./bmps/egg_1.bmp",
        ], 
        1
    ),
    # -4- Independance Day
    Scene(
        RGB(255,0,0), RGB(255,255,255), RGB(255,255,255), RGB(0,0,255),
        [
            "./bmps/blank.bmp", "./bmps/firework_1.bmp", "./bmps/firework_2.bmp", "./bmps/firework_3.bmp", 
            "./bmps/firework_4.bmp", "./bmps/firework_5.bmp", "./bmps/firework_6.bmp", "./bmps/firework_7.bmp", 
            "./bmps/firework_8.bmp", "./bmps/firework_9.bmp", "./bmps/firework_10.bmp", "./bmps/firework_11.bmp", 
            "./bmps/firework_12.bmp", "./bmps/firework_13.bmp", "./bmps/firework_14.bmp", "./bmps/firework_15.bmp"
        ], 
        1
    ),
    # -5- New Years Eve
    Scene(
        RGB(255,222,0), RGB(223,223,223), RGB(255,222,0), RGB(223,223,223),
        [
            "./bmps/champagne_1.bmp", "./bmps/champagne_1.bmp", "./bmps/champagne_1.bmp", "./bmps/champagne_1.bmp",
            "./bmps/champagne_1.bmp", "./bmps/champagne_2.bmp", "./bmps/champagne_3.bmp", "./bmps/champagne_4.bmp",
            "./bmps/champagne_4.bmp", "./bmps/champagne_5.bmp", "./bmps/champagne_4.bmp", "./bmps/champagne_5.bmp",
            "./bmps/champagne_4.bmp", "./bmps/champagne_5.bmp", "./bmps/champagne_4.bmp", "./bmps/champagne_5.bmp",
            "./bmps/champagne_5.bmp", "./bmps/champagne_6.bmp", "./bmps/champagne_7.bmp", "./bmps/champagne_8.bmp"
        ], 
        1
    ),
    # -6-  New Years Day
    Scene(
        RGB(255,255,255), RGB(255,255,255), RGB(255,255,255), RGB(255,255,255),
        ["./bmps/blank.bmp", "./bmps/blank.bmp"], 
        1
    ),   
    # -7-  Valentines
    Scene(
        RGB(255,0,0), RGB(155,0,0), RGB(255,0,50), RGB(255,155,155),
        ["./bmps/heart_1.bmp", "./bmps/heart_2.bmp", "./bmps/heart_3.bmp", "./bmps/heart_4.bmp"], 
        1
    ),
    # -8-  St. Patricks
    Scene(
        RGB(0,255, 0), RGB(0 ,155, 0), RGB(0,255,50), RGB(155,255,155),
        ["./bmps/clover_1.bmp", "./bmps/clover_2.bmp", "./bmps/clover_3.bmp", "./bmps/clover_4.bmp", "./bmps/clover_5.bmp"], 
        1
    ),
    # -9-  St. Martin's Day
    Scene(
        RGB(125,79,36), RGB(255,150,0), RGB(255,50,80) ,RGB(255,190,0), 
        ["./bmps/paper-lantern_1.bmp", "./bmps/paper-lantern_2.bmp", "./bmps/paper-lantern_3.bmp"], 
        4
    ),
    # -10-  Halloween
    Scene(
        RGB(200,150,0), RGB(200,105,0),RGB(80,50,23), RGB(140,77,0), 
        ["./bmps/lantern_1.bmp", "./bmps/lantern_2.bmp"], 
        4
    ),
    # -11-  Birthday
    Scene(
        RGB(255,230,230), RGB(199,84,193),RGB(237,28,36), RGB(199,84,193), 
        ["./bmps/pinkcake_1.bmp", "./bmps/pinkcake_2.bmp", "./bmps/pinkcake_3.bmp", "./bmps/pinkcake_4.bmp"], 
        1, 
        BirthdayAction
    ),
    # -12-  Daffodil
    Scene(
        RGB(255,251,162), RGB(255,218,15), RGB(255,180,255), RGB(50,230,0), 
        ["./bmps/daffodil_1.bmp", "./bmps/daffodil_2.bmp"], 
        4
    ),
    # -13-  Sunflowers
    Scene(
        RGB(200,190,0), RGB(255,150,0),RGB(128,64,0), RGB(0,96,0),  
        ["./bmps/sunflower_1.bmp", "./bmps/sunflower_2.bmp"], 
        4
    ),
    # -14-  Pumpkin
    Scene(
        RGB(255,190,0), RGB(255,130,0),RGB(107,68,31), RGB(175,96,0), 
        ["./bmps/pumpkin_1.bmp", "./bmps/pumpkin_2.bmp"], 
        4
    ),
    # -15-  Snowman
    Scene(
        RGB(255,255,255), RGB(0,255,255), RGB(255,255,255), RGB(94,40,0), 
        ["./bmps/snowman_1.bmp", "./bmps/snowman_2.bmp"], 
        4
    ),
    # -16-  Scarecrow
    Scene(
        RGB(255,190,0), RGB(255,100,0), RGB(255,190,0), RGB(255,190,0), 
        ["./bmps/scarecrow_1.bmp", "./bmps/scarecrow_2.bmp"], 
        4
    ),
]