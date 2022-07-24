class Scene:    
    def __init__(self, primaryColor, secondaryColor, bmp, bmp2=None):      
        self.primaryColor = primaryColor            
        self.secondaryColor = secondaryColor            
        self.bmp = bmp                                  
        self.bmp2 = bmp2        
    def setBMP(self, bmp):
        self.bmp = bmp
    def getBMP(self):    
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