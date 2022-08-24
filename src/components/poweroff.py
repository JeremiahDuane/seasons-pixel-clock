import requests
from datetime import datetime
from rgbmatrix import graphics
from PIL import Image
from objects.scene import SCENES
from system.config import config_matrix

FONT_SUBTITLE = graphics.Font()
FONT_SUBTITLE.LoadFont("/home/jgage/code/seasons-pixel-clock/fonts/pixelclock-subtitle-7.bdf") 

def getPowerOffCanvas(cvsPowerOff):
    #Scene
    scene = SCENES[0]
    clrPrimary = graphics.Color(scene.getPrimaryColor().R,scene.getPrimaryColor().G,scene.getPrimaryColor().B) 
    clrSecondary = graphics.Color(scene.getSecondaryColor().R,scene.getSecondaryColor().G,scene.getSecondaryColor().B) 
    strImagePath = scene.getBMP1()

    #Draw
    image = Image.open(strImagePath)
    image.thumbnail((config_matrix["width"], config_matrix["height"]), Image.ANTIALIAS)
    cvsPowerOff.SetImage(image.convert('RGB'))  

    graphics.DrawText(cvsPowerOff, FONT_SUBTITLE, 0, 12, clrPrimary, "Powering off...")

    return cvsPowerOff
