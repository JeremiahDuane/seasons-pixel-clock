from PIL import Image
from system.config import config_matrix, config_timezone

def getBlankCanvas(cvsBlank):
    image = Image.open("./bmps/blank.bmp")
    image.thumbnail((config_matrix["width"], config_matrix["height"]), Image.ANTIALIAS)
    cvsBlank.SetImage(image.convert('RGB')) 
    
    return cvsBlank
