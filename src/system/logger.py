from curses import nonl
from datetime import datetime
from config import package

debug = 0
def init():
    global debug
    debug+=1
    print(debug)

def logger(error):

    def log(newLine):
        global debug
        global package
        nonlocal error
        
        return [
            f'----------------------------------------------------------{str(datetime.now())}{newLine}',
            f'    Log#: {debug}                                                              {newLine}',
            f'    Error#: {error}                                                            {newLine}',
            f'----------------------------------------------------------{package.version}    {newLine}'
        ]

    with open("/home/jgage/code/seasons-pixel-clock/src/system/log.txt", "a") as file:
        file.writelines(log('\n'))
        file.close

    for line in log('\n'):
        print(line)
